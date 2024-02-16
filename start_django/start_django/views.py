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

def hello_view(request):
    data = {'message': 'Hello?'}
    return JsonResponse(data)

#
def solar_graph(request):
    data = {'message': 'Hello?'}
    return JsonResponse(data)

