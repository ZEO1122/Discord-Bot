# -*- coding: utf-8 -*-
"""
OIBC 2025 일사량 예측 - Simple CatBoost Baseline

특징:
- train.csv / test.csv 기준의 가벼운 베이스라인
- time 기반 feature + 몇 가지 기상 파생변수만 사용
- 단일 모델 + 단일 time-based validation
- 업샘플링, 복잡한 clear-sky 스케일링, K-Fold, 무거운 진단 로직 제거 (메모리 사용 최소화)

사용법 예시:
    conda install -c conda-forge catboost
    python baseline_catboost_simple.py \
        --data_dir ./OIBC_2025_DATA \
        --valid_ratio 0.1 \
        --iters 2000 \
        --lr 0.03 \
        --depth 8 \
        --out submission_catboost_baseline.csv
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from typing import Tuple, List

SEED = 42
np.random.seed(SEED)


# ======================
# 1. 공통 유틸
# ======================

def _strip_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [str(c).strip() for c in df.columns]
    return df


def _parse_time(df: pd.DataFrame, col: str = "time") -> pd.DataFrame:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")
        # tz 정보 있으면 제거
        try:
            df[col] = df[col].dt.tz_localize(None)
        except Exception:
            try:
                df[col] = df[col].dt.tz_convert(None)
            except Exception:
                pass
    return df


def load_oibc_data(data_dir: Path) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train_path = data_dir / "train.csv"
    test_path = data_dir / "test.csv"

    if not train_path.exists() or not test_path.exists():
        raise FileNotFoundError("train.csv 또는 test.csv를 찾을 수 없습니다.")

    train = pd.read_csv(train_path, low_memory=False)
    test = pd.read_csv(test_path, low_memory=False)

    train = _strip_columns(train)
    test = _strip_columns(test)

    train = _parse_time(train, "time")
    test = _parse_time(test, "time")

    # sample_submission 자동 탐색
    cand = [
        data_dir / "sample_submission.csv",
        data_dir / "sample_submission_v1.csv",
        data_dir / "submission_sample.csv",
    ]
    sub_path = next((p for p in cand if p.exists()), None)
    if sub_path is None:
        raise FileNotFoundError("sample_submission.csv 파일을 찾지 못했습니다.")
    sub = pd.read_csv(sub_path)
    sub = _strip_columns(sub)
    _parse_time(sub, "time")

    # 타깃 이름 방어 (nins 소문자 고정)
    if "nins" not in train.columns:
        cand = [c for c in train.columns if str(c).strip().lower() == "nins"]
        if not cand:
            raise KeyError("train.csv에 'nins' 타깃 컬럼이 존재하지 않습니다.")
        train = train.rename(columns={cand[0]: "nins"})

    return train, test, sub


# ======================
# 2. Feature Engineering (가벼운 버전)
# ======================

TIME_COL = "time"
TARGET_COL = "nins"


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    if TIME_COL not in df.columns:
        return df

    t = df[TIME_COL]
    df["hour"] = t.dt.hour
    df["minute"] = t.dt.minute
    df["doy"] = t.dt.dayofyear

    # 주기형 인코딩
    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24.0)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24.0)
    df["doy_sin"] = np.sin(2 * np.pi * df["doy"] / 365.0)
    df["doy_cos"] = np.cos(2 * np.pi * df["doy"] / 365.0)
    return df


def add_basic_weather_features(df: pd.DataFrame) -> pd.DataFrame:
    # 일부 대표적인 컬럼만 활용 (있을 때만)
    if {"cloud_a", "cloud_b"}.issubset(df.columns):
        df["cloud_mean"] = (pd.to_numeric(df["cloud_a"], errors="coerce") +
                            pd.to_numeric(df["cloud_b"], errors="coerce")) / 2.0

    if "precip_1h" in df.columns:
        df["precip_flag"] = (pd.to_numeric(df["precip_1h"], errors="coerce").fillna(0) > 0).astype(int)

    if "rain" in df.columns:
        df["rain_flag"] = (pd.to_numeric(df["rain"], errors="coerce").fillna(0) > 0).astype(int)

    if "snow" in df.columns:
        df["snow_flag"] = (pd.to_numeric(df["snow"], errors="coerce").fillna(0) > 0).astype(int)

    # 풍향 → sin/cos
    for col in ["wind_dir_a", "wind_dir_b"]:
        if col in df.columns:
            rad = np.deg2rad(pd.to_numeric(df[col], errors="coerce") % 360.0)
            df[f"{col}_sin"] = np.sin(rad)
            df[f"{col}_cos"] = np.cos(rad)

    # 돌풍 대비 평균풍
    if "wind_gust_spd" in df.columns and "wind_spd_a" in df.columns:
        df["gust_delta_a"] = (
            pd.to_numeric(df["wind_gust_spd"], errors="coerce")
            - pd.to_numeric(df["wind_spd_a"], errors="coerce")
        ).clip(lower=0)

    return df


def build_features(df: pd.DataFrame, is_train: bool) -> pd.DataFrame:
    df = df.copy()

    df = add_time_features(df)
    df = add_basic_weather_features(df)

    # 숫자/범주형 분리:
    # - pv_id, type은 catboost 범주형으로 사용 (있으면)
    # - 나머지는 숫자로 시도
    cat_cols: List[str] = []
    for c in ["pv_id", "type"]:
        if c in df.columns:
            cat_cols.append(c)
            df[c] = df[c].astype(str).fillna("NA")

    # 타깃은 건들지 않음
    exclude = set(cat_cols + [TIME_COL])
    if is_train:
        exclude.add(TARGET_COL)

    for c in df.columns:
        if c not in exclude:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    return df


# ======================
# 3. Train/Valid Split
# ======================

def time_based_split(train_df: pd.DataFrame, valid_ratio: float) -> Tuple[pd.DataFrame, pd.DataFrame]:
    if TIME_COL not in train_df.columns:
        # time이 없으면 단순 홀드아웃
        n = len(train_df)
        cut = int(n * (1.0 - valid_ratio))
        return train_df.iloc[:cut].copy(), train_df.iloc[cut:].copy()

    train_sorted = train_df.sort_values(TIME_COL).reset_index(drop=True)
    cut_time = train_sorted[TIME_COL].quantile(1.0 - valid_ratio)
    tr = train_sorted[train_sorted[TIME_COL] < cut_time].copy()
    va = train_sorted[train_sorted[TIME_COL] >= cut_time].copy()
    return tr, va


# ======================
# 4. Train & Predict
# ======================

def train_and_predict(args):
    from catboost import CatBoostRegressor, Pool  # 로컬에서 임포트

    data_dir = Path(args.data_dir)
    train_raw, test_raw, sub = load_oibc_data(data_dir)

    # 타깃 결측 제거
    train_raw = train_raw.copy()
    train_raw[TARGET_COL] = pd.to_numeric(train_raw[TARGET_COL], errors="coerce")
    train_raw = train_raw[np.isfinite(train_raw[TARGET_COL])].reset_index(drop=True)

    # Feature build
    train_feat = build_features(train_raw, is_train=True)
    test_feat = build_features(test_raw, is_train=False)

    # 공통 feature set (train/test 교집합)
    feature_cols = [c for c in train_feat.columns
                    if c in test_feat.columns and c not in (TIME_COL,)]
    # 타깃/시간은 제외
    feature_cols = [c for c in feature_cols if c != TARGET_COL]

    # Split
    tr_df, va_df = time_based_split(train_feat, args.valid_ratio)

    X_tr = tr_df[feature_cols]
    y_tr = train_raw.loc[tr_df.index, TARGET_COL].values

    X_va = va_df[feature_cols]
    y_va = train_raw.loc[va_df.index, TARGET_COL].values

    # CatBoost 범주형 인덱스
    cat_features_idx = [
        i for i, c in enumerate(feature_cols)
        if c in ("pv_id", "type")
    ]

    train_pool = Pool(X_tr, y_tr, cat_features=cat_features_idx)
    valid_pool = Pool(X_va, y_va, cat_features=cat_features_idx)
    test_pool = Pool(test_feat[feature_cols], cat_features=cat_features_idx)

    model = CatBoostRegressor(
        iterations=args.iters,
        learning_rate=args.lr,
        depth=args.depth,
        l2_leaf_reg=args.l2_leaf_reg,
        subsample=args.subsample,
        rsm=args.rsm,
        loss_function="MAE",
        eval_metric="MAE",
        random_seed=SEED,
        od_type="Iter",
        od_wait=args.od_wait,
        allow_writing_files=False,
        verbose=100,
    )

    model.fit(train_pool, eval_set=valid_pool, use_best_model=True)

    # Validation MAE 출력
    va_pred = model.predict(valid_pool)
    va_mae = float(np.mean(np.abs(va_pred - y_va)))
    print(f"[INFO] Validation MAE: {va_mae:.5f}")

    # Test 예측
    te_pred = model.predict(test_pool)
    te_pred = np.clip(te_pred, 0, None)  # 음수 방지 (일사량)

    # ======================
    # 5. Submission 매핑
    # ======================
    sub_out = sub.copy()

    # sample_submission이 test와 같은 순서라고 가정하는 가장 단순한 방식
    # (대회 기본 포맷이 이 구조면 이게 가장 안전하고 메모리도 적게 듦)
    if len(sub_out) == len(test_raw):
        sub_out["nins"] = te_pred.astype(float)
    else:
        # 길이 다르면 key merge 시도: time, pv_id, type 교집합 사용
        key_cols = [c for c in ("time", "pv_id", "type")
                    if c in sub_out.columns and c in test_raw.columns]
        if not key_cols:
            raise RuntimeError(
                "submission과 test row 수가 다르고, 매핑 가능한 공통 키(time/pv_id/type)가 없습니다."
            )
        tmp_pred = test_raw.copy()
        tmp_pred["nins"] = te_pred.astype(float)
        sub_out = sub_out.merge(
            tmp_pred[key_cols + ["nins"]],
            on=key_cols,
            how="left",
            validate="one_to_one",
        )
        if sub_out["nins"].isna().any():
            print("[WARN] 일부 submission 행에 예측 누락 → 0으로 채움")
            sub_out["nins"] = sub_out["nins"].fillna(0.0)

    out_path = Path(args.out)
    sub_out.to_csv(out_path, index=False)
    print(f"[INFO] Saved submission to: {out_path.resolve()}")


# ======================
# 6. CLI
# ======================

def get_args():
    p = argparse.ArgumentParser()

    p.add_argument("--data_dir", type=str, default="./OIBC_2025_DATA")
    p.add_argument("--valid_ratio", type=float, default=0.10)

    p.add_argument("--iters", type=int, default=2000)
    p.add_argument("--lr", type=float, default=0.03)
    p.add_argument("--depth", type=int, default=8)
    p.add_argument("--l2_leaf_reg", type=float, default=3.0)
    p.add_argument("--subsample", type=float, default=0.8)
    p.add_argument("--rsm", type=float, default=0.8)
    p.add_argument("--od_wait", type=int, default=200)

    p.add_argument("--out", type=str, default="submission_catboost_baseline.csv")

    return p.parse_args()


if __name__ == "__main__":
    args = get_args()
    train_and_predict(args)