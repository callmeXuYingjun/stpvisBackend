from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('my_api', views.my_api, name='my_api'),
    path('treeInit', views.treeInit, name='treeInit'),
    path('partition', views.partition, name='partition'),
]