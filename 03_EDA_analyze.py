# 데이터 불러오기
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 현재 작업 디렉토리 확인 (선택)
# 
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

# 기본 통계
print(train[['nins']].describe())

# 결측치 비율
na_ratio = train.isna().mean().sort_values(ascending=False)
print(na_ratio.head(20))

# 상관관계(타겟 포함)
cols = ['nins'] + list(features)
numeric_cols = train[cols].select_dtypes(include=[np.number]).columns.tolist()

# numeric_cols에 'nins'가 반드시 포함되어 있어야 합니다.
# (만약 nins가 float/int가 아니라면 먼저 train['nins'] = pd.to_numeric(train['nins'], errors='coerce') 등으로 변환)
corr = train[numeric_cols].corr()

# 이후 기존의 annot/threshold 처리 코드는 그대로 사용 가능
threshold = 0.3
annot = corr.round(2).astype(str)
annot_mask = corr.abs() < threshold
for i in range(annot.shape[0]):
    for j in range(annot.shape[1]):
        if annot_mask.iloc[i, j]:
            annot.iloc[i, j] = ''

plt.figure(figsize=(10,10))
sns.heatmap(corr, vmin=-1, vmax=1, center=0, cmap='vlag', annot=annot, fmt='', square=False, cbar_kws={'shrink':0.6})
plt.title(f'Correlation matrix (annotations only where |corr| >= {threshold})')
plt.show()