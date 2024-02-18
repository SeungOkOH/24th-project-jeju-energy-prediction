from django.shortcuts import render
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
# pytorch 모델을 사용해서 예측값을 생성하는 경우, 
import torch
from torchvision import transforms
from PIL import Image
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from call_data.tomorrow_energy_data_get import get_energy_data

# 예측 모델을 로드하는 함수 - 임의 ; 수정필요
def load_model(model_path):
    model = torch.load(model_path)
    model.eval()  # 모델을 추론 모드로 설정
    return model

# 모델을 사용하여 예측을 생성하는 함수 - 임의 ; 수정필요
def generate_prediction(model):
    # 모델 예측 수행 , 예측값을 list형식으로 저장(근데 아래에서 코드 작성하기 쉽게 저장해야될 듯)
    with torch.no_grad():
        prediction = model()
    return prediction

def split_predictions(raw_prediction):
    # 주어진 예측값과 모델의 예측 결과를 각각 변수에 저장 - 수정해야됨 엄청 많을 것이기 떄문 특히 alert가
    alert = {"time": raw_prediction["time"], "demand": raw_prediction["demand"], "solarGen": raw_prediction["solarGen"], "windGen": raw_prediction["windGen"]}
    solar_prediction = {"tomorrow_solar": raw_prediction["tomorrow_solar"]}
    wind_prediction = {"tomorrow_wind": raw_prediction["tomorrow_wind"]}
    demand_prediction = {"tomorrow_demand": raw_prediction["tomorrow_demand"]}
    
    return alert, solar_prediction, wind_prediction, demand_prediction


#지우면 안됨.
def main(request):
    message = request.GET.get('abc')
    print(message)

    return HttpResponse("안녕?")










############################################################################################################

### frontend에게 전달


# time, demand, solarGen, windGen 차이값까지
def alert_data(request):

    #모델이 예측 수행한 모듈에서 데이터 받는 부분을 작성해야함
    model_prediction = generate_prediction(load_model('모델 경로를 새롭게 지정하세요'))
    alert, solar_prediction, wind_prediction, demand_prediction = split_predictions(model_prediction)
    #
    #
     
   # 받은 데이터 예시 (time, demand, solarGen, windGen로 구성된 리스트)
    data_list = [
        {"time": "12:00", "demand": 100, "solarGen": 80, "windGen": 20},
        {"time": "13:00", "demand": 120, "solarGen": 100, "windGen": 30},
        {"time": "14:00", "demand": 150, "solarGen": 120, "windGen": 40},
        # 엄청 많은 데이터가 여기에 들어감
    ]
    filtered_data = []

    for data in data_list:
        # demand가 solarGen과 windGen의 합보다 작은 경우만 필터링
        if data["demand"] < data["solarGen"] + data["windGen"]:
            filtered_data.append(data)

    return JsonResponse(filtered_data, safe=False)


def fuel_data(request):

    #모델이 예측 수행한 모듈에서 데이터 받는 부분(여기 alert_data랑 같은 데이터 들어감)을 작성해야함
    #
    #
    #

   # 받은 데이터 예시 (time, demand, solarGen, windGen로 구성된 리스트)
    data_list = [
        {"time": "12:00", "demand": 100, "solarGen": 80, "windGen": 10},
        {"time": "13:00", "demand": 120, "solarGen": 100, "windGen": 30},
        {"time": "14:00", "demand": 150, "solarGen": 120, "windGen": 40},
        # 엄청 많은 데이터가 여기에 들어감
    ]
    filtered_data = []

    for data in data_list:
        # demand가 solarGen과 windGen의 합보다 작은 경우만 필터링
        if data["demand"] > data["solarGen"] + data["windGen"]:
            filtered_data.append(data)

    return JsonResponse(filtered_data, safe=False)

# 아름답게 잘 그려진 데이터가 png 파일로 저장되어 있어야함.
def demand_graph(request):

    # 예측값을 시각화하고 png 파일로 디렉토리 안에 demand_graph란 이름으로 저장하는 코드 작성해야함.
    #
    #
    #

    # 이미지 파일 경로
    image_path = os.path.join(BASE_DIR, 'demand_graph.png')  # demand_graph.png 파일이 저장된 경로로 수정할 것.

    # 이미지 파일 읽기
    with open(image_path, 'rb') as img_file:
        response = HttpResponse(img_file.read(), content_type='image/png')

    return response


### gencomponent 

def solar_graph(request):
    # 예측값을 시각화하고 png 파일로 디렉토리 안에 solar_graph 이름으로 저장하는 코드 작성해야함.
    #
    #
    #


    # 이미지 파일 경로
    image_path = os.path.join(BASE_DIR, 'solar_graph.png')  # 경로 수정할 것.

    # 이미지 파일 읽기
    with open(image_path, 'rb') as img_file:
        response = HttpResponse(img_file.read(), content_type='image/png')

    return response

def wind_graph(request):


    # 예측값을 시각화하고 png 파일로 디렉토리 안에 wind_graph란 이름으로 저장하는 코드 작성해야함.
    #
    #
    #

    # 이미지 파일 경로
    image_path = os.path.join(BASE_DIR, 'wind_graph.png')  # 경로 수정할 것.

    # 이미지 파일 읽기
    with open(image_path, 'rb') as img_file:
        response = HttpResponse(img_file.read(), content_type='image/png')

    return response