from django.urls import path
from hw1 import views

urlpatterns = [
    path('', views.index, name='index'),
    path('readFile', views.readFile, name='readFile'),
]