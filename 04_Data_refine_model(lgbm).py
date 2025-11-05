import numpy as np
import pandas as pd
from pathlib import Path
import warnings

# 현재 pandas 버전에서는 그룹핑하는 기준 컬럼 데이터 또한 포함하여 그룹핑함
warnings.filterwarnings(
    "ignore",
    message=(
        "DataFrameGroupBy.apply operated on the grouping columns. This behavior is deprecated"
    ),
    category=FutureWarning,
)

# LightGBM only 라이브러리 미설치시 오류
try:
    from lightgbm import LGBMRegressor, early_stopping, log_evaluation, reset_parameter
except Exception:
    raise ImportError("lightgbm이 설치되어 있지 않습니다. `conda install -c conda-forge lightgbm` 로 설치하세요.")

SEED = 42
np.random.seed(SEED)

# === Ablation switches (restore baseline, then add features stepwise) ===
USE_SOLAR = True              # 태양 위치 파생 사용 여부
USE_INTERACTIONS = False      # 상호작용 파생 사용 여부
USE_DAYLIGHT_WEIGHTS = False  # 낮/밤 가중치 (기본 OFF로 베이스라인 복구)
USE_MONOTONE = False          # 단조 제약 (기본 OFF)

# 시간에 따라 연속적으로 변하는 값
LINEAR_COLS = [ 
    "cloud_a","cloud_b","ceiling","uv_idx","vis","rel_hum","humidity",
    "dew_point","pressure","ground_press","temp_a","temp_b","appr_temp",
    "real_feel_temp","real_feel_temp_shade","wind_spd_a","wind_spd_b",
    "wind_gust_spd"
]

#계단형(시간동안 값이 유지되는) 값
STEP_COLS   = ["precip_1h","rain","snow","wind_dir_a","wind_dir_b"]

DROP_COLS   = ["energy"]  # 누수/테스트 미존재


def load_csv():
    train = pd.read_csv("./OIBC_2025_DATA/train.csv", parse_dates=["time"], low_memory=False)
    test  = pd.read_csv("./OIBC_2025_DATA/test.csv",  parse_dates=["time"], low_memory=False)
    # 안전: 공통 컬럼만 사용
    common_cols = [c for c in train.columns if c in test.columns or c == "nins"]
    train = train[common_cols + (["nins"] if "nins" not in common_cols else [])]
    return train, test


def sort_idx(df):
    return df.sort_values(["pv_id","time"]).reset_index(drop=True)


def upsample_hourly_to_5min(df, cols_linear, cols_step):
    """pv_id별 5분 그리드로 리샘플 + 시간보간/전파"""
    outs = []
    for pid, g in df.groupby("pv_id", sort=False):
        g = g.set_index("time").sort_index()
        idx5 = pd.date_range(g.index.min(), g.index.max(), freq="5min")
        g = g.reindex(idx5)
        # 계단형은 전파, 연속형은 선형보간
        inter_lin = [c for c in cols_linear if c in g.columns]
        inter_stp = [c for c in cols_step   if c in g.columns]
        if inter_lin:
            g[inter_lin] = g[inter_lin].interpolate(method="time", limit=12, limit_direction="both")
        if inter_stp:
            g[inter_stp] = g[inter_stp].ffill().bfill()
        g["pv_id"] = pid
        g = g.reset_index().rename(columns={"index":"time"})
        outs.append(g)
    out = pd.concat(outs, axis=0, ignore_index=True)
    return out


def physical_clip(df):
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


