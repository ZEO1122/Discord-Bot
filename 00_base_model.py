# 데이터 불러오기
import pandas as pd
from lightgbm import LGBMRegressor
import os

# 현재 작업 디렉토리 확인 (선택)
print("현재 작업 경로:", os.getcwd())

# CSV 파일 경로 설정 ( 본인 환경에 맞게 수정)
train_path = './OIBC_2025_DATA/train.csv'
test_path =  './OIBC_2025_DATA/test.csv'
submission_path =  './OIBC_2025_DATA/submission_sample.csv'

# 데이터 읽기
train = pd.read_csv(train_path)
test = pd.read_csv(test_path)
submission = pd.read_csv(submission_path)

#time 컬럼을 날짜/시간 형식으로 변환
train['time'] = pd.to_datetime(train['time'])
test['time'] = pd.to_datetime(test['time'])

# 결측지 보정
features = train.columns.drop(['time', 'pv_id', 'type', 'energy', 'nins'])

# dfs = []
# for pv_id, df_group in train.groupby('pv_id'):
#     dfs.append(df_group[features].apply(lambda x: x.fillna(method='bfill')))
# weather_fillna_df = pd.concat(dfs)
# train[features] = weather_fillna_df

# dfs = []
# for pv_id, df_group in test.groupby('pv_id'):
#     dfs.append(df_group[features].apply(lambda x: x.fillna(method='bfill')))
# weather_fillna_df = pd.concat(dfs)
# test[features] = weather_fillna_df

def fill_group(df):
    return df.sort_values('time').fillna(method='bfill').fillna(method='ffill')

train = train.groupby('pv_id', group_keys=False).apply(fill_group)
test  = test.groupby('pv_id', group_keys=False).apply(fill_group)

#결측지가 포함된 행 제거
train = train.dropna(subset=['time', 'nins'])

#LightGBM 회귀 모델을 학습하고 test 데이터에 대한 일사량 추정값을 산출하는 과정
lgbm = LGBMRegressor()
lgbm.fit(train[features], train['nins'])
lgbm_pred = lgbm.predict(test[features])

# 음수로 에측된 값은 0으로 치환
lgbm_pred[lgbm_pred < 0] = 0

submission['nins'] = lgbm_pred
submission.to_csv('result_submission', index=False)