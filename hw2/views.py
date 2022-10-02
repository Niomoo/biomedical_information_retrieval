from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def hw2(request):
    return render(request, 'hw2.html', {
        'uploaded': False,
    })