def add_features(df):
    # 구름 평균
    if "cloud_a" in df.columns and "cloud_b" in df.columns:
        df["cloud_mean"] = ((df["cloud_a"].astype(float)) + (df["cloud_b"].astype(float))) / 2.0
        df["cloud_mean"] = df["cloud_mean"].clip(0,1)
    # 강수 플래그
    if "precip_1h" in df.columns:
        df["precip_flag"] = (df["precip_1h"].fillna(0) > 0).astype(int)
    if "rain" in df.columns:
        df["rain_flag"] = (df["rain"].fillna(0) > 0).astype(int)
    if "snow" in df.columns:
        df["snow_flag"] = (df["snow"].fillna(0) > 0).astype(int)
    # 풍향 → sin/cos
    for c in ["wind_dir_a","wind_dir_b"]:
        if c in df.columns:
            rad = np.deg2rad(df[c].astype(float) % 360)
            df[c+"_sin"] = np.sin(rad)
            df[c+"_cos"] = np.cos(rad)
    # 돌풍-평균풍
    if "wind_gust_spd" in df.columns and "wind_spd_a" in df.columns:
        df["gust_delta_a"] = (df["wind_gust_spd"] - df["wind_spd_a"]).clip(lower=0)
    if "wind_gust_spd" in df.columns and "wind_spd_b" in df.columns:
        df["gust_delta_b"] = (df["wind_gust_spd"] - df["wind_spd_b"]).clip(lower=0)
    # 시간 파생
    df["hour"] = df["time"].dt.hour
    df["doy"]  = df["time"].dt.dayofyear
    df["hour_sin"] = np.sin(2*np.pi*df["hour"]/24)
    df["hour_cos"] = np.cos(2*np.pi*df["hour"]/24)
    return df


def add_solar_features(df):
    """시간/위경도 기반 태양 위치 파생(외부데이터 미사용)
    coord1/2는 각각 위도, 경도(도 단위)로 가정
    """
    # 위경도 존재 여부 확인
    if "coord1" not in df.columns or "coord2" not in df.columns:
        # 필요 컬럼 없으면 기본 더미만 반환
        df["solar_elev"] = 0.0
        df["solar_cos_zen_pos"] = 0.0
        df["daylight_flag"] = 0
        df["doy_sin"] = np.sin(2*np.pi*df["time"].dt.dayofyear/365.0)
        df["doy_cos"] = np.cos(2*np.pi*df["time"].dt.dayofyear/365.0)
        return df

    # 숫자 캐스팅
    lat = np.deg2rad(pd.to_numeric(df["coord1"], errors="coerce"))
    lon_deg = pd.to_numeric(df["coord2"], errors="coerce")
    lon = np.deg2rad(lon_deg)

    doy = df["time"].dt.dayofyear
    hour = df["time"].dt.hour + df["time"].dt.minute/60.0

    # 방정식의 시간 (분) - 간이식
    B = 2*np.pi*(doy-81)/364.0
    EoT = 9.87*np.sin(2*B) - 7.53*np.cos(B) - 1.5*np.sin(B)  # 분

    # 표준경도 근사 및 시간보정 (분)
    LSTM = 15*np.round(lon_deg/15.0)
    TC = 4*(lon_deg - LSTM) + EoT

    # 현지 태양시(시간)
    LST = hour + TC/60.0

    # 시각차(Hour Angle)
    HRA = np.deg2rad(15*(LST-12.0))

    # 태양 적위(간이식)
    decl = np.deg2rad(23.45)*np.sin(2*np.pi*(284 + doy)/365.0)

    # 천정각으로부터 고도 계산
    cos_zen = np.sin(lat)*np.sin(decl) + np.cos(lat)*np.cos(decl)*np.cos(HRA)
    cos_zen = np.clip(cos_zen, -1.0, 1.0)
    zenith = np.arccos(cos_zen)
    elev = np.pi/2 - zenith

    # 파생 추가
    df["solar_elev"] = elev
    df["solar_cos_zen_pos"] = np.clip(np.cos(zenith), 0, None)
    df["daylight_flag"] = (df["solar_elev"] > 0).astype(int)
    df["doy_sin"] = np.sin(2*np.pi*doy/365.0)
    df["doy_cos"] = np.cos(2*np.pi*doy/365.0)
    return df


