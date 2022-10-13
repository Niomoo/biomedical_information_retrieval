from django.urls import path
from hw3 import views

urlpatterns = [
    path('', views.hw3, name='hw3'),
]