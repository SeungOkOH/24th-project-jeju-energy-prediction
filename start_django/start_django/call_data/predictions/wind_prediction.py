import pandas as pd
import urllib
import urllib.request
import json
import datetime
import numpy as np
import math
from joblib import load
import torch

def convert_wind(tomorrow_df):
    tomorrow_df = tomorrow_df.dropna()
    tomorrow_df.reset_index(drop = True, inplace = True)

    tomorrow_df['WindDirection_cos'] = tomorrow_df['WindDirection'].apply(lambda x : math.cos(x))
    tomorrow_df['WindDirection_sin'] = tomorrow_df['WindDirection'].apply(lambda x : math.sin(x))

    tomorrow_df['Year'] = tomorrow_df['date'].apply(lambda x : x.year)
    tomorrow_df['Month'] = tomorrow_df['date'].apply(lambda x : x.month)
    tomorrow_df['Day'] = tomorrow_df['date'].apply(lambda x : x.day)

    tomorrow_df = tomorrow_df.drop(columns = ['WindDirection', 'Q12', 'Q13', 'date'])

    columns_to_scale = ['WindSpeed', 'Cloud', 'Rainfall', 'Humidity', 'Temperature', 'Q_mean']
    
    sd_scaler = load('scalers/wind_scaler.bin')
    tomorrow_df[columns_to_scale] = sd_scaler.transform(tomorrow_df[columns_to_scale])

    PCA_df = tomorrow_df.drop(columns = ['WindSpeed', 'WindDirection_cos', 'WindDirection_sin', 'weekday'])
    pca = load('scalers/pca_model.joblib')
    PCA_df = pca.transform(PCA_df)
    principalDf = pd.DataFrame(data = PCA_df, columns = ['PC1', 'PC2', 'PC3'])

    tomorrow_df = pd.concat([tomorrow_df[['WindSpeed', 'WindDirection_cos', 'WindDirection_sin']], principalDf], axis = 1)
    testdata = tomorrow_df.to_numpy(dtype = np.float32)
    testdata = torch.tensor(testdata)
    
    return testdata