def make_feature_matrix(df, is_train=True):
    # 결측 플래그(원천 결측 신호 활용)
    for c in (LINEAR_COLS + STEP_COLS):
        if c in df.columns:
            df[f"is_imputed_{c}"] = df[c].isna().astype(int)

    # 실제로 존재하는 컬럼만 대상으로 선정
    inter_lin = [c for c in LINEAR_COLS if c in df.columns]
    inter_stp = [c for c in STEP_COLS if c in df.columns]

    if inter_lin or inter_stp:
        def _fill_group(g):
            gi = g.set_index("time").sort_index()
            if inter_lin:
                gi[inter_lin] = gi[inter_lin].interpolate("time", limit=12, limit_direction="both").ffill().bfill()
            if inter_stp:
                gi[inter_stp] = gi[inter_stp].ffill().bfill()
            gi = gi.reset_index()
            return gi
        df = df.groupby(["pv_id"], group_keys=False).apply(_fill_group, include_groups=False)

    df = add_features(df)
    if USE_SOLAR:
        df = add_solar_features(df)

    # 물리 상호작용 파생 (옵션)
    if USE_INTERACTIONS:
        if "cloud_mean" in df.columns and "uv_idx" in df.columns:
            df["cloud_uv_inter"] = df["cloud_mean"] * df["uv_idx"]
        if "cloud_mean" in df.columns and "solar_cos_zen_pos" in df.columns:
            df["cloud_sun_inter"] = df["cloud_mean"] * df["solar_cos_zen_pos"]

    # 대표 피처 선정
    chosen = [
        # 구름/복사 관련
        "cloud_mean", "uv_idx", "vis",
        # 기압/온습도
        "pressure", "temp_a", "rel_hum",
        # 바람
        "wind_spd_a", "wind_dir_a_sin", "wind_dir_a_cos", "gust_delta_a",
        # 강수 플래그
        "precip_flag", "rain_flag", "snow_flag",
        # 시간/연주기
        "hour_sin", "hour_cos", "doy",
        # 위치 및 개체 식별
        "coord1", "coord2", "pv_id",
    ]
    if USE_SOLAR:
        chosen += ["doy_sin", "doy_cos", "solar_cos_zen_pos", "daylight_flag"]
    if USE_INTERACTIONS:
        chosen += ["cloud_uv_inter", "cloud_sun_inter"]

    X = df[[c for c in chosen if c in df.columns]].copy()

    # 수치형 캐스팅 & pv_id 인코딩
    for c in X.columns:
        if c not in ["pv_id"]:
            X[c] = pd.to_numeric(X[c], errors="coerce")
    if "pv_id" in X.columns:
        X["pv_id"] = X["pv_id"].astype("category").cat.codes

    if is_train and "nins" in df.columns:
        y = df["nins"].astype(float).values
        return X, y
    else:
        return X


def time_based_split(df, valid_ratio=0.1):
    ts = df["time"].sort_values()
    cut = ts.quantile(1.0 - valid_ratio)
    tr = df[df["time"] < cut].copy()
    va = df[df["time"] >= cut].copy()
    return tr, va



def mae(a, b):
    return float(np.mean(np.abs(a - b)))


def compute_regression_metrics(y_true, y_pred):
    """Return dict: MAE, NMAPE, MSE, MSLE, RMSLE"""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    # Safety clip for log metrics
    y_true_clip = np.clip(y_true, 0.0, None)
    y_pred_clip = np.clip(y_pred, 0.0, None)

    mae_v = float(np.mean(np.abs(y_true - y_pred)))
    denom = float(max(np.mean(y_true_clip), 1.0))
    nmape_v = float(mae_v / denom)
    mse_v = float(np.mean((y_true - y_pred) ** 2))
    # MSLE / RMSLE
    log_true = np.log1p(y_true_clip)
    log_pred = np.log1p(y_pred_clip)
    msle_v = float(np.mean((log_true - log_pred) ** 2))
    rmsle_v = float(np.sqrt(msle_v))
    return {
        "MAE": mae_v,
        "NMAPE": nmape_v,
        "MSE": mse_v,
        "MSLE": msle_v,
        "RMSLE": rmsle_v,
    }


def train_and_predict():
    train, test = load_csv()
    # 안전 제거
    for c in DROP_COLS:
        if c in train.columns:
            train = train.drop(columns=[c])
        if c in test.columns:
            test  = test.drop(columns=[c])

    train = sort_idx(train)
    test  = sort_idx(test)

    # 타깃 없는 행 제거
    if "nins" in train.columns:
        train = train[~train["nins"].isna()].copy()

    # 시간 기반 분할 (누수 방지: 분할 먼저)
    tr_df, va_df = time_based_split(train, valid_ratio=0.1)

    # 각 split 내부에서만 1시간 → 5분 업샘플/보간
    tr_df = upsample_hourly_to_5min(tr_df, LINEAR_COLS, STEP_COLS)
    va_df = upsample_hourly_to_5min(va_df, LINEAR_COLS, STEP_COLS)
    test  = upsample_hourly_to_5min(test,  LINEAR_COLS, STEP_COLS)

    # 피처 매트릭스
    X_tr, y_tr = make_feature_matrix(tr_df, is_train=True)
    X_va, y_va = make_feature_matrix(va_df, is_train=True)
    X_te = make_feature_matrix(test, is_train=False)

    # 낮/밤 가중치 (옵션)
    if USE_DAYLIGHT_WEIGHTS:
        def _weights(xdf):
            if "daylight_flag" in xdf.columns:
                return np.where(xdf["daylight_flag"] == 1, 3.0, 1.0)
            return np.ones(len(xdf), dtype=float)
        w_tr = _weights(X_tr)
    else:
        w_tr = None

    # Step-decay learning rate (remedy #4)
    def _lr(cur_iter: int) -> float:
        base = 0.015
        if cur_iter < 1500:
            return base
        elif cur_iter < 3000:
            return base * 0.67
        else:
            return base * 0.5

    if USE_MONOTONE:
        mono_map = {
            "cloud_mean": -1,
            "uv_idx": +1,
            "rel_hum": -1,
            "precip_flag": -1,
            "rain_flag": -1,
            "snow_flag": -1,
            "solar_cos_zen_pos": +1,
            "daylight_flag": +1,
            "temp_a": +1,
        }
        mono_list = [mono_map.get(c, 0) for c in X_tr.columns]
    else:
        mono_list = None

    model = LGBMRegressor(
        n_estimators=4000,
        learning_rate=0.015,
        max_depth=6,
        num_leaves=63,
        min_child_samples=150,
        subsample=0.7, subsample_freq=1,
        colsample_bytree=0.6,
        lambda_l1=1.0, lambda_l2=8.0,
        objective="regression_l1",
        random_state=SEED, n_jobs=-1,
        verbosity=-1,
        **({"monotone_constraints": mono_list} if USE_MONOTONE else {}),
    )

    fit_kwargs = dict(
        X=X_tr, y=y_tr,
        eval_set=[(X_va, y_va)],
        eval_metric="mae",
        callbacks=[
            early_stopping(stopping_rounds=300),
            log_evaluation(period=100),
            reset_parameter(learning_rate=_lr),
        ],
    )
    if w_tr is not None:
        fit_kwargs["sample_weight"] = w_tr
    model.fit(**fit_kwargs)

    _best_it = getattr(model, "best_iteration_", None)
    va_pred = model.predict(X_va, num_iteration=_best_it) if _best_it else model.predict(X_va)
    # ---- Compute & print metrics (Train / Validation) ----
    tr_pred = model.predict(X_tr, num_iteration=_best_it) if _best_it else model.predict(X_tr)
    tr_metrics = compute_regression_metrics(y_tr, tr_pred)
    va_metrics = compute_regression_metrics(y_va, va_pred)

    def _pfx(d):
        return (f"  - MAE: {d['MAE']:.5f}\n"
                f"  - NMAPE: {d['NMAPE']:.5f}\n"
                f"  - MSE: {d['MSE']:.5f}\n"
                f"  - MSLE: {d['MSLE']:.5f}\n"
                f"  - RMSLE: {d['RMSLE']:.5f}")

    print("[LGBM] Train Metrics", flush=True)
    print(_pfx(tr_metrics), flush=True)
    print("[LGBM] Validation Metrics", flush=True)
    print(_pfx(va_metrics), flush=True)

    te_pred = model.predict(X_te, num_iteration=_best_it) if _best_it else model.predict(X_te)

    # 제출 파일 생성
    sub = pd.read_csv("./OIBC_2025_DATA/submission_sample.csv")
    te_key = test[["time","pv_id"]].copy()
    te_key["__row__"] = np.arange(len(te_key))
    out = te_key[["__row__"]].copy()
    out["nins"] = te_pred
    out = out.sort_values("__row__")
    sub["nins"] = out["nins"].values
    out_name = "submission_lgbm_v1.csv"
    sub.to_csv(out_name, index=False)
    print(f"Saved: {out_name}")


if __name__ == "__main__":
    train_and_predict()
