# -*- coding: utf-8 -*-
"""
OIBC 2025 일사량 예측 - CatBoost 단일 스크립트 베이스라인
사용법:
    conda install -c conda-forge catboost
    python model_catboost.py \
        --data_dir ./OIBC_2025_DATA \
        --valid_ratio 0.10 \
        --iters 4000 \
        --lr 0.03 \
        --depth 8 \
        --od_wait 200 \
        --day_weight 3.0 \
        --out submission_catboost.csv
        
- Note: 테스트 단계에서는 업샘플링을 수행하지 않습니다(원본 그리드 유지). 제출 격자가 더 촘촘하면 매핑 오류가 발생합니다.
- Added options: --val_eval_mode (weighted_day|plain_all), --global_scale, --eval_cos_day_threshold; plus per-segment (day/twilight/night) MAE diagnostics.
"""

import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import warnings

# --- Added evaluation options and diagnostics (2025-11-06) ---

from typing import List, Tuple

warnings.filterwarnings(
    "ignore",
    message="DataFrameGroupBy.apply operated on the grouping columns",
    category=FutureWarning,
)

try:
    from catboost import CatBoostRegressor, Pool
except Exception as e:
    raise ImportError(
        "catboost가 설치되어 있지 않습니다. 다음을 실행하세요:\n"
        "    conda install -c conda-forge catboost\n"
    ) from e

SEED = 42
rng = np.random.default_rng(SEED)
np.random.seed(SEED)

# ---- 1) 컬럼 그룹 정의 ---- #
LINEAR_COLS = [
    "cloud_a","cloud_b","ceiling","uv_idx","vis","rel_hum","humidity",
    "dew_point","pressure","ground_press","temp_a","temp_b","appr_temp",
    "real_feel_temp","real_feel_temp_shade","wind_spd_a","wind_spd_b","wind_gust_spd"
]
STEP_COLS   = ["precip_1h","rain","snow","wind_dir_a","wind_dir_b"]
DROP_COLS   = ["energy"]  # 테스트에 없음 + 누수 위험

# === A) 주간만 학습 & 야간 0 예측 / B) Clear-sky 기반 clearness index 타깃 /
#     C) 짧은 랙/롤링 피처 / D) 월별 Blocked KFold 앙상블 ===
LAG_SPEC = [
    ("uv_idx", 1),       # 5분
    ("cloud_mean", 1),   # 5분
    ("vis", 2),          # 10분
    ("rel_hum", 2),      # 10분
]
ROLL_SPEC = [
    ("cloud_mean", 3, "mean"),   # 15분 평균
    ("vis", 3, "median"),        # 15분 중앙값
    ("rel_hum", 3, "std"),       # 15분 표준편차
]

# ---- 중복 컬럼/타깃 방어 유틸 ---- #
def _remove_dup_columns(df: pd.DataFrame) -> pd.DataFrame:
    """중복 컬럼명이 있으면 첫 번째만 남기고 제거"""
    if df.columns.duplicated().any():
        dup_names = df.columns[df.columns.duplicated()].unique().tolist()
        print(f"[WARN] 중복 컬럼 제거: {dup_names}")
        df = df.loc[:, ~df.columns.duplicated()].copy()
    return df

def _fix_dup_target(df: pd.DataFrame, target: str = "nins") -> pd.DataFrame:
    """타깃 컬럼이 중복된 경우 첫 번째 비결측값을 우선으로 합쳐 하나로 만든 후 나머지 제거"""
    if (df.columns == target).sum() > 1:
        tcols = [c for c in df.columns if c == target]
        print(f"[WARN] 타깃 '{target}' 중복 {len(tcols)}개 → 병합")
        merged = pd.to_numeric(df[tcols].bfill(axis=1).iloc[:, 0], errors="coerce")
        df = df.drop(columns=tcols).copy()
        df[target] = merged
    return df

# ---- 월별 Blocked KFold 생성 ---- #
def make_month_folds(df: pd.DataFrame, n_folds: int) -> List[Tuple[np.ndarray, np.ndarray]]:
    """time의 month 기준으로 블록을 나누어 폴드 생성. 반환은 (train_idx, valid_idx) 리스트.
    타임존 포함 시 tz를 제거하여 경고/오류를 방지한다.
    """
    t = df["time"]
    # tz-aware → naive 변환 시도 (실패하면 원본 유지)
    try:
        t = t.dt.tz_localize(None)
    except Exception:
        pass
    months = t.dt.to_period("M").astype(str)
    uniq = months.dropna().unique().tolist()
    uniq.sort()
    # 월을 순서대로 n_folds로 분할
    buckets = [[] for _ in range(n_folds)]
    for i, m in enumerate(uniq):
        buckets[i % n_folds].append(m)
    folds = []
    for k in range(n_folds):
        val_months = set(buckets[k])
        val_mask = months.isin(val_months).values
        tr_idx = np.where(~val_mask)[0]
        va_idx = np.where(val_mask)[0]
        folds.append((tr_idx, va_idx))
    return folds

