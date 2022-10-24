from django.urls import path
from hw3 import views

urlpatterns = [
    path('', views.hw3, name='hw3'),
    path('getSimilar', views.get_top_similarity, name='get_top_similarity'),
]