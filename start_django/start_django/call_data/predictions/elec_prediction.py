import pandas as pd
import numpy as np
import torch
from joblib import load

def convert_elec(tomorrow_df):
    tomorrow_df['dum_weekday'] = tomorrow_df['weekday'].copy()
    tomorrow_df = pd.get_dummies(tomorrow_df, columns = ['weekday'], prefix = 'weekday')
    tomorrow_df.rename(columns = {'dum_weekday': 'weekday'}, inplace = True)

    # 모든 요일에 대한 열이 있는지 확인하고, 없는 경우 해당 열 추가
    for i in range(7):  # 0부터 6까지 각 요일에 대해
        col_name = f'weekday_{i}'
        if col_name not in tomorrow_df.columns:
            tomorrow_df[col_name] = 0  # 없는 요일 열을 0으로 추가
        tomorrow_df[col_name] = tomorrow_df[col_name].astype(int)

    # 열 순서 정렬을 위해 열 이름을 정렬
    sorted_columns = sorted(tomorrow_df.columns)
    tomorrow_df = tomorrow_df[sorted_columns]

    # 스케일링
    columns_to_scale = ['WindDirection', 'WindSpeed', 'Cloud', 'Rainfall', 'Humidity', 'Temperature', 'Q12', 'Q13', 'Q_mean', 'weekday']

    sd_scaler = load('scalers/elec_scaler.joblib')
    tomorrow_df[columns_to_scale] = sd_scaler.transform(tomorrow_df[columns_to_scale])
    tomorrow_df = tomorrow_df.drop(['date', 'WindDirection', 'WindSpeed', 'Q12', 'Q_mean', 'weekday'], axis=1)

    testdata = tomorrow_df.to_numpy(dtype = np.float32)
    testdata = torch.tensor(testdata)

    return testdata