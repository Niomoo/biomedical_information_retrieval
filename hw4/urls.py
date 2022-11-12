from django.urls import path
from hw4 import views

urlpatterns = [
    path('', views.hw4, name='hw4'),
]