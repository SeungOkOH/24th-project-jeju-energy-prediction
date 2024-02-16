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
    return response