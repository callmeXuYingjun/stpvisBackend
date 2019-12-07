
# Create your views here.
from django.http import HttpResponse
import json
from polls import models


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def my_api(request):
    dic = {}
    if request.method == 'GET':
        user_list = models.User.objects.all()
        return HttpResponse(user_list)
    else:
        dic['message'] = '方法错误'
        return HttpResponse(json.dumps(dic, ensure_ascii=False))
