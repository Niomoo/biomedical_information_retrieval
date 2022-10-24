from django.shortcuts import render
from gensim.models import word2vec

# Create your views here.
def hw3(request):
    return render(request, 'hw3.html')

def get_top_similarity(request):
    if request.method == 'POST':
        word = request.POST.get('words')
        model = word2vec.Word2Vec.load('hw3/model/cbow_1000.model')
        word_list = []
        for item in model.wv.most_similar(word):
            word_list.append(item[0])
    return render(request, 'hw3.html', {
        'content': word_list
    })

def train_model(word):
    model1 = word2vec.Word2Vec.load('hw3/model/cbow_1000.model')
    model2 = word2vec.Word2Vec.load('hw3/model/skipgram_1000.model')
    model3 = word2vec.Word2Vec.load('hw3/model/cbow_5000.model')
    model4 = word2vec.Word2Vec.load('hw3/model/skipgram_5000.model')
    model5 = word2vec.Word2Vec.load('hw3/model/cbow_10000.model')
    model6 = word2vec.Word2Vec.load('hw3/model/skipgram_10000.model')