from django.urls import path
from hw2 import views

urlpatterns = [
    path('', views.hw2, name='hw2'),
]