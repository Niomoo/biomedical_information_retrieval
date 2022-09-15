from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.

def index(request):
    return render(request, 'index.html')

def readFile(request, filename):
    response = requests.get(filename)
    content = response.json()['Text']
    return render(request, 'index.html', {
        "content": content,
    })
    if request.method == 'POST':
        File = request.FILES.get('files', None)
        content = open(File, 'r')
        s = content.read()
        return render(request, 'index.html', {
            "content": s,
        })