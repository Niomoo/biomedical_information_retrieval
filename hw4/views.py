from django.shortcuts import render
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter
import numpy as np
import json
import re

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

processed_title = []
processed_text = []

DF = {}
TF_IDF = {}
TF_IDF_TITLE = {}

# Create your views here.
def hw4(request):
    return render(request, 'hw4.html', {
        'search': False,
    })

def get_ranking(request):
    if request.method == 'POST':
        word = request.POST.get('words')
    cancer_file = 'data/cancer.json'
    hemodialysis_file = 'data/hemodialysis.json'
    N = process_text(cancer_file)
    DF = calculate_df(N)
    total_vocal = [x for x in DF]
    calculate_dfidf(N)
    calculate_dfidf_title(N)
    merge_weight()


#  below is the calculate function

def match_score(query):
    preprocessed_query = preprocess(query)
    tokens = word_tokenize(str(preprocessed_query))
    print("Matching Score")
    print("\nQuery:", query)
    print("")
    print(tokens)
    query_weights = {}
    for key in TF_IDF:
        if key[1] in tokens:
            try:
                query_weights[key[0]] += TF_IDF[key]
            except:
                query_weights[key[0]] = TF_IDF[key]
    
    query_weights = sorted(query_weights.items(), key=lambda x: x[1], reverse=True)
    print("")
    l = []
    for i in query_weights[:10]:
        l.append(i[0])
    print(l)

def text_prepare(text):
    lower = text.lower()
    replace_by_spaces = REPLACE_BY_SPACE_RE.sub(" ", lower)
    bad_symbols = BAD_SYMBOLS_RE.sub(" ", replace_by_spaces)
    text = ' '.join([word for word in bad_symbols.split() if word not in STOPWORDS])
    return text

def stemming(data):
    stemmer = PorterStemmer()
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + stemmer.stem(w)
    return new_text

def preprocess(data):
    data = text_prepare(data)
    data = stemming(data)
    return data

def process_text(filepath):
    with open(filepath) as file:
        jsondata = json.loads(file.read())
        N = len(jsondata)
        title = [preprocess(x['title']) for x in jsondata]
        content = [preprocess(x['content']) for x in jsondata]
        for i in title:
            processed_title.append(word_tokenize(str(i)))
        for i in content:
            processed_text.append(word_tokenize(str(i)))
        # print(processed_title)
        # print(processed_text)
        return N

def calculate_df(num):
    for i in range(num):
        tokens = processed_title[i]
        for w in tokens:
            try:
                DF[w].add(i)
            except:
                DF[w] = {i}
        tokens = processed_text[i]
        for w in tokens:
            try:
                DF[w].add(i)
            except:
                DF[w] = {i}
    for i in DF:
        DF[i] = len(DF[i])
    return DF

def calculate_dfidf(num):
    doc = 0
    for i in range(num):
        tokens = processed_text[i]
        counter = Counter(tokens + processed_title[i]) # 計算加入標題後字的數量
        words_count = len(tokens + processed_title[i]) # 加入標題後的總字數
        for token in np.unique(tokens):
            tf = counter[token]  / words_count
            df = doc_freq(token)
            idf = np.log((num + 1) / (df + 1))
            TF_IDF[doc, token] = tf * idf
        doc += 1

def calculate_dfidf_title(num):
    doc = 0
    for i in range(num):
        tokens = processed_title[i]
        counter = Counter(tokens + processed_text[i]) # 計算加入內文後字的數量
        words_count = len(tokens + processed_text[i]) # 加入內文後的總字數
        for token in np.unique(tokens):
            tf = counter[token]  / words_count
            df = doc_freq(token)
            idf = np.log((num + 1) / (df + 1))
            TF_IDF_TITLE[doc, token] = tf * idf
        doc += 1

def doc_freq(word):
    c = 0
    try:
        c = DF[word]
    except:
        pass
    return c

def merge_weight():
    for i in TF_IDF:
        TF_IDF[i] *= 0.3
    for i in TF_IDF_TITLE:
        TF_IDF[i] = TF_IDF_TITLE[i]