from django.urls import path

from . import views

urlpatterns = [
    path('treeInit', views.treeInit, name='treeInit'),
    path('partition', views.partition, name='partition'),
]