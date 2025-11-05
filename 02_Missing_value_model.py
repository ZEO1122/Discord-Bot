# per_feature_models.py (예시)
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from lightgbm import LGBMRegressor, early_stopping
import joblib

# 설정
MIN_COVERAGE_PCT = 0.05   # 전체 행의 최소 관측 비율 (예: 5%)
MIN_ABS_SAMPLES = 50000   # 또는 절대 샘플 수 기준
RANDOM_STATE = 42

def feature_coverage_stats(df, features):
    n_total = len(df)
    stats = []
    for f in features:
        cnt = df[f].notna().sum()
        stats.append((f, cnt, cnt / n_total))
    return pd.DataFrame(stats, columns=['feature','non_null_count','coverage'])

# 1) 데이터 준비 (train, test는 미리 읽어둔 상태)
# train, test = pd.read_csv(...), pd.read_csv(...)
# train['time'] = pd.to_datetime(train['time'])  # 이미 처리되었다 가정

# CSV 파일 경로 설정 ( 본인 환경에 맞게 수정)
train_path = './OIBC_2025_DATA/train.csv'
test_path =  './OIBC_2025_DATA/test.csv'
submission_path =  './OIBC_2025_DATA/submission_sample.csv'

# 데이터 읽기
train = pd.read_csv(train_path)
test = pd.read_csv(test_path)
submission = pd.read_csv(submission_path)

train['time'] = pd.to_datetime(train['time'])
test['time'] = pd.to_datetime(test['time'])

base_features = [c for c in train.columns if c not in ['time','pv_id','type','nins','coord1','coord2','energy']]

# 2) 피처 커버리지 확인
cov_df = feature_coverage_stats(train, base_features).sort_values('coverage', ascending=False)
print(cov_df.head(30))

# 3) 글로벌(기본) 모델 — fallback
# 결측 플래그 추가
train_glob = train.copy()
for c in base_features:
    train_glob[c + '_isna'] = train_glob[c].isna().astype('int8')

glob_feats = [c for c in train_glob.columns if c not in ['time','pv_id','type','nins','coord1','coord2','energy']]
X = train_glob[glob_feats]
y = train_glob['nins']

# 시간-기반 샘플링/검증이 권장되지만 간단히 분할 예시
X_tr, X_val, y_tr, y_val = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)
glob_model = LGBMRegressor(n_estimators=500, random_state=RANDOM_STATE)
glob_model.fit(
    X_tr, y_tr,
    eval_set=[(X_val, y_val)],
    callbacks=[early_stopping(stopping_rounds=50)]
)
val_pred = glob_model.predict(X_val)
print("Global MAE:", mean_absolute_error(y_val, val_pred))
joblib.dump(glob_model, "model_global.pkl")

# 4) 피처별 특화 모델 학습 (커버리지 기준 만족하는 피처만)
feature_models = {}  # 저장: {feature: (model, val_mae)}
for _, row in cov_df.iterrows():
    f, cnt, pct = row['feature'], row['non_null_count'], row['coverage']
    if pct < MIN_COVERAGE_PCT and cnt < MIN_ABS_SAMPLES:
        continue  # 수량/비율 기준 미달 -> 건너뜀

    # 이 피처가 존재하는 행만 사용 (그리고 다른 피처 결측 때문에 행이 더 줄면 그건 인정)
    df_sub = train[train[f].notna()].copy()
    if len(df_sub) < 1000:
        continue

    # 피처셋: 글로벌 피처 + (원하면) 해당 피처 우선적 포함
    feats_sub = [c for c in base_features if c in df_sub.columns]  # 기본적으로 같은 피처들 사용
    # 결측플래그도 추가
    for c in feats_sub:
        df_sub[c + '_isna'] = df_sub[c].isna().astype('int8')
    Xs = df_sub[[c for c in df_sub.columns if c not in ['time','pv_id','type','nins','coord1','coord2','energy']]]
    ys = df_sub['nins']

    Xtr, Xv, ytr, yv = train_test_split(Xs, ys, test_size=0.2, random_state=RANDOM_STATE)
    m = LGBMRegressor(n_estimators=500, random_state=RANDOM_STATE)
    m.fit(
        Xtr, ytr,
        eval_set=[(Xv, yv)],
        callbacks=[early_stopping(stopping_rounds=50)]
    )
    mae = mean_absolute_error(yv, m.predict(Xv))
    print(f"Feature model '{f}': samples={len(df_sub)}, val_mae={mae:.4f}")
    feature_models[f] = (m, mae)
    joblib.dump(m, f"model_feat_{f}.pkl")

# 5) 테스트 예측 병합: 특화 모델 예측(해당 피처 존재시) + 글로벌 예측(없을 때)
# 먼저 글로벌 예측
test_glob = test.copy()
for c in base_features:
    test_glob[c + '_isna'] = test_glob[c].isna().astype('int8')
X_test_glob = test_glob[[c for c in test_glob.columns if c not in ['time','pv_id','type','nins','coord1','coord2','energy']]]
pred_glob = glob_model.predict(X_test_glob)

# 특화 모델 예측 모음 (각 모델이 적용 가능한 행에만)
preds_stack = []  # list of (pred_array, mask, weight)
for f, (m, mae) in feature_models.items():
    mask = test[f].notna().values
    if mask.sum() == 0:
        continue
    # 동일한 피처 전처리: 결측플래그 생성 (위에서 만든 이름과 일치해야 함)
    test_sub = test_glob.copy()
    X_test_sub = test_sub[[c for c in test_sub.columns if c not in ['time','pv_id','type','nins','coord1','coord2','energy']]]
    pred_sub = m.predict(X_test_sub)
    weight = 1.0 / (mae + 1e-8)  # 성능 기반 가중치
    preds_stack.append((pred_sub, mask, weight))

# 최종 병합: 가중평균 (특화 모델이 하나라도 있으면 가중합, 없으면 글로벌)
final_pred = pred_glob.copy()
if preds_stack:
    # 가중합 numerator/denominator
    num = np.zeros_like(final_pred, dtype=float)
    den = np.zeros_like(final_pred, dtype=float)
    for pred_arr, mask, w in preds_stack:
        num[mask] += pred_arr[mask] * w
        den[mask] += w
    # where den>0, override with weighted average; else keep global
    has_spec = den > 0
    final_pred[has_spec] = num[has_spec] / den[has_spec]

# 음수 방지
final_pred[final_pred < 0] = 0
submission['nins'] = final_pred
submission.to_csv('submission_per_feature_ensemble.csv', index=False)