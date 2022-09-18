from django.urls import path
from hw1 import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fileUpload', views.file_upload, name='fileUpload'),
]