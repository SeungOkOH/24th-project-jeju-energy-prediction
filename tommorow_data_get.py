import pandas as pd
import urllib
import urllib.request
import json
import numpy as np
from datetime import date, timedelta, datetime

#오늘 내일 날짜 불러오기
def get_data():
    today = date.today()
    formatted_today = today.strftime('%Y%m%d')
    tomorrow = today + timedelta(days=1)
    formatted_tomorrow = tomorrow.strftime('%Y%m%d')

    servicekey = 's+fQ9LDUrt9xJ9LSIp0R4+gJBR7eOiUpRHNKXMb6gaV844FL4oI+OYVOY+MC2Bff+Iq9bQWFeWrktswAfBtkyg=='
    url= 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'

    queryParams = '?' + urllib.parse.urlencode(
        {
            urllib.parse.quote_plus('servicekey') : servicekey,
            urllib.parse.quote_plus('pageNo') : '1',
            urllib.parse.quote_plus('numOfRows') : '372',  # 12 * 31 = 372
        # 아님 12개 항목임
            urllib.parse.quote_plus('dataType') : 'JSON', # JSON, XML 두가지 포멧을 제공합니다.
            urllib.parse.quote_plus('base_date') : formatted_today, # 예보 받을 날짜를 입력합니다. 최근 1일간의 자료만 제공합니다.
            urllib.parse.quote_plus('base_time') : '1700', # 예보 시간을 입력합니다. 2시부터 시작하여 3시간 단위로 입력 가능합니다.
            urllib.parse.quote_plus('nx') : '48', # 울산 태양광 발전소 x 좌표입니다. '기상청18_동네예보 조회서비스_오픈API활용가이드.zip'에 포함 된 excel파일을 통해 확인 가능합니다.
            urllib.parse.quote_plus('ny') : '36' # 울산 태양광 발전소 y 좌표입니다. '기상청18_동네예보 조회서비스_오픈API활용가이드.zip'에 포함 된 excel파일을 통해 확인 가능합니다.
        }
    )

    response = urllib.request.urlopen(url + queryParams).read()
    response = json.loads(response)
    
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
    # Forecast_date와 Forecast_hour 열을 datetime 형식으로 변환
    fcst_df['Forecast_date'] = pd.to_datetime(fcst_df['Forecast_date'], format='%Y%m%d')
    fcst_df['Forecast_hour'] = fcst_df['Forecast_hour'].astype(str).str.zfill(4)  # 시간을 4자리 문자열로 변환
    fcst_df['Forecast_hour'] = fcst_df['Forecast_hour'].str[:2].astype(int)  # 앞의 2자리를 추출하여 정수로 변환
    fcst_df = fcst_df.rename(columns={'Forecast_date': 'date', 'Forecast_hour': 'hour'})
    # date가 '20240213'인 데이터만 추출하여 tomorrow_df에 저장
    tomorrow_df = fcst_df[(fcst_df['date'] == formatted_tomorrow)].copy()
    tomorrow_df.replace('강수없음', int('0'), inplace=True)
    # Rainfall 열 값 변경
    rainfall_mapping = {'0': 0, '1mm 미만': 1, '1.0mm': 1, '2.0mm': 1, '3.0mm': 1}
    tomorrow_df['Rainfall'] = tomorrow_df['Rainfall'].astype(str).map(rainfall_mapping).fillna(2).astype(int)

    # Cloud 값 보정
    cloud_mapping = {1: 2, 2: 4, 3: 8, 4: 10}
    tomorrow_df['Cloud'] = tomorrow_df['Cloud'].map(cloud_mapping)

    # hour 값 0~23 을 1~24로 수정
    tomorrow_df['hour'] = tomorrow_df['hour'] + 1
    an = [1.000110,0.034221,0.000719]
    bn = [0,0.001280,0.000077]
    cn = [0.006918,-0.399912,-0.006758,-0.002697]
    dn = [0,0.070257,0.000907,0.000148]


    S = 1367 #solar constant
    L = 33.3 #latitude
    L_rad = np.deg2rad(L) #latitude를 rad으로 변환

    tomorrow_df['date'] = pd.to_datetime(tomorrow_df['date'])
    d = tomorrow_df['date'].dt.dayofyear
    t = 2*np.pi*d/365

    LN = datetime.datetime(2024, 2, 9, 12, 0, 0) # local noon time
    # sun-earth distance  : r0 값을 알 수 없어서, a로 근사한 식을 이용함
    r0_r2 = np.zeros(t.shape)
    for i in range(0,3) :
        r0_r2 = r0_r2+an[i]*np.cos(i*t)+bn[i]*np.sin(i*t)
    # declination angle
    delta_rad = np.zeros(t.shape)
    for i in range(0,4) :
        delta_rad = delta_rad+cn[i]*np.cos(i*t)+dn[i]*np.sin(i*t)
    # Solar insolation for hour gap
    # Q12는 태양 남중 12시로 가정한거고, Q13은 남중 13시로 가정한검니당
    Q = np.zeros(t.shape)
    gap = np.pi/12
    tomorrow_df['Q12'] = S*r0_r2*((np.sin(L_rad)*np.sin(delta_rad))+((24/np.pi)*np.cos(L_rad)*np.cos(delta_rad)*np.sin(np.pi/24)*np.cos((tomorrow_df.hour-12)*gap)))
    tomorrow_df['Q12'] = tomorrow_df['Q12'].ap  ply(lambda x: max(0, x))
    tomorrow_df['Q13'] = S*r0_r2*((np.sin(L_rad)*np.sin(delta_rad))+((24/np.pi)*np.cos(L_rad)*np.cos(delta_rad)*np.sin(np.pi/24)*np.cos((tomorrow_df.hour-13)*gap)))
    tomorrow_df['Q13'] = tomorrow_df['Q13'].apply(lambda x: max(0, x))
    tomorrow_df['Q_mean'] = (tomorrow_df['Q12']+tomorrow_df['Q13'])/2
    tomorrow_df['date'] = pd.to_datetime(tomorrow_df['date'])
    tomorrow_df['weekday'] = tomorrow_df['date'].dt.dayofweek
    # columns_to_scale 정의
    columns_to_scale = ['WindDirection', 'WindSpeed', 'Cloud', 'Rainfall', 'Humidity', 'Temperature', 'Q12', 'Q13', 'Q_mean', 'weekday']
    # test 세트에도 동일한 scaling 적용
    tomorrow_df[columns_to_scale] = ss.transform(tomorrow_df[columns_to_scale])