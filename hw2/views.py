from django.shortcuts import render, redirect
from django.http import HttpResponse
import xml.etree.ElementTree as ET
import json
import requests
from metapub import PubMedFetcher

# Create your views here.
def hw2(request):
    pubmed = getPubMed()
    twitter = getTwitter()
    return render(request, 'hw2.html', {
        'uploaded': False,
    })

def getPubMed():
    with open('hw2/data/pubmed/pubmed_data.json') as file:
        data = json.loads(file.read())
    content = ''
    for text in data:
        content += text
    return content

def getTwitter():
    with open('hw2/data/tweets/tweet_data.json') as file:
        data = json.loads(file.read())
    content = ''
    for text in data:
        content += text['text']
    return content

def countWords(s):
    words = s.split()
    return len(words)