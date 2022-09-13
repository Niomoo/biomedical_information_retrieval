from django.urls import path
from hw1 import views

urlpatterns = [
    path('home', views.index, name='index'),
]