# 파일: data_inspect.py
# 사용법 예: python data_inspect.py
import pandas as pd
import numpy as np
import sys
from pathlib import Path

def load_csv(path, parse_time_col='time'):
    """CSV를 읽어오고 time 컬럼이 있으면 datetime으로 파싱"""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"{path} 이(가) 없습니다.")
    df = pd.read_csv(path, low_memory=False)
    if parse_time_col in df.columns:
        try:
            df[parse_time_col] = pd.to_datetime(df[parse_time_col])
        except Exception:
            # 파싱 실패시 원본 유지
            pass
    return df

def basic_summary(df, name="data", head_n=5, value_count_cols=None, dropna_rows=False):
    """
    데이터프레임 기본 요약 출력

    - dropna_rows=False: (기본) 원본 기준 통계 + NA 제외한 컬럼별 통계 출력
    - dropna_rows=True: 결측치(행) 제거 후 전체 describe 출력(완전결측 제거된 샘플만)
    """
    print(f"\n=== [{name}] 기본 정보 ===")
    print("Shape (rows, cols):", df.shape)
    print("\n-- 컬럼 목록 (순서대로) --")
    print(list(df.columns))
    print("\n-- dtypes 및 non-null 개요 --")
    df.info(verbose=True, memory_usage='deep')
    
    mem_bytes = df.memory_usage(deep=True).sum()
    print(f"\n총 메모리 사용량: {mem_bytes/1024**2:.2f} MB")
    
    print(f"\n-- 상위 {head_n}개 샘플 --")
    display_head = df.head(head_n)
    print(display_head.to_string(index=False))
    
    # --- 원본 수치형 기술통계 (pandas.describe는 기본적으로 NaN 제외하여 계산) ---
    print("\n-- 원본 데이터 수치형 기술 통계 (NaN 제외하여 계산하는 기본 describe) --")
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df.select_dtypes(include=[np.number]).describe().T)
    
    # --- 옵션: 결측치(행) 제거 후 전체 describe ---
    if dropna_rows:
        df_dropna_rows = df.dropna(axis=0, how='any')
        print(f"\n-- 결측치(행) 제거 후 전체 데이터 수치형 기술 통계 (rows with ANY NaN removed) --")
        print("New shape:", df_dropna_rows.shape)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(df_dropna_rows.select_dtypes(include=[np.number]).describe().T)
    else:
        # --- 컬럼별로 NA 제외한 통계(각 컬럼에서 사용 가능한 값만으로 계산) ---
        print("\n-- 컬럼별 NA 제외 통계(각 컬럼의 available 값으로 계산) --")
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        # 각 컬럼별 describe를 요약해서 보여줌 (count는 NaN 제외한 개수)
        for c in num_cols:
            desc = df[c].describe()  # describe excludes NaN by default
            print(f"\n[{c}] (NA 제외) count={int(desc['count']) if not np.isnan(desc['count']) else 0}")
            print(desc.to_string())
    
    print("\n-- 범주형/문자열 요약 (unique 개수, top 값) --")
    obj_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    for c in obj_cols:
        nunique = df[c].nunique(dropna=False)
        top = df[c].mode().iloc[0] if nunique>0 else None
        print(f"  {c}: unique={nunique}, top={top}")
    
    # 결측치 요약
    print("\n-- 결측치 (missing) 요약 --")
    miss = df.isna().sum()
    miss_percent = (miss / len(df) * 100).round(3)
    miss_table = pd.DataFrame({'missing_count': miss, 'missing_pct': miss_percent})
    print(miss_table.sort_values('missing_pct', ascending=False).to_string())
    
    # 유니크 값 수 (간단히)
    print("\n-- 컬럼별 unique count (상위 20) --")
    uniq = df.nunique(dropna=False).sort_values(ascending=False)
    print(uniq.head(20).to_string())
    
    # value_counts 확인(선택 컬럼)
    if value_count_cols:
        print("\n-- 지정 컬럼의 상위 value_counts --")
        for c in value_count_cols:
            if c in df.columns:
                print(f"\n[{c}] top 10:")
                print(df[c].value_counts(dropna=False).head(10).to_string())
            else:
                print(f"\n[{c}] 존재하지 않는 컬럼입니다.")
    print("\n=== 요약 끝 ===\n")

def save_summary_csv(df, out_path):
    """컬럼별 결측/유니크/타입 요약을 csv로 저장"""
    miss = df.isna().sum()
    miss_pct = (miss / len(df) * 100).round(6)
    summary = pd.DataFrame({
        'dtype': df.dtypes.astype(str),
        'non_null_count': df.count(),
        'missing_count': miss,
        'missing_pct': miss_pct,
        'unique_count': df.nunique(dropna=False)
    })
    summary.to_csv(out_path)
    print(f"요약 파일 저장됨: {out_path}")