# ---- Clear-sky 스케일링 ---- #
def compute_clear_scale(train_df: pd.DataFrame, q: float = 0.98) -> float:
    """추정용 스케일 S. solar_cos_zen_pos가 없으면 필요한 최소 컬럼(time, coord1, coord2)로 계산 후 사용."""
    if "solar_cos_zen_pos" not in train_df.columns:
        # 필요한 최소 컬럼이 없다면 안전하게 1.0 반환
        need_cols = {"time", "coord1", "coord2"}
        if not need_cols.issubset(set(train_df.columns)):
            return 1.0
        tmp = train_df.copy()
        tmp = add_solar_features(tmp)
    else:
        tmp = train_df
    # 낮 구간만 사용
    day_mask = (pd.to_numeric(tmp["solar_cos_zen_pos"], errors="coerce") > 0)
    if "nins" in tmp.columns:
        day_mask = day_mask & (~tmp["nins"].isna())
    if day_mask.sum() == 0:
        return 1.0
    nins_ser = pd.to_numeric(tmp.loc[day_mask, "nins"], errors="coerce") if "nins" in tmp.columns else None
    cos_ser = pd.to_numeric(tmp.loc[day_mask, "solar_cos_zen_pos"], errors="coerce")
    # 박명 구간 배제: cos > 0.2만 사용
    strong = cos_ser > 0.2
    if nins_ser is not None:
        strong &= (pd.to_numeric(nins_ser, errors="coerce") > 0)
    if strong.sum() >= 1000:
        nins_ser = nins_ser[strong]
        cos_ser = cos_ser[strong]
    if nins_ser is None:
        return 1.0
    nins_q = np.nanquantile(nins_ser, q)
    cos_q = np.nanquantile(cos_ser, q)
    if not np.isfinite(cos_q) or cos_q <= 1e-6:
        return 1.0
    return float(nins_q / cos_q)


# ---- 2) 유틸 ---- #
def load_csvs(data_dir: Path):
    train = pd.read_csv(data_dir / "train.csv", parse_dates=["time"], low_memory=False)
    test  = pd.read_csv(data_dir / "test.csv",  parse_dates=["time"], low_memory=False)

    # 0) 컬럼명 공백 정리(양끝 공백 제거). 대소문자는 유지.
    train.columns = [str(c).strip() for c in train.columns]
    test.columns  = [str(c).strip() for c in test.columns]

    # 0-1) 'time' tz-aware → naive 변환 시도
    if "time" in train.columns and pd.api.types.is_datetime64_any_dtype(train["time"]):
        try:
            train["time"] = train["time"].dt.tz_localize(None)
        except Exception:
            pass
    if "time" in test.columns and pd.api.types.is_datetime64_any_dtype(test["time"]):
        try:
            test["time"] = test["time"].dt.tz_localize(None)
        except Exception:
            pass

    # 0-2) nins 컬럼 복구 시도(대소문자/공백 무시)
    if "nins" not in train.columns:
        cand = [c for c in train.columns if str(c).strip().lower() == "nins"]
        if cand:
            train = train.rename(columns={cand[0]: "nins"})

    # 1) 중복 컬럼 우선 정리
    train = _remove_dup_columns(train)
    test  = _remove_dup_columns(test)
    train = _fix_dup_target(train, target="nins")

    # 2) 공통 컬럼 + nins 구성 (순서 유지, 중복 제거)
    common = [c for c in train.columns if c in test.columns]
    if "nins" in train.columns:
        common.append("nins")
    common = list(dict.fromkeys(common))
    train = train[common].copy()

    # 3) 혹시 남아있을 수 있는 중복 다시 정리
    train = _remove_dup_columns(train)
    train = _fix_dup_target(train, target="nins")
    test  = _remove_dup_columns(test)
    return train, test

def sort_by_key(df: pd.DataFrame) -> pd.DataFrame:
    keys = [c for c in ["pv_id", "time"] if c in df.columns]
    if not keys:
        return df.reset_index(drop=True)
    return df.sort_values(keys).reset_index(drop=True)

def upsample_hourly_to_5min(df, cols_linear, cols_step):
    """pv_id별로 5분 그리드 reindex → 선형/전파 보간"""
    outs = []
    for pid, g in df.groupby("pv_id", sort=False):
        g = g.set_index("time").sort_index()
        idx5 = pd.date_range(g.index.min(), g.index.max(), freq="5min")
        g = g.reindex(idx5)
        lin = [c for c in cols_linear if c in g.columns]
        stp = [c for c in cols_step   if c in g.columns]
        if lin:
            g[lin] = g[lin].interpolate("time", limit=12, limit_direction="both")
        if stp:
            g[stp] = g[stp].ffill().bfill()
        if "type" in g.columns:
            g["type"] = g["type"].ffill().bfill()
        # 좌표/정적 메타데이터는 계단형으로 전파 (업샘플 시 NaN 방지)
        for meta_col in ["coord1", "coord2"]:
            if meta_col in g.columns:
                g[meta_col] = pd.to_numeric(g[meta_col], errors="coerce").ffill().bfill()
        g["pv_id"] = pid
        outs.append(g.reset_index().rename(columns={"index":"time"}))
    return pd.concat(outs, ignore_index=True)



