from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import json
from . import models

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def my_api(request):
    dic = {}
    if request.method == 'GET':

        user_list =models.User.objects.all(); 
        dic['message'] = 1000
        return HttpResponse(json.dumps(dic))
    else:
        dic['message'] = '方法错误'
        return HttpResponse(json.dumps(dic, ensure_ascii=False))
