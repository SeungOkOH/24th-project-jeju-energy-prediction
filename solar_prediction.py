import pandas as pd


# 새로운 데이터프레임을 생성
fcst_df = pd.DataFrame(columns=['Forecast_date', 'Forecast_hour', 'WindDirection', 'WindSpeed', 'Cloud', 'Rainfall', 'Humidity', 'Temperature'])

row_idx = 0  # row_idx 초기화

for data in response['response']['body']['items']['item']:
    fcst_df.loc[row_idx, 'Forecast_date'] = data['fcstDate']
    fcst_df.loc[row_idx, 'Forecast_hour'] = data['fcstTime']

    if data['category'] == 'REH':
        fcst_df.loc[row_idx, 'Humidity'] = float(data.get('fcstValue', 'NaN'))
    elif data['category'] == 'PCP':
        fcst_df.loc[row_idx, 'Rainfall'] = str(data.get('fcstValue', 'NaN'))
    elif data['category'] == 'TMP':
        fcst_df.loc[row_idx, 'Temperature'] = float(data.get('fcstValue', 'NaN'))
    elif data['category'] == 'SKY':
        fcst_df.loc[row_idx, 'Cloud'] = float(data.get('fcstValue', 'NaN'))
    elif data['category'] == 'VEC':
        fcst_df.loc[row_idx, 'WindDirection'] = float(data.get('fcstValue', 'NaN'))
    elif data['category'] == 'WSD':
        fcst_df.loc[row_idx, 'WindSpeed'] = float(data.get('fcstValue', 'NaN'))
        row_idx += 1  # 다음 행으로 이동
fcst_df['Forecast_date'] = pd.to_datetime(fcst_df['Forecast_date'], format='%Y%m%d')
fcst_df['Forecast_hour'] = fcst_df['Forecast_hour'].astype(str).str.zfill(4)  # 시간을 4자리 문자열로 변환
fcst_df['Forecast_hour'] = fcst_df['Forecast_hour'].str[:2].astype(int)  # 앞의 2자리를 추출하여 정수로 변환
fcst_df = fcst_df.rename(columns={'Forecast_date': 'date', 'Forecast_hour': 'hour'})
# date가 '
# 내일 날짜인 데이터만 추출하여 tomorrow_df에 저장
tomorrow_df = fcst_df[(fcst_df['date'] == formatted_tomorrow)].copy()