def clip_physical(df: pd.DataFrame) -> pd.DataFrame:
    clip_map = {
        "cloud_a":(0,1), "cloud_b":(0,1),
        "rel_hum":(0,100), "humidity":(0,100),
        "uv_idx":(0,15), "vis":(0, np.inf),
        "pressure":(850,1100), "ground_press":(850,1100),
        "wind_spd_a":(0,np.inf), "wind_spd_b":(0,np.inf),
        "wind_gust_spd":(0,np.inf),
        "precip_1h":(0,np.inf),
        "nins":(0,np.inf),
    }
    for c,(lo,hi) in clip_map.items():
        if c in df.columns:
            df[c] = df[c].clip(lower=lo, upper=hi)
    return df

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    # 구름 평균
    if "cloud_a" in df.columns and "cloud_b" in df.columns:
        df["cloud_mean"] = (df["cloud_a"].astype(float) + df["cloud_b"].astype(float))/2.0
        df["cloud_mean"] = df["cloud_mean"].clip(0,1)

    # 강수 플래그
    if "precip_1h" in df.columns:
        df["precip_flag"] = (df["precip_1h"].fillna(0) > 0).astype(int)
    if "rain" in df.columns:
        df["rain_flag"]   = (df["rain"].fillna(0) > 0).astype(int)
    if "snow" in df.columns:
        df["snow_flag"]   = (df["snow"].fillna(0) > 0).astype(int)

    # 풍향 → sin, cos
    for c in ["wind_dir_a", "wind_dir_b"]:
        if c in df.columns:
            rad = np.deg2rad(pd.to_numeric(df[c], errors="coerce") % 360.0)
            df[f"{c}_sin"] = np.sin(rad)
            df[f"{c}_cos"] = np.cos(rad)

    # 돌풍-평균풍 차이
    if "wind_gust_spd" in df.columns and "wind_spd_a" in df.columns:
        df["gust_delta_a"] = (df["wind_gust_spd"] - df["wind_spd_a"]).clip(lower=0)
    if "wind_gust_spd" in df.columns and "wind_spd_b" in df.columns:
        df["gust_delta_b"] = (df["wind_gust_spd"] - df["wind_spd_b"]).clip(lower=0)

    # 시간 파생
    df["hour"] = df["time"].dt.hour
    df["doy"]  = df["time"].dt.dayofyear
    df["hour_sin"] = np.sin(2*np.pi*df["hour"]/24.0)
    df["hour_cos"] = np.cos(2*np.pi*df["hour"]/24.0)

    # 추가 상호작용
    if "vis" in df.columns and "rel_hum" in df.columns:
        df["haze_inter"] = pd.to_numeric(df["vis"], errors="coerce") * pd.to_numeric(df["rel_hum"], errors="coerce")
    if "temp_a" in df.columns and "cloud_mean" in df.columns:
        df["thermal_inter"] = pd.to_numeric(df["temp_a"], errors="coerce") * (1 - pd.to_numeric(df["cloud_mean"], errors="coerce").clip(0,1))

    return df

def add_solar_features(df: pd.DataFrame) -> pd.DataFrame:
    """외부 데이터 없이 위도/경도/시간 기반 태양 위치 간이 파생"""
    if "coord1" not in df.columns or "coord2" not in df.columns:
        df["solar_elev"] = 0.0
        df["solar_cos_zen_pos"] = 0.0
        df["daylight_flag"] = 0
        df["doy_sin"] = np.sin(2*np.pi*df["time"].dt.dayofyear/365.0)
        df["doy_cos"] = np.cos(2*np.pi*df["time"].dt.dayofyear/365.0)
        return df

    lat = np.deg2rad(pd.to_numeric(df["coord1"], errors="coerce"))
    lon_deg = pd.to_numeric(df["coord2"], errors="coerce")

    doy = df["time"].dt.dayofyear
    hour = df["time"].dt.hour + df["time"].dt.minute/60.0

    B = 2*np.pi*(doy-81)/364.0
    EoT = 9.87*np.sin(2*B) - 7.53*np.cos(B) - 1.5*np.sin(B)  # 분
    LSTM = 15*np.round(lon_deg/15.0)
    TC = 4*(lon_deg - LSTM) + EoT
    LST = hour + TC/60.0
    HRA = np.deg2rad(15*(LST-12.0))
    decl = np.deg2rad(23.45) * np.sin(2*np.pi*(284 + doy)/365.0)

    cos_zen = np.sin(lat)*np.sin(decl) + np.cos(lat)*np.cos(decl)*np.cos(HRA)
    cos_zen = np.clip(cos_zen, -1.0, 1.0)
    zenith  = np.arccos(cos_zen)
    elev    = np.pi/2 - zenith

    df["solar_elev"] = elev
    df["solar_cos_zen_pos"] = np.clip(np.cos(zenith), 0, None)  # 낮: 0~1, 밤: 0
    df["daylight_flag"] = (df["solar_elev"] > 0).astype(int)
    df["doy_sin"] = np.sin(2*np.pi*doy/365.0)
    df["doy_cos"] = np.cos(2*np.pi*doy/365.0)
    return df

