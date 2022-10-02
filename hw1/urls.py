from django.urls import path
from hw1 import views

urlpatterns = [
    path('', views.index, name='hw1'),
    path('fileUpload', views.file_upload, name='fileUpload'),
]