from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

# Create your views here.
def hw2(request):
    pubmed = getPubMed()
    twitter = getTwitter()
    return render(request, 'hw2.html', {
        'uploaded': False,
        'content': pubmed,
    })

def countWords(s):
    words = s.split()
    return len(words)
