# Create your views here.
from django.http import HttpResponse
import json
from algorithm import models
from algorithm.stpvis import partition


def index(request):
    return HttpResponse("Hello, world. You're at the algorithm index.")


def my_api(request):
    dic = {}
    if request.method == 'GET':
        user_list = models.User.objects.all()
        print(partition.summation(5))
        return HttpResponse(user_list)
    else:
        dic['message'] = '方法错误'
        return HttpResponse(json.dumps(dic, ensure_ascii=False))
