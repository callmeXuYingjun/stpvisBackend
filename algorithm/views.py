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
        return HttpResponse(user_list)
    else:
        dic['message'] = '方法错误'
        return HttpResponse(json.dumps(dic, ensure_ascii=False))
def patition(request):
    partition.treeInit()
    partition.partition("A",0,2)
    partition.partition("A0",1,2)
    partition.partition("A01",2,3)
    tree=partition.partition("A011",1,2)
    return HttpResponse(json.dumps(tree, default=lambda obj: obj.__dict__, sort_keys=True, indent=4))
