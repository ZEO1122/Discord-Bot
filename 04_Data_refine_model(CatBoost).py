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
"""

import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import warnings

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


# ---- 2) 유틸 ---- #
def load_csvs(data_dir: Path):
    train = pd.read_csv(data_dir / "train.csv", parse_dates=["time"], low_memory=False)
    test  = pd.read_csv(data_dir / "test.csv",  parse_dates=["time"], low_memory=False)

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
    return df.sort_values(["pv_id","time"]).reset_index(drop=True)

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
            return gi.reset_index()
        df = df.groupby(["pv_id"], group_keys=False).apply(_fill, include_groups=False)

    df = clip_physical(df)
    df = add_features(df)
    df = add_solar_features(df)

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


# ---- 3) 메인 파이프라인 ---- #
def main(args):
    data_dir = Path(args.data_dir)
    train, test = load_csvs(data_dir)

    # 누수 위험/불필요 컬럼 제거
    for c in DROP_COLS:
        if c in train.columns: train = train.drop(columns=[c])
        if c in test.columns:  test  = test.drop(columns=[c])

    # 정렬 및 타깃 유효성
    train = sort_by_key(train)
    test  = sort_by_key(test)

    # 컬럼/타깃 중복 최종 방어
    train = _remove_dup_columns(train)
    train = _fix_dup_target(train, target="nins")
    if "nins" not in train.columns:
        raise KeyError("train.csv에 'nins' 컬럼이 없습니다. 데이터 경로를 확인하세요.")
    # 불리언 인덱싱 시 DataFrame이 되지 않도록 단일 시리즈 보장
    nins_ser = pd.to_numeric(train["nins"], errors="coerce")
    train = train[nins_ser.notna()].copy()
    
    # 시간 기반 분할 (먼저 나누고 각 split 내부에서 업샘플/보간)
    tr_df, va_df = time_split(train, valid_ratio=args.valid_ratio)
    tr_df = upsample_hourly_to_5min(tr_df, LINEAR_COLS, STEP_COLS)
    va_df = upsample_hourly_to_5min(va_df, LINEAR_COLS, STEP_COLS)
    test  = upsample_hourly_to_5min(test,  LINEAR_COLS, STEP_COLS)

    # 피처 매트릭스 (CatBoost 전용)
    X_tr, y_tr = make_matrix(tr_df, is_train=True, for_catboost=True)
    X_va, y_va = make_matrix(va_df, is_train=True, for_catboost=True)
    X_te       = make_matrix(test,  is_train=False, for_catboost=True)

    # 낮/밤 가중치
    def make_weights(xdf: pd.DataFrame, day_w: float):
        if "daylight_flag" in xdf.columns:
            return np.where(xdf["daylight_flag"].values == 1, day_w, 1.0)
        return np.ones(len(xdf), dtype=float)
    w_tr = make_weights(X_tr, args.day_weight)

    # 범주형 컬럼 인덱스
    cat_features = []
    if "pv_id" in X_tr.columns:
        cat_features.append(X_tr.columns.get_loc("pv_id"))

    train_pool = Pool(X_tr, y_tr, weight=w_tr, cat_features=cat_features)
    valid_pool = Pool(X_va, y_va, cat_features=cat_features)

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
    best_it = model.get_best_iteration() if hasattr(model, "get_best_iteration") else None

    va_pred = model.predict(valid_pool, ntree_end=best_it) if best_it else model.predict(valid_pool)
    vmae = mae(y_va, va_pred)
    print(f"[CatBoost] Valid MAE: {vmae:.5f} | per 200 units: {vmae/200.0:.5f}")

    te_pool = Pool(X_te, cat_features=cat_features)
    te_pred = model.predict(te_pool, ntree_end=best_it) if best_it else model.predict(te_pool)

    # 샘플 제출 양식 자동 탐색
    cand = [
        data_dir/"submission_sample.csv",
    ]
    sub_path = next((p for p in cand if p.exists()), None)
    if sub_path is None:
        raise FileNotFoundError("sample_submission 파일을 찾지 못했습니다. data_dir에 sample_submission.csv가 있어야 합니다.")

    sub = pd.read_csv(sub_path)
    # test 정렬키와 정렬 순서를 맞춰서 주입
    te_key = test[["time","pv_id"]].copy()
    te_key["__row__"] = np.arange(len(te_key))
    out = te_key[["__row__"]].copy()
    out["nins"] = te_pred
    out = out.sort_values("__row__")
    sub["nins"] = out["nins"].values

    out_path = Path(args.out)
    sub.to_csv(out_path, index=False)
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
    p.add_argument("--day_weight", type=float, default=3.0)
    p.add_argument("--out", type=str, default="submission_catboost.csv")
    args = p.parse_args()
    main(args)