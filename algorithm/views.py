# Create your views here.
from django.http import HttpResponse
import numpy as np
import json
from algorithm import models
from algorithm.stpvis import tree

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        """
        只要检查到了是bytes类型的数据就把它转为str类型
        :param obj:
        :return:
        """
        print(type(obj))
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def index(request):
    return HttpResponse("Hello, world. You're at the algorithm index.")
def Object2dict(obj):
    if type(obj) is np.ndarray:
        return obj.tolist()
    else:
        return obj.__dict__

def my_api(request):
    dic = {}
    if request.method == 'GET':
        user_list = models.User.objects.all()
        return HttpResponse(user_list)
    else:
        dic['message'] = '方法错误'
        return HttpResponse(json.dumps(dic, ensure_ascii=False))
def treeInit(request):
    tree.treeInit()
    treeOut=tree.partition("Root",0,2)
    
    # partition.partition("A0",1,2)
    # partition.partition("A01",2,3)
    # tree=partition.partition("A011",1,2)
    # print(filter(lambda a: not a.startswith('__'), dir(treeOut)))
    # return HttpResponse(json.dumps(treeOut, default=lambda obj: obj.__dict__, sort_keys=True, indent=4))
    return HttpResponse(json.dumps(treeOut, default=lambda obj:obj.tolist() if  type(obj) is np.ndarray else obj.__dict__, sort_keys=True, indent=4))
    # return HttpResponse(json.dumps(treeOut,cls=MyEncoder,indent=4))

def partition(request):
    dimensionSelect=int(request.GET.get('dimensionSelect'))
    clusteringMethodsSelect=request.GET.get('clusteringMethodsSelect')
    clusterNum=int(request.GET.get('clusterNum'))
    tensorSelectedData=request.GET.get('tensorSelectedData')
    print(tensorSelectedData,dimensionSelect,clusterNum)
    treeOut=tree.partition(tensorSelectedData,dimensionSelect,clusterNum)
    
    return HttpResponse(json.dumps(treeOut, default=lambda obj:obj.tolist() if  type(obj) is np.ndarray else obj.__dict__, sort_keys=True, indent=4))
