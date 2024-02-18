import torch
from joblib import load
import numpy as np

def convert_solar(tomorrow_df):
    # 스케일링
    columns_to_scale = ['WindDirection', 'WindSpeed', 'Cloud', 'Rainfall', 'Humidity', 'Temperature', 'Q12', 'Q13', 'Q_mean']

    sd_scaler = load('scalers/solar_scaler.pkl')
    tomorrow_df[columns_to_scale] = sd_scaler.transform(tomorrow_df[columns_to_scale])
    tomorrow_df = tomorrow_df.drop(['date', 'WindDirection', 'WindSpeed', 'Q12', 'Q_mean', 'weekday'], axis=1)
    
    testdata = tomorrow_df.to_numpy(dtype = np.float32)
    testdata = torch.tensor(testdata)

    return testdata