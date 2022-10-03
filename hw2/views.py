from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

# Create your views here.
def hw2(request):
    return render(request, 'hw2.html', {
        'search': False,
    })

def searchPubMed(request):
    with open('data/pubmed/pubmed_data.json') as file:
        data = json.loads(file.read())
    content = data[0]
    return render(request, 'hw2.html', {
        'search': True,
        'content': content,
    })