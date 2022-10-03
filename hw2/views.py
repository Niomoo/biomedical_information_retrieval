from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
from .porter import PorterStemmer

# Create your views here.
def hw2(request):
    common_pubMed = getPubMedData()
    common_tweet = getTwitterData()
    return render(request, 'hw2.html', {
        'search': False,
        'pubmed': common_pubMed,
        'tweet': common_tweet,
    })

def searchPubMed(request):
    with open('hw2/data/pubmed/pubmed_data.json') as file:
        data = json.loads(file.read())
    content = data[0]
    return render(request, 'hw2.html', {
        'search': True,
        'content': content,
    })

def searchTwitter(request):
    with open('hw2/data/tweets/tweet_data.json') as file:
        data = json.loads(file.read())
    content = ''
    for text in data[6:11]:
        content += text['text']
    return render(request, 'hw2.html', {
        'search': True,
        'content': content,
    })

def getPubMedData():
    with open('hw2/data/pubmed/pubmed_data.json') as file:
        data = json.loads(file.read())
        content = ''
        for text in data:
            content += text
    top_word = getWordList(content)
    return top_word[:5]
    
def getTwitterData():
    with open('hw2/data/tweets/tweet_data.json') as file:
        data = json.loads(file.read())
        content = ''
        for text in data:
            content += text['text']
    top_word = getWordList(content)
    return top_word[:5]

def getWordList(content):
    words = Counter(content.split())
    ps = PorterStemmer()
    stem_word = []
    for word in words:
        stem_word.append(ps.stem(word))
    words_count = {}
    for word in stem_word:
        if(words_count.get(word) == None):
            words_count[word] = 1
        else:
            words_count[word] += 1
    common_word = sorted(words_count.items(), key=lambda x: x[1], reverse=True)
    return common_word