def head_stats(df, head_n=5, dropna_rows=False, show_non_numeric=True):
    """
    상위 head_n개 샘플에서 통계 확인
    - dropna_rows=False: 선택된 행들(예: first 5 rows)에서 각 컬럼별로 NaN을 제외한 통계 출력
      (pandas.describe는 NaN을 자동 제외합니다.)
    - dropna_rows=True: 선택된 행들 중 NaN을 포함한 행을 모두 제거한 뒤(완전한 행만),
      남은 행들에 대해 전체 통계 출력.
    """
    head = df.head(head_n).copy()
    print(f"\n== 상위 {head_n}개 샘플 선택 (원본 shape: {df.shape}) ==\n")
    print(head.to_string(index=False))  # 샘플 자체를 먼저 보여줌

    if dropna_rows:
        head_drop = head.dropna(axis=0, how='any')
        print(f"\n== 선택된 {head_n}개 행에서 NaN 포함 행 제거 후 shape: {head_drop.shape} ==")
        if head_drop.empty:
            print("모든 선택된 행들에 NaN이 포함되어 있어 제거 후 남는 행이 없습니다.")
        else:
            print("\n-- 수치형 통계 (describe) --")
            print(head_drop.select_dtypes(include=[np.number]).describe().T)
            if show_non_numeric:
                print("\n-- 범주형/문자열 통계 (count, unique, top) --")
                for c in head_drop.select_dtypes(include=['object','category']).columns:
                    print(f"{c}: count={head_drop[c].count()}, unique={head_drop[c].nunique(dropna=False)}, top={head_drop[c].mode().iloc[0] if head_drop[c].count()>0 else None}")
    else:
        print(f"\n== 선택된 {head_n}개 행에서 컬럼별 NaN 제외 통계(available 값으로 계산) ==")
        num_cols = head.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            # describe는 NaN 자동 제외
            print("\n-- 수치형 통계 (NaN 제외, describe) --")
            print(head[num_cols].describe().T)
            # 각 컬럼별로 non-null 개수 표시
            non_null_counts = head[num_cols].count()
            print("\n-- 각 수치형 컬럼의 non-null 개수 (selected rows 중) --")
            print(non_null_counts.to_string())
        else:
            print("선택된 샘플에 수치형 컬럼이 없습니다.")
        if show_non_numeric:
            print("\n-- 범주형/문자열 통계 (selected rows) --")
            for c in head.select_dtypes(include=['object','category']).columns:
                print(f"{c}: count={head[c].count()}, unique={head[c].nunique(dropna=False)}, top={head[c].mode().iloc[0] if head[c].count()>0 else None}")

if __name__ == "__main__":
    # 기본 경로 (같은 폴더에 train.csv, test.csv가 있다고 가정)
    train_path = './OIBC_2025_DATA/train.csv'
    
    # 필요하면 CLI 인자로 경로를 받을 수 있음: python data_inspect.py train.csv
    if len(sys.argv) >= 2:
        train_path = sys.argv[1]
    # 추가 플래그로 결측치 제거 후 통계만 보고 싶으면 다음처럼 실행: python data_inspect.py train.csv drop
    dropna_flag = (len(sys.argv) >= 3 and sys.argv[2].lower() in ['drop','dropna','d'])
    
    train_df = load_csv(train_path)
    # dropna_rows=True 로 하면 "결측치(행) 제거 후 전체 describe"를 보여줍니다.
    basic_summary(train_df, name="train", head_n=5, value_count_cols=['pv_id','type'], dropna_rows=dropna_flag)
    
    # 간단한 CLI 사용 예:
    # python head_stats.py ./OIBC_2025_DATA/train.csv 5       -> 상위 5개, 컬럼별 NaN 제외 통계
    # python head_stats.py ./OIBC_2025_DATA/train.csv 5 drop  -> 상위 5개 중 NaN 포함 행 제거 후 통계
    if len(sys.argv) < 3:
        print("사용법: python head_stats.py <train.csv 경로> <head_n> [drop]")
        sys.exit(0)
    path = Path(sys.argv[1])
    head_n = int(sys.argv[2])
    drop_flag = len(sys.argv) >= 4 and sys.argv[3].lower() in ['drop','dropna','d']
    df = pd.read_csv(path, low_memory=False)
    # time 컬럼이 있으면 datetime으로 변환 (선택)
    if 'time' in df.columns:
        try:
            df['time'] = pd.to_datetime(df['time'])
        except Exception:
            pass
    head_stats(df, head_n=head_n, dropna_rows=drop_flag)
    # 요약 CSV로 저장 (원하면 활성화)
    # save_summary_csv(train_df, "train_summary.csv")