def make_matrix(df: pd.DataFrame, is_train=True, for_catboost=True):
    # 결측 플래그 (결측 자체를 신호로)
    for c in (LINEAR_COLS + STEP_COLS):
        if c in df.columns:
            df[f"is_imputed_{c}"] = df[c].isna().astype(int)

    # 그룹 내 보간
    lin = [c for c in LINEAR_COLS if c in df.columns]
    stp = [c for c in STEP_COLS   if c in df.columns]

    if lin or stp:
        def _fill(g):
            gi = g.set_index("time").sort_index()
            if lin:
                gi[lin] = gi[lin].interpolate("time", limit=12, limit_direction="both").ffill().bfill()
            if stp:
                gi[stp] = gi[stp].ffill().bfill()
            # 좌표는 그룹 내에서 상수 취급 → 전파
            for meta_col in ["coord1", "coord2"]:
                if meta_col in gi.columns:
                    gi[meta_col] = pd.to_numeric(gi[meta_col], errors="coerce").ffill().bfill()
            return gi.reset_index()
        if "pv_id" in df.columns:
            df = df.groupby(["pv_id"], group_keys=False).apply(_fill, include_groups=False)
        else:
            df = _fill(df)

    df = clip_physical(df)
    df = add_features(df)
    df = add_solar_features(df)

    # --- 랙/롤링 피처 (짧은 윈도우) ---
    sort_keys = [c for c in ["pv_id", "time"] if c in df.columns]
    if len(sort_keys) == 0:
        # 안전장치: 둘 다 없으면 랙/롤링은 전역 기준 시간순만 시도
        if "time" in df.columns:
            df = df.sort_values(["time"]).reset_index(drop=True)
        else:
            df = df.reset_index(drop=True)
    else:
        df = df.sort_values(sort_keys).reset_index(drop=True)

    def _add_lag_roll(g: pd.DataFrame) -> pd.DataFrame:
        g = g.sort_values("time")
        for col, lag in LAG_SPEC:
            if col in g.columns:
                g[f"{col}_lag{lag}"] = g[col].shift(lag)
        for col, win, how in ROLL_SPEC:
            if col in g.columns:
                if how == "mean":
                    g[f"{col}_roll{win}_mean"] = g[col].rolling(win, min_periods=1).mean()
                elif how == "median":
                    g[f"{col}_roll{win}_median"] = g[col].rolling(win, min_periods=1).median()
                elif how == "std":
                    g[f"{col}_roll{win}_std"] = g[col].rolling(win, min_periods=1).std()
        return g
    if "pv_id" in df.columns:
        df = df.groupby("pv_id", group_keys=False).apply(_add_lag_roll)
    else:
        # pv_id가 없으면 전체에 대해 적용
        df = _add_lag_roll(df)

    # 상호작용
    if "cloud_mean" in df.columns and "uv_idx" in df.columns:
        df["cloud_uv_inter"]  = df["cloud_mean"] * df["uv_idx"]
    if "cloud_mean" in df.columns and "solar_cos_zen_pos" in df.columns:
        df["cloud_sun_inter"] = df["cloud_mean"] * df["solar_cos_zen_pos"]

    # 최종 선택 피처
    chosen = [
        "cloud_mean","uv_idx","vis",
        "pressure","temp_a","rel_hum",
        "wind_spd_a","wind_dir_a_sin","wind_dir_a_cos","gust_delta_a",
        "precip_flag","rain_flag","snow_flag",
        "hour_sin","hour_cos","doy","doy_sin","doy_cos",
        "solar_cos_zen_pos","daylight_flag",
        "cloud_uv_inter","cloud_sun_inter",
        "coord1","coord2","pv_id",

        # 신규 상호작용/랙/롤링
        "haze_inter","thermal_inter",
        "uv_idx_lag1","cloud_mean_lag1","vis_lag2","rel_hum_lag2",
        "cloud_mean_roll3_mean","vis_roll3_median","rel_hum_roll3_std",
    ]
    X = df[[c for c in chosen if c in df.columns]].copy()

    # 숫자 캐스팅 / 범주형 설정
    for c in X.columns:
        if c != "pv_id":
            X[c] = pd.to_numeric(X[c], errors="coerce")
    if "pv_id" in X.columns and for_catboost:
        X["pv_id"] = X["pv_id"].astype(str)  # CatBoost에서 범주형 컬럼로 취급

    if is_train and "nins" in df.columns:
        y = pd.to_numeric(df["nins"], errors="coerce").values
        return X, y
    return X

def time_split(df: pd.DataFrame, valid_ratio=0.1):
    cut = df["time"].quantile(1.0 - valid_ratio)
    tr = df[df["time"] < cut].copy()
    va = df[df["time"] >= cut].copy()
    return tr, va

def mae(a, b) -> float:
    return float(np.mean(np.abs(a - b)))


def safe_mae(y_true, y_pred):
    """MAE with NaN/Inf safety and vector shape normalization."""
    y_true = np.asarray(y_true, dtype=float).reshape(-1)
    y_pred = np.asarray(y_pred, dtype=float).reshape(-1)
    m = np.isfinite(y_true) & np.isfinite(y_pred)
    if not np.any(m):
        return np.nan
    return float(np.mean(np.abs(y_true[m] - y_pred[m])))


