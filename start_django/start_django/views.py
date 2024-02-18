from django.shortcuts import render
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse


def model(request):
  return JsonResponse({"result":[0]*24})


def main(request):
    message = request.GET.get('abc')
    print(message)

    return HttpResponse("안녕?")


### demand component

# 여기에 결과값 받아와서 가공해서 보내주기 
# time, demand, solarGen, windGen 차이값까지
def alert_data(request):

    #모델에서 데이터 받는 부분을 작성해야함
    #
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

    #모델에서 데이터 받는 부분(여기 alert_data랑 같은 데이터 들어감)을 작성해야함
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