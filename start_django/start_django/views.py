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
from .call_data.tomorrow_energy_data_get import get_energy_data
import logging


# prediction값 모델로부터 가져오기!!
def energy_data():
    logger = logging.getLogger(__name__)

    try:
        data = get_energy_data()
        logger.info("Successfully retrieved energy data")
        return data
    except Exception as e:
     
     
        logger.error(f"Error retrieving energy data: {e}")
        return {'error': str(e)}
#가져온 데이터 가공하기 (alert_data, fuel_data에서 사용할 것)
    
def processed_data():        
    try:
        json_data = energy_data()  # energy_data 함수 호출
        if 'error' in json_data:
            logger.error(f"Error in energy_data: {json_data['error']}")
            return None
        
        # 데이터 가공 로직을 여기에 추가...
        # elec, solar, wind 값들을 int()를 사용하여 정수로 변환
        processed_list = [
            {
                "index": i + 1, 
                "elec": int(float(elec)),  # 소수점 제거
                "solar": int(float(solar)),  # 소수점 제거
                "wind": int(float(wind))  # 소수점 제거
            }
            for i, (elec, solar, wind) in enumerate(zip(json_data['elec'], json_data['solar'], json_data['wind']))
        ]
        
        return processed_list
    except Exception as e:
        return None





#지우면 안됨.
def main(request):
    message = request.GET.get('abc')
    print(message)

    return HttpResponse("안녕?")







############################################################################################################

### frontend에게 전달


# time, demand, solarGen, windGen 차이값까지
def alert_data(request):
    logger = logging.getLogger(__name__)

    try:
        json_data = energy_data()  # energy_data 함수 호출

        # 에러 검사: json_data가 'error' 키를 포함하는지 확인
        if isinstance(json_data, dict) and 'error' in json_data:
            logger.error(f"Error in energy_data: {json_data['error']}")
            return JsonResponse({'error': json_data['error']}, status=500)
        
        # 데이터 가공
        if all(key in json_data for key in ['elec', 'solar', 'wind']):  # 필수 키 존재 확인
            processed_data = [
                {"index": i + 1, "elec": elec, "solar": solar, "wind": wind}
                for i, (elec, solar, wind) in enumerate(zip(json_data['elec'], json_data['solar'], json_data['wind']))
            ]

            
        return JsonResponse(processed_data, safe=False)  # 필터링된 데이터를 JSON 형태로 반환
    except Exception as e:
        logger.error(f"Error processing alert_data: {e}")
        return JsonResponse({'error': str(e)}, status=400)
    

def fuel_data(request):

    try:
        json_data = energy_data()  # energy_data 함수 호출

        # 에러 검사: json_data가 'error' 키를 포함하는지 확인
        if isinstance(json_data, dict) and 'error' in json_data:
            logger.error(f"Error in energy_data: {json_data['error']}")
            return JsonResponse({'error': json_data['error']}, status=500)
        
        # 데이터 가공
        if all(key in json_data for key in ['elec', 'solar', 'wind']):  # 필수 키 존재 확인
            processed_data = [
                {"index": i + 1, "elec": elec, "solar": solar, "wind": wind}
                for i, (elec, solar, wind) in enumerate(zip(json_data['elec'], json_data['solar'], json_data['wind']))
            ]

            filtered_data = [
            data for data in processed_data
            if data["elec"] > data["solar"] + data["wind"]
        ]

        return JsonResponse(filtered_data, safe=False)  # 필터링된 데이터를 JSON 형태로 반환
    except Exception as e:
        logger.error(f"Error processing alert_data: {e}")
        return JsonResponse({'error': str(e)}, status=400)
    


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