# ---- 3) 메인 파이프라인 ---- #
def main(args):
    data_dir = Path(args.data_dir)
    train_full, test_full = load_csvs(data_dir)
    global_scale_S = None

    # 공통 정리
    for c in DROP_COLS:
        if c in train_full.columns: train_full = train_full.drop(columns=[c])
        if c in test_full.columns:  test_full  = test_full.drop(columns=[c])

    train_full = sort_by_key(train_full)
    test_full  = sort_by_key(test_full)

    # Optional: use one global clear-sky scale across folds
    if getattr(args, "global_scale", False):
        try:
            global_scale_S = compute_clear_scale(train_full)
            print(f"[OPT] Using global clear-sky scale S={global_scale_S:.6f}")
        except Exception as _e:
            print(f"[WARN] global scale estimation failed: {_e}")
            global_scale_S = None

    # 안전 방어
    train_full = _remove_dup_columns(train_full)
    train_full = _fix_dup_target(train_full, target="nins")
    if "nins" not in train_full.columns:
        raise KeyError("train.csv에 'nins' 컬럼이 없습니다. 데이터 경로를 확인하세요.")

    # 테스트는 절대 업샘플링하지 않음 (원본 해상도 유지)
    test_up = test_full.copy()
    try:
        tu_sorted = test_up.sort_values("time").reset_index(drop=True)
        if len(tu_sorted) >= 3:
            dt1 = (pd.to_datetime(tu_sorted.loc[1,"time"]) - pd.to_datetime(tu_sorted.loc[0,"time"]))
            dt2 = (pd.to_datetime(tu_sorted.loc[2,"time"]) - pd.to_datetime(tu_sorted.loc[1,"time"]))
            print(f"[DIAG] test time deltas (head): {dt1} | {dt2}")
    except Exception as _e:
        print(f"[WARN] failed to inspect test time deltas: {_e}")
    X_te_base = make_matrix(test_up, is_train=False, for_catboost=True)
    # --- 진단 출력: 테스트 세트 태양 파생/좌표 유효성 ---
    _cos = pd.to_numeric(X_te_base.get("solar_cos_zen_pos"), errors="coerce")
    _coord_ok = int((pd.to_numeric(test_up.get("coord1"), errors="coerce").notna() & pd.to_numeric(test_up.get("coord2"), errors="coerce").notna()).mean() * 100)
    _cos_pos = int((_cos.fillna(0) > 0).mean() * 100)
    print(f"[DIAG] test_up coord1/coord2 non-NaN ratio: {_coord_ok}%  |  solar_cos_zen_pos>0 ratio in X_te_base: {_cos_pos}%")

    # 폴드 만들기 (월 단위 블록)
    folds = make_month_folds(train_full, n_folds=args.folds)

    # 테스트 예측 앙상블 저장소
    te_preds = []

    # OOF 집계(업샘플 검증셋 기준)
    total_abs_err = 0.0
    total_count = 0
    fold_maes = []

    for fi, (tr_idx, va_idx) in enumerate(folds, start=1):
        tr_raw = train_full.iloc[tr_idx].copy()
        va_raw = train_full.iloc[va_idx].copy()

        # --- 업샘플/보간은 각 split에서 독립 수행 (누수 방지) ---
        tr_up = upsample_hourly_to_5min(tr_raw, LINEAR_COLS, STEP_COLS)
        va_up = upsample_hourly_to_5min(va_raw, LINEAR_COLS, STEP_COLS)

        # --- 피처 매트릭스 ---
        X_tr_all, y_tr_all = make_matrix(tr_up, is_train=True, for_catboost=True)
        X_va_all, y_va_all = make_matrix(va_up, is_train=True, for_catboost=True)

        # --- Clear-sky 스케일(훈련 세트에서 추정) & clearness index 타깃(B) ---
        # fold-local scale (default) vs global scale (optional)
        scale_S = global_scale_S if (global_scale_S is not None) else compute_clear_scale(tr_up)

        def build_clear(df_feat: pd.DataFrame) -> pd.Series:
            if "solar_cos_zen_pos" not in df_feat.columns:
                return pd.Series(np.zeros(len(df_feat)))
            return scale_S * pd.to_numeric(df_feat["solar_cos_zen_pos"], errors="coerce").fillna(0.0)

        G_tr = build_clear(X_tr_all)
        G_va = build_clear(X_va_all)

        # 주간만 학습(A): clearness index = nins / G_clear (G>0)
        day_tr_mask = (G_tr > 0)
        y_tr_ci = np.zeros_like(y_tr_all, dtype=float)
        y_tr_ci[day_tr_mask.values] = y_tr_all[day_tr_mask.values] / np.maximum(G_tr[day_tr_mask.values], 1e-6)

        # 입력도 주간만 사용(불필요한 노이즈 제거)
        X_tr = X_tr_all.loc[day_tr_mask].reset_index(drop=True)
        y_tr = y_tr_ci[day_tr_mask.values]

        # 검증은 전체 구간에서 예측 → 야간은 0으로 강제
        X_va = X_va_all.reset_index(drop=True)
        y_va = y_va_all

        # 검증용 clearness index 라벨 및 가중치(밤=0, 박명은 약하게)
        G_va_arr = G_va.values
        y_va_ci = np.zeros_like(y_va, dtype=float)
        day_mask_va = (G_va_arr > 0)
        y_va_ci[day_mask_va] = y_va[day_mask_va] / np.maximum(G_va_arr[day_mask_va], 1e-6)
        def make_weights_for_feat(xdf: pd.DataFrame, day_w: float, twilight_cos: float) -> np.ndarray:
            cos = pd.to_numeric(xdf.get("solar_cos_zen_pos", pd.Series(np.zeros(len(xdf)))), errors="coerce").fillna(0.0).values
            w = np.ones(len(xdf), dtype=float)
            w[cos > twilight_cos] = day_w
            w[(cos > 0) & (cos <= twilight_cos)] = 0.7 * day_w
            return w
        w_tr = make_weights_for_feat(X_tr, args.day_weight, args.twilight_cos)
        w_va = make_weights_for_feat(X_va, args.day_weight, args.twilight_cos)
        # 완전 야간은 평가 제외
        cos_va_tmp = pd.to_numeric(X_va.get("solar_cos_zen_pos"), errors="coerce").fillna(0.0).values
        w_va[cos_va_tmp <= 0] = 0.0

        # 범주형 지정
        cat_features = []
        if "pv_id" in X_tr.columns:
            cat_features.append(X_tr.columns.get_loc("pv_id"))

        # --- NaN 타깃 방어: CatBoost는 타깃 NaN을 허용하지 않음 ---
        # Train: 유효 타깃만 사용
        m_tr = np.isfinite(y_tr)
        if m_tr.sum() < len(y_tr):
            X_tr = X_tr.loc[m_tr].reset_index(drop=True)
            y_tr = y_tr[m_tr]
            w_tr = w_tr[m_tr]

        # Valid: 평가/조기종료는 유효 타깃 + 가중치>0 만 사용
        m_va = np.isfinite(y_va_ci) & (w_va > 0)
        X_va_eval = X_va.loc[m_va].reset_index(drop=True)
        y_va_eval = y_va_ci[m_va]
        w_va_eval = w_va[m_va]
        if len(y_va_eval) == 0:
            raise ValueError("Validation set has no finite targets after masking; check label construction.")

        train_pool = Pool(X_tr, y_tr, weight=w_tr, cat_features=cat_features)
        valid_pool = Pool(X_va_eval, label=y_va_eval, weight=w_va_eval, cat_features=cat_features)
        valid_pool_pred = Pool(X_va, cat_features=cat_features)

        model = CatBoostRegressor(
            iterations=args.iters,
            learning_rate=args.lr,
            depth=args.depth,
            l2_leaf_reg=args.l2_leaf_reg,
            subsample=args.subsample,
            rsm=args.rsm,
            loss_function="MAE",
            eval_metric="MAE",
            random_seed=SEED + fi,
            od_type="Iter",
            od_wait=args.od_wait,
            allow_writing_files=False,
            verbose=100,
            bagging_temperature=getattr(args, "bagging_temperature", 1.0),
            random_strength=getattr(args, "random_strength", 0.2),
            min_data_in_leaf=getattr(args, "min_data_in_leaf", 1),
        )

        # 주의: 타깃이 clearness index이므로, 검증 지표는 예측 후 복원하여 계산
        model.fit(train_pool, eval_set=valid_pool, use_best_model=True)
        best_it = model.get_best_iteration() if hasattr(model, "get_best_iteration") else None

        # 검증 예측: clearness index → nins 복원 + 규칙 기반 캘리브레이션
        ci_va = model.predict(valid_pool_pred, ntree_end=best_it) if best_it else model.predict(valid_pool_pred)
        # clearness index 합리적 범위로 클립
        ci_va = np.clip(ci_va, 0.0, 1.2)
        pred_va = ci_va * G_va.values
        cos_va = pd.to_numeric(X_va.get("solar_cos_zen_pos"), errors="coerce").fillna(0.0).values
        # 야간 0, 트와일라이트 상한
        pred_va[cos_va <= 0] = 0.0
        twilight_mask = (cos_va > 0) & (cos_va <= args.twilight_cos)
        pred_va[twilight_mask] = np.minimum(pred_va[twilight_mask], args.alpha_limit * G_va.values[twilight_mask])
        pred_va = np.clip(pred_va, 0, None)

        # For evaluation masks/diagnostics
        cos_va_all = pd.to_numeric(X_va.get("solar_cos_zen_pos"), errors="coerce").fillna(0.0).values

        # OOF 집계 (업샘플된 검증 y 와 예측 사용) — 길이/유효값 방어
        y_va_true = np.asarray(y_va_all, dtype=float).reshape(-1)
        pred_va = np.asarray(pred_va, dtype=float).reshape(-1)

        # 길이 불일치 방어: 공통 길이로 절단
        if len(y_va_true) != len(pred_va):
            min_len = min(len(y_va_true), len(pred_va))
            print(f"[WARN] length mismatch: y={len(y_va_true)} pred={len(pred_va)} → using first {min_len}")
            y_va_true = y_va_true[:min_len]
            pred_va = pred_va[:min_len]
            cos_va_all = cos_va_all[:min_len]
            w_va = w_va[:min_len]

        # NaN/Inf 제거 마스크
        base_mask = np.isfinite(y_va_true) & np.isfinite(pred_va)

        # --- 평가 모드 ---
        eval_mode = getattr(args, "val_eval_mode", "weighted_day")
        if eval_mode not in ("weighted_day", "plain_all"):
            eval_mode = "weighted_day"

        if eval_mode == "weighted_day":
            # 주간 위주 가중 MAE (야간/가중 0 제외)
            m = base_mask & (w_va > 0)
            if not np.any(m):
                print(f"[WARN] no finite values to evaluate on fold {fi} (weighted_day)")
                fold_mae = np.nan
            else:
                w = w_va[m]
                err = np.abs(y_va_true[m] - pred_va[m])
                fold_mae = float(np.sum(err * w) / np.maximum(np.sum(w), 1e-12))
                total_abs_err += float(np.sum(err * w))
                total_count   += float(np.sum(w))
        else:
            # 전체 구간 단순 MAE (LB 근사)
            m = base_mask
            if not np.any(m):
                print(f"[WARN] no finite values to evaluate on fold {fi} (plain_all)")
                fold_mae = np.nan
            else:
                err = np.abs(y_va_true[m] - pred_va[m])
                fold_mae = float(np.mean(err))
                total_abs_err += float(np.sum(err))
                total_count   += int(m.sum())

        # 구간별(낮/박명/밤) MAE 진단은 항상 출력 (가중치 없이)
        try:
            twi_cos = float(getattr(args, "eval_cos_day_threshold", 0.1))
        except Exception:
            twi_cos = 0.1
        seg_masks = {
            "day(cos>%.2f)" % twi_cos: base_mask & (cos_va_all > twi_cos),
            "twilight(0<cos<=%.2f)" % twi_cos: base_mask & ((cos_va_all > 0) & (cos_va_all <= twi_cos)),
            "night(cos<=0)": base_mask & (cos_va_all <= 0),
        }
        seg_msgs = []
        for seg_name, seg_m in seg_masks.items():
            if np.any(seg_m):
                seg_mae = float(np.mean(np.abs(y_va_true[seg_m] - pred_va[seg_m])))
            else:
                seg_mae = float("nan")
            seg_msgs.append(f"{seg_name}: {seg_mae:.3f}")
        print("[VAL] segment MAE → " + " | ".join(seg_msgs))

        # 추가: 항상 plain_all MAE도 진단 (LB 근사 확인용)
        if np.any(base_mask):
            plain_all_err = np.abs(y_va_true[base_mask] - pred_va[base_mask])
            fold_mae_plain_all = float(np.mean(plain_all_err))
        else:
            fold_mae_plain_all = float("nan")

        fold_maes.append(fold_mae)
        print(f"[Fold {fi}/{args.folds}] MAE({eval_mode})={fold_mae:.5f} | MAE(plain_all)={fold_mae_plain_all:.5f}")

        # 테스트 예측 (fold 스케일 사용)
        G_te = scale_S * pd.to_numeric(X_te_base.get("solar_cos_zen_pos"), errors="coerce").fillna(0.0).values
        te_pool = Pool(X_te_base, cat_features=cat_features)
        ci_te = model.predict(te_pool, ntree_end=best_it) if best_it else model.predict(te_pool)
        # clearness index 합리적 범위로 클립
        ci_te = np.clip(ci_te, 0.0, 1.2)
        pred_te = ci_te * G_te
        cos_te = pd.to_numeric(X_te_base.get("solar_cos_zen_pos"), errors="coerce").fillna(0.0).values
        pred_te[cos_te <= 0] = 0.0
        twilight_te = (cos_te > 0) & (cos_te <= args.twilight_cos)
        pred_te[twilight_te] = np.minimum(pred_te[twilight_te], args.alpha_limit * G_te[twilight_te])
        pred_te = np.clip(pred_te, 0, None)
        te_preds.append(pred_te)

    # 전체 OOF 성능 (업샘플 검증셋 기준 총합)
    full_mae = (total_abs_err / max(total_count, 1))
    print(f"[OOF] Mean MAE over {args.folds} folds (mode={getattr(args, 'val_eval_mode', 'weighted_day')}): {full_mae:.5f}")
    print("Fold MAEs:", ", ".join(f"{m:.3f}" for m in fold_maes))

    # 테스트 앙상블 평균
    te_pred_mean = np.mean(np.vstack(te_preds), axis=0)

    # --- 진단: 테스트 예측의 0 비율 확인 (전체/주간) ---
    cos_te_all = pd.to_numeric(X_te_base.get("solar_cos_zen_pos"), errors="coerce").fillna(0.0).values
    zero_ratio_all = float((te_pred_mean <= 1e-12).mean())
    day_mask_diag = cos_te_all > 0.1
    zero_ratio_day = float((te_pred_mean[day_mask_diag] <= 1e-12).mean()) if day_mask_diag.any() else 0.0
    print(f"[DIAG] te_pred zeros: overall={zero_ratio_all:.3f}, daytime(cos>0.1)={zero_ratio_day:.3f}")

    # 제출 파일 작성 (자동 탐색)
    cand = [
        data_dir/"sample_submission.csv",
        data_dir/"sample_submission_v1.csv",
        data_dir/"submission_sample.csv",
    ]
    sub_path = next((p for p in cand if p.exists()), None)
    if sub_path is None:
        raise FileNotFoundError("sample_submission 파일을 찾지 못했습니다. data_dir에 sample_submission.csv가 있어야 합니다.")

    sub = pd.read_csv(sub_path)
    # time 파싱 및 tz naive 통일
    if "time" in sub.columns:
        try:
            sub["time"] = pd.to_datetime(sub["time"]).dt.tz_localize(None)
        except Exception:
            try:
                sub["time"] = pd.to_datetime(sub["time"]).dt.tz_convert(None)
            except Exception:
                sub["time"] = pd.to_datetime(sub["time"])  # as-is

    # 예측 프레임 구성: test_up(원본 dtype 유지) 기준 key + 예측
    base_time = getattr(test_up, "time", pd.Series(index=np.arange(len(te_pred_mean))))
    base_pv   = getattr(test_up, "pv_id", pd.Series(index=np.arange(len(te_pred_mean))))
    pred_frame = pd.DataFrame({
        "time": base_time.values,
        "pv_id": base_pv.values,
        "nins_pred": te_pred_mean,
    })
    if "type" in getattr(test_up, "columns", []):
        pred_frame["type"] = test_up["type"].values

    # 키 dtype 정렬: pv_id를 sub의 dtype에 맞춤 (숫자면 숫자, 그 외는 문자열)
    if "pv_id" in sub.columns and "pv_id" in pred_frame.columns:
        # sub의 pv_id가 전부 숫자로 변환 가능하면 숫자형으로 통일
        try:
            sub_pv_num = pd.to_numeric(sub["pv_id"], errors="raise")
            pred_pv_num = pd.to_numeric(pred_frame["pv_id"], errors="coerce")
            if pred_pv_num.isna().sum() == 0:
                sub["pv_id"] = sub_pv_num
                pred_frame["pv_id"] = pred_pv_num
            else:
                # 숫자 변환 불가 값이 있으면 문자열로 통일
                sub["pv_id"] = sub["pv_id"].astype(str).str.strip()
                pred_frame["pv_id"] = pred_frame["pv_id"].astype(str).str.strip()
        except Exception:
            sub["pv_id"] = sub["pv_id"].astype(str).str.strip()
            pred_frame["pv_id"] = pred_frame["pv_id"].astype(str).str.strip()

    # 키 병합으로 정확히 sample_submission 순서에 맞춰 예측 매핑
    key_cols = [c for c in ["time", "pv_id", "type"] if c in sub.columns and c in pred_frame.columns]
    if not key_cols:
        # 최소한 time, pv_id는 있어야 함
        raise KeyError("submission 매핑 키(time, pv_id[, type])가 누락되었습니다.")
    # 테스트는 업샘플링하지 않으므로, 제출 격자가 테스트보다 촘촘하면 매핑이 불가능
    try:
        sub_sorted = sub.sort_values("time").reset_index(drop=True)
        if len(sub_sorted) >= 2:
            dt_sub = (pd.to_datetime(sub_sorted.loc[1, "time"]) - pd.to_datetime(sub_sorted.loc[0, "time"]))
            # test_up time 간격 (첫 두 개로 근사)
            tu_sorted = test_up.sort_values("time").reset_index(drop=True)
            if len(tu_sorted) >= 2:
                dt_te = (pd.to_datetime(tu_sorted.loc[1, "time"]) - pd.to_datetime(tu_sorted.loc[0, "time"]))
            else:
                dt_te = None
            if pd.notna(dt_te) and pd.notna(dt_sub) and dt_sub < dt_te:
                raise RuntimeError(
                    "현재 설정은 테스트 업샘플링을 금지합니다. 그러나 sample_submission의 시간 격자가 더 촘촘(예: 5분)하여 키 매핑이 불가능합니다. "
                    "1) 제출 격자를 테스트 해상도에 맞춘 샘플을 사용하거나, 2) 정책을 변경해 테스트 업샘플을 허용해야 합니다."
                )
    except Exception:
        pass

    merged = sub.copy()
    merged = merged.merge(pred_frame[key_cols + ["nins_pred"]], on=key_cols, how="left", validate="one_to_one")

    # 누락 체크 및 길이 검증
    miss = merged["nins_pred"].isna().sum()
    print(f"[INFO] submission match: matched={len(merged) - miss} / total={len(merged)} (missing={miss})")
    if miss > 0:
        print(f"[WARN] submission rows with missing prediction: {miss}")
        # 안전 차선: 결측은 0으로 대체 (야간/결측)
        merged["nins_pred"] = merged["nins_pred"].fillna(0.0)

    if len(merged) != len(sub):
        print(f"[WARN] submission length mismatch: sub={len(sub)} merged={len(merged)}")

    sub_out = merged.copy()
    sub_out["nins"] = pd.to_numeric(sub_out["nins_pred"], errors="coerce").fillna(0.0)
    sub_out = sub_out.drop(columns=[c for c in ["nins_pred"] if c in sub_out.columns])

    # ===== Additional submission diagnostics =====
    try:
        # 1) 전체 분포 요약
        desc = sub_out["nins"].describe(percentiles=[0.01,0.05,0.25,0.5,0.75,0.95,0.99])
        print("[STAT] submission nins describe:\n", desc.to_string())

        # 2) 낮/밤 분포 요약 (cos join)
        tmp_pred = pred_frame[key_cols + ["nins_pred"]].copy()
        tmp_pred = tmp_pred.merge(X_te_base[["solar_cos_zen_pos"]].reset_index(drop=True), left_index=True, right_index=True, how="left")
        tmp_pred["is_day"] = (pd.to_numeric(tmp_pred["solar_cos_zen_pos"], errors="coerce").fillna(0.0) > 0.1).astype(int)
        day_desc = tmp_pred.loc[tmp_pred["is_day"]==1, "nins_pred"].describe()
        night_desc = tmp_pred.loc[tmp_pred["is_day"]==0, "nins_pred"].describe()
        print("[STAT] daytime nins_pred describe:\n", day_desc.to_string())
        print("[STAT] nighttime nins_pred describe:\n", night_desc.to_string())

        # 3) 스케일 진단: fold별 G_te 통계
        print("[STAT] G_te scale by fold (mean,max) → 과도 축소 여부 점검")
        cos_arr = pd.to_numeric(X_te_base.get("solar_cos_zen_pos"), errors="coerce").fillna(0.0).values
        for i, pred in enumerate(te_preds, start=1):
            # pred = ci * (scale_S_i * cos)
            # 진짜 ci를 복원하려면 fold별 scale_S가 필요하지만, 여기서는 pred/(cos)로 보면 scale_S가 곱해져서 부정확.
            # 대신 pred/(pred/ci) = ci. 아래는 근사치로 pred / (cos * median_scale_S) 사용.
            # 더 정확히 보기 위해 fold 스케일을 추정: ci_hat_raw = pred / max(cos,eps)
            eps = 1e-12
            ci_hat_raw = pred / np.maximum(cos_arr, eps)
            # fold 스케일 대략치 = ci_hat_raw의 상위 98% 백분위(맑은 하늘 근사)
            scale_hat = float(np.nanpercentile(ci_hat_raw, 98))
            ci_hat = ci_hat_raw / max(scale_hat, 1e-6)
            print(f"  - fold {i}: scale_hat≈{scale_hat:.3f}, ci_hat mean≈{np.nanmean(ci_hat):.3f}, 95p≈{np.nanpercentile(ci_hat,95):.3f}")

        # 4) 값 범위 sanity check
        over_2000 = (sub_out["nins"] > 2000).mean()
        under_1 = (sub_out["nins"] < 1e-3).mean()
        print(f"[STAT] nins >2000 ratio={over_2000:.4f}, <1e-3 ratio={under_1:.4f}")
    except Exception as e:
        print(f"[WARN] diagnostic summary failed: {e}")

    out_path = Path(args.out)
    sub_out.to_csv(out_path, index=False)
    print(f"Saved submission: {out_path.resolve()}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", type=str, default="./OIBC_2025_DATA")
    p.add_argument("--valid_ratio", type=float, default=0.10)
    p.add_argument("--iters", type=int, default=4000)
    p.add_argument("--lr", type=float, default=0.03)
    p.add_argument("--depth", type=int, default=8)
    p.add_argument("--l2_leaf_reg", type=float, default=3.0)
    p.add_argument("--subsample", type=float, default=0.7)
    p.add_argument("--rsm", type=float, default=0.8)  # column sampling
    p.add_argument("--od_wait", type=int, default=200)
    p.add_argument("--day_weight", type=float, default=1.0)
    p.add_argument("--out", type=str, default="submission_catboost.csv")

    p.add_argument("--folds", type=int, default=3)
    p.add_argument("--twilight_cos", type=float, default=0.02, help="cos(zenith) 기준 박명 구간")
    p.add_argument("--alpha_limit", type=float, default=0.8, help="박명 상한 배수")
    p.add_argument("--bagging_temperature", type=float, default=1.0)
    p.add_argument("--random_strength", type=float, default=0.2)
    p.add_argument("--min_data_in_leaf", type=int, default=1)

    p.add_argument("--val_eval_mode", type=str, choices=["weighted_day", "plain_all"], default="plain_all", help="Validation MAE mode: weighted_day uses solar weights(>0 only); plain_all is unweighted over all rows (LB 근사)")
    p.add_argument("--global_scale", action="store_true", help="Use one global clear-sky scale from full train for all folds")
    p.add_argument("--eval_cos_day_threshold", type=float, default=0.1, help="Day-vs-twilight split threshold for diagnostics (cos(zenith)>")

    args = p.parse_args()
    main(args)