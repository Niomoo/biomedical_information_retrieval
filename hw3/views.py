from django.shortcuts import render
from gensim.models import word2vec
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


# Create your views here.
def hw3(request):
    content = train_model('cancer')
    return render(request, 'hw3.html', {
        'search': False,
        'cbow_1000': content['cbow_1000'],
        'skipgram_1000': content['skipgram_1000'],
        'cbow_5000': content['cbow_5000'],
        'skipgram_5000': content['skipgram_5000'],
        'cbow_10000': content['cbow_10000'],
        'skipgram_10000': content['skipgram_10000'],
    })

def get_top_similarity(request):
    if request.method == 'POST':
        word = request.POST.get('words')
        content = train_model(word)
    return render(request, 'hw3.html', {
        'search': True,
        'subject': word,
        'cbow_1000': content['cbow_1000'],
        'skipgram_1000': content['skipgram_1000'],
        'cbow_5000': content['cbow_5000'],
        'skipgram_5000': content['skipgram_5000'],
        'cbow_10000': content['cbow_10000'],
        'skipgram_10000': content['skipgram_10000'],
    })

def train_model(word):
    model1 = word2vec.Word2Vec.load('hw3/model/cbow_1000.model')
    model2 = word2vec.Word2Vec.load('hw3/model/skipgram_1000.model')
    model3 = word2vec.Word2Vec.load('hw3/model/cbow_5000.model')
    model4 = word2vec.Word2Vec.load('hw3/model/skipgram_5000.model')
    model5 = word2vec.Word2Vec.load('hw3/model/cbow_10000.model')
    model6 = word2vec.Word2Vec.load('hw3/model/skipgram_10000.model')
    
    cbow_1000 = []
    skipgram_1000 = []
    cbow_5000 = []
    skipgram_5000 = []
    cbow_10000 = []
    skipgram_10000 = []

    plot_list = []
    plot_list2 = []
    for item in model1.wv.most_similar(word):
        item_list = list(item)
        plot_list.append(item_list[0])
        item_list[1] = round(item_list[1], 5)
        item_tuple = tuple(item_list)
        cbow_1000.append(item_tuple)
    visualization(model1, plot_list, 'CBOW_1000')
    for item in model2.wv.most_similar(word):
        item_list = list(item)
        plot_list.append(item_list[0])
        item_list[1] = round(item_list[1], 5)
        item_tuple = tuple(item_list)
        skipgram_1000.append(item_tuple)
    visualization(model2, plot_list, 'skipgram_1000')
    for item in model3.wv.most_similar(word):
        item_list = list(item)
        plot_list.append(item_list[0])
        item_list[1] = round(item_list[1], 5)
        item_tuple = tuple(item_list)
        cbow_5000.append(item_tuple)
    visualization(model3, plot_list, 'CBOW_5000')
    for item in model4.wv.most_similar(word):
        item_list = list(item)
        plot_list2.append(item_list[0])
        item_list[1] = round(item_list[1], 5)
        item_tuple = tuple(item_list)
        skipgram_5000.append(item_tuple)
    visualization(model4, plot_list2, 'skipgram_5000')
    for item in model5.wv.most_similar(word):
        item_list = list(item)
        plot_list.append(item_list[0])
        item_list[1] = round(item_list[1], 5)
        item_tuple = tuple(item_list)
        cbow_10000.append(item_tuple)
    visualization(model5, plot_list, 'CBOW_10000')
    for item in model6.wv.most_similar(word):
        item_list = list(item)
        plot_list.append(item_list[0])
        item_list[1] = round(item_list[1], 5)
        item_tuple = tuple(item_list)
        skipgram_10000.append(item_tuple)  
    visualization(model6, plot_list, 'skipgram_10000')
        
    return {
        'cbow_1000': cbow_1000,
        'skipgram_1000': skipgram_1000,
        'cbow_5000': cbow_5000,
        'skipgram_5000': skipgram_5000,
        'cbow_10000': cbow_10000,
        'skipgram_10000': skipgram_10000,
    }  

def visualization(model, words, title):
    my_vocab = {}
    for w in words:
        my_vocab[w] = model.wv.key_to_index[w]
    X = model.wv[my_vocab]
    twoDim = PCA().fit_transform(X)[:,:2]
    plt.figure(figsize=(5,5))        
    plt.title(title)
    plt.scatter(twoDim[:,0], twoDim[:,1], edgecolors='k', c='r')
    for word, (x,y) in zip(words, twoDim):
        plt.text(x+0.05, y+0.05, word)
    plt.tight_layout()
    plt.savefig('static/img/' + title + '.png')
    