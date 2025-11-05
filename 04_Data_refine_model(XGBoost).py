# -*- coding: utf-8 -*-
# Usage:
#   python 04_xgb_baseline.py

import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings(
    "ignore",
    message=(
        "DataFrameGroupBy.apply operated on the grouping columns. This behavior is deprecated"
    ),
    category=FutureWarning,
)

try:
    import xgboost as xgb
    from xgboost import XGBRegressor
except Exception:
    raise ImportError("xgboost가 설치되어 있지 않습니다. `conda install -c conda-forge xgboost` 로 설치하세요.")

SEED = 42
np.random.seed(SEED)

LINEAR_COLS = [
    "cloud_a","cloud_b","ceiling","uv_idx","vis","rel_hum","humidity",
    "dew_point","pressure","ground_press","temp_a","temp_b","appr_temp",
    "real_feel_temp","real_feel_temp_shade","wind_spd_a","wind_spd_b",
    "wind_gust_spd"
]
STEP_COLS   = ["precip_1h","rain","snow","wind_dir_a","wind_dir_b"]

DROP_COLS   = ["energy"]  # 누수/테스트 미존재

def load_csv():
    def _safe_read_csv(path):
        # 1) 기본: C 엔진 시도
        try:
            return pd.read_csv(path, parse_dates=["time"], low_memory=False)
        except pd.errors.ParserError as e:
            print(f"[WARN] ParserError on {path}: {e}. Trying engine='python' with on_bad_lines='skip' ...")
            # 2) 파이썬 엔진 + 문제 라인 스킵
            return pd.read_csv(
                path,
                parse_dates=["time"],
                low_memory=False,
                engine="python",
                on_bad_lines="skip",
            )
        except UnicodeDecodeError as e:
            print(f"[WARN] UnicodeDecodeError on {path}: {e}. Trying utf-8-sig ...")
            try:
                return pd.read_csv(path, parse_dates=["time"], low_memory=False, encoding="utf-8-sig")
            except Exception as e2:
                print(f"[WARN] Fallback failed on {path}: {e2}. Trying engine='python' + errors='replace' ...")
                # 마지막 시도: engine='python' + 잘못된 문자는 치환
                return pd.read_csv(
                    path,
                    parse_dates=["time"],
                    low_memory=False,
                    engine="python",
                    encoding_errors="replace",
                )

    train_path = "./OIBC_2025_DATA/train.csv"
    test_path  = "./OIBC_2025_DATA/test.csv"

    train = _safe_read_csv(train_path)
    test  = _safe_read_csv(test_path)

    # 공통 컬럼 교집합 정리 (nins 포함)
    common_cols = [c for c in train.columns if c in test.columns or c == "nins"]
    if "nins" not in common_cols and "nins" in train.columns:
        common_cols = common_cols + ["nins"]
    train = train[common_cols]
    return train, test

def sort_idx(df):
    return df.sort_values(["pv_id","time"]).reset_index(drop=True)

def upsample_hourly_to_5min(df, cols_linear, cols_step):
    outs = []
    for pid, g in df.groupby("pv_id", sort=False):
        g = g.set_index("time").sort_index()
        idx5 = pd.date_range(g.index.min(), g.index.max(), freq="5min")
        g = g.reindex(idx5)
        inter_lin = [c for c in cols_linear if c in g.columns]
        inter_stp = [c for c in cols_step   if c in g.columns]
        if inter_lin:
            g[inter_lin] = g[inter_lin].interpolate(method="time", limit=18, limit_direction="both")
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
        "uv_idx":(0,15), "vis":(0, float("inf")),
        "pressure":(850,1100), "ground_press":(850,1100),
        "wind_spd_a":(0,float("inf")), "wind_spd_b":(0,float("inf")),
        "wind_gust_spd":(0,float("inf")),
        "precip_1h":(0,float("inf")),
        "nins":(0,float("inf")),
    }
    for c,(lo,hi) in clip_map.items():
        if c in df.columns:
            df[c] = df[c].clip(lower=lo, upper=hi)
    return df

def add_features(df):
    if "cloud_a" in df.columns and "cloud_b" in df.columns:
        df["cloud_mean"] = ((df["cloud_a"].astype(float)) + (df["cloud_b"].astype(float))) / 2.0
        df["cloud_mean"] = df["cloud_mean"].clip(0,1)
    if "precip_1h" in df.columns:
        df["precip_flag"] = (df["precip_1h"].fillna(0) > 0).astype(int)
    if "rain" in df.columns:
        df["rain_flag"] = (df["rain"].fillna(0) > 0).astype(int)
    if "snow" in df.columns:
        df["snow_flag"] = (df["snow"].fillna(0) > 0).astype(int)
    for c in ["wind_dir_a","wind_dir_b"]:
        if c in df.columns:
            rad = np.deg2rad(df[c].astype(float) % 360)
            df[c+"_sin"] = np.sin(rad)
            df[c+"_cos"] = np.cos(rad)
    if "wind_gust_spd" in df.columns and "wind_spd_a" in df.columns:
        df["gust_delta_a"] = (df["wind_gust_spd"] - df["wind_spd_a"]).clip(lower=0)
    if "wind_gust_spd" in df.columns and "wind_spd_b" in df.columns:
        df["gust_delta_b"] = (df["wind_gust_spd"] - df["wind_spd_b"]).clip(lower=0)
    df["hour"] = df["time"].dt.hour
    df["doy"]  = df["time"].dt.dayofyear
    df["hour_sin"] = np.sin(2*np.pi*df["hour"]/24)
    df["hour_cos"] = np.cos(2*np.pi*df["hour"]/24)
    return df

def make_feature_matrix(df, is_train=True):
    for c in (LINEAR_COLS + STEP_COLS):
        if c in df.columns:
            df[f"is_imputed_{c}"] = df[c].isna().astype(int)

    inter_lin = [c for c in LINEAR_COLS if c in df.columns]
    inter_stp = [c for c in STEP_COLS if c in df.columns]

    if inter_lin or inter_stp:
        def _fill_group(g):
            gi = g.set_index("time").sort_index()
            if inter_lin:
                gi[inter_lin] = gi[inter_lin].interpolate("time", limit=18, limit_direction="both").ffill().bfill()
            if inter_stp:
                gi[inter_stp] = gi[inter_stp].ffill().bfill()
            gi = gi.reset_index()
            return gi
        df = df.groupby(["pv_id"], group_keys=False).apply(_fill_group, include_groups=False)

    df = physical_clip(df)
    df = add_features(df)

    chosen = [
        "cloud_mean","uv_idx","vis","pressure","temp_a","rel_hum",
        "wind_spd_a","wind_dir_a_sin","wind_dir_a_cos",
        "gust_delta_a","precip_flag","rain_flag","snow_flag",
        "hour_sin","hour_cos","doy","pv_id"
    ]
    X = df[[c for c in chosen if c in df.columns]].copy()

    for c in X.columns:
        if c != "pv_id":
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

def train_and_predict():
    train, test = load_csv()
    for c in DROP_COLS:
        if c in train.columns: train = train.drop(columns=[c])
        if c in test.columns:  test  = test.drop(columns=[c])

    train = sort_idx(train)
    test  = sort_idx(test)

    train = upsample_hourly_to_5min(train, LINEAR_COLS, STEP_COLS)
    test  = upsample_hourly_to_5min(test,  LINEAR_COLS, STEP_COLS)

    if "nins" in train.columns:
        train = train[~train["nins"].isna()].copy()

    tr_df, va_df = time_based_split(train, valid_ratio=0.1)

    X_tr, y_tr = make_feature_matrix(tr_df, is_train=True)
    X_va, y_va = make_feature_matrix(va_df, is_train=True)
    X_te = make_feature_matrix(test, is_train=False)

    # === XGBoost (staged training: stop if MAE increases every 200 rounds) ===
    params = {
        "objective": "reg:absoluteerror",  # MAE
        "eval_metric": "mae",
        "max_depth": 8,
        "eta": 0.03,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "lambda": 1.0,
        "tree_method": "hist",
        "nthread": -1,
        "seed": SEED,
    }

    # Convert to DMatrix for native xgboost API (enables staged training)
    dtrain = xgb.DMatrix(X_tr, label=y_tr)
    dvalid = xgb.DMatrix(X_va, label=y_va)

    evals = [(dtrain, "train"), (dvalid, "valid")]

    max_rounds = 4000
    chunk = 200  # check every 200 boosting rounds
    booster = None
    best_chunk_mae = float("inf")

    rounds_done = 0
    while rounds_done < max_rounds:
        # Train additional `chunk` rounds on top of the existing booster
        booster = xgb.train(
            params,
            dtrain,
            num_boost_round=chunk,
            evals=evals,
            verbose_eval=False,
            xgb_model=booster,  # continue training
        )
        rounds_done += chunk

        # Fetch last eval result for validation MAE
        eval_hist = booster.eval(dvalid)
        # eval string format: '[]\ttrain-mae:...\tvalid-mae:...'
        try:
            valid_mae = float([part.split(":")[1] for part in eval_hist.split("\t") if part.startswith("valid-mae")][0])
        except Exception:
            # fallback parsing
            valid_mae = float(eval_hist.split("valid-mae:")[-1])

        print(f"[XGB] rounds={rounds_done:4d}  valid MAE={valid_mae:.6f}")

        # Stop if MAE increased compared to the previous 200-round checkpoint
        if valid_mae > best_chunk_mae:
            print("[EARLY STOP] Validation MAE increased vs previous 200-round checkpoint. Stopping.")
            break
        else:
            best_chunk_mae = valid_mae

    # Use the trained booster for inference
    va_pred = booster.predict(dvalid)
    orig_mae = mae(y_va, va_pred)
    scaled_mae = orig_mae / 200.0
    print(f"[XGB] Valid MAE: {orig_mae:.5f}  |  MAE per 200 units: {scaled_mae:.5f}")

    dtest = xgb.DMatrix(X_te)
    te_pred = booster.predict(dtest)

    sub = pd.read_csv("./OIBC_2025_DATA/submission_sample.csv")
    te_key = test[["time","pv_id"]].copy()
    te_key["__row__"] = np.arange(len(te_key))
    out = te_key[["__row__"]].copy()
    out["nins"] = te_pred
    out = out.sort_values("__row__")
    sub["nins"] = out["nins"].values
    out_name = "submission_xgb.csv"
    sub.to_csv(out_name, index=False)
    print(f"Saved: {out_name}")

if __name__ == "__main__":
    train_and_predict()