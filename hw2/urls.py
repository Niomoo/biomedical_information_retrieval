from django.urls import path
from hw2 import views

urlpatterns = [
    path('', views.hw2, name='hw2'),
    path('searchPubMed', views.searchPubMed, name='searchPubMed'),
    path('searchTwitter', views.searchTwitter, name='searchTwitter'),
]