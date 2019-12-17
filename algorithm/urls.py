from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('my_api', views.my_api, name='my_api'),
    path('patition', views.patition, name='patition'),
    path('patition1', views.patition1, name='patition1'),
]