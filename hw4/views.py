from django.shortcuts import render
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter
import numpy as np
import json
import re
import math

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

processed_title = []
processed_text = []
total_vocab = []

DF = {}
TF_IDF = {}
TF_IDF_TITLE = {}
N = 0

# Create your views here.
def hw4(request):
    return render(request, 'hw4.html', {
        'search': False,
    })

#  below is the calculate function
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

def calculate_dfidf(method, num):
    doc = 0
    for i in range(num):
        tokens = processed_text[i]
        counter = Counter(tokens + processed_title[i]) # 計算加入標題後字的數量
        words_count = len(tokens + processed_title[i]) # 加入標題後的總字數
        for token in np.unique(tokens):
            df = doc_freq(token)
            if method == 1:     # term frequency
                tf = counter[token] / words_count
                idf = np.log((num + 1) / (df + 1))
                TF_IDF[doc, token] = tf * idf
            elif method == 2:   # frequency
                tf = counter[token]  / words_count
                TF_IDF[doc, token] = np.log(1 + tf)
            elif method == 3:   # augmented frequency
                tf = 1 + np.log(counter[token] / words_count)
                idf = np.log((num + 1) / (df + 1))
                TF_IDF[doc, token] = tf * idf
        doc += 1
    return TF_IDF

def calculate_dfidf_title(method, num):
    doc = 0
    for i in range(num):
        tokens = processed_title[i]
        counter = Counter(tokens + processed_text[i]) # 計算加入內文後字的數量
        words_count = len(tokens + processed_text[i]) # 加入內文後的總字數
        for token in np.unique(tokens):
            tf = counter[token]  / words_count
            df = doc_freq(token)
            if method == 1:     # log frequency
                idf = np.log((num + 1) / (df + 1))
            elif method == 2:   # frequency
                idf = (num + 1) / (df + 1)
            elif method == 3:   # augmented frequency
                idf = 0.5 + 0.5 * (num + 1) / (df + 1)/np.max((num + 1) / (df + 1))
            TF_IDF_TITLE[doc, token] = tf * idf
        doc += 1
    return TF_IDF_TITLE

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

def match_score(query):
    preprocessed_query = preprocess(query)
    tokens = word_tokenize(str(preprocessed_query))
    print("Matching Score")
    print("Query:", query)
    print(tokens)
    query_weights = {}
    for key in TF_IDF:
        if key[1] in tokens:
            try:
                query_weights[key[0]] += TF_IDF[key]
            except:
                query_weights[key[0]] = TF_IDF[key]   
    query_weights = sorted(query_weights.items(), key=lambda x: x[1], reverse=True)
    l = []
    for i in query_weights[:10]:
        l.append(i[0])
    print(l)

def cosine_sim(a, b):
    cos_sim = np.dot(a, b)/(np.linalg.norm(a) * np.linalg.norm(b))
    return cos_sim

def vector_tfidf(num, total_vocab, total_vocab_size):
    D = np.zeros((num, total_vocab_size))
    for i in TF_IDF:
        try:
            ind = total_vocab.index(i[1])
            D[i[0]][ind] = TF_IDF[i]
        except:
            pass
    return D

def gen_vector(num, tokens, total_vocab):
    Q = np.zeros((len(total_vocab)))
    counter = Counter(tokens)
    words_count = len(tokens)
    for token in np.unique(tokens):
        tf = counter[token] / words_count
        df = doc_freq(token)
        idf = math.log((num + 1)/( df +1))
        try:
            ind = total_vocab.index(token)
            Q[ind] = tf * idf
        except:
            pass
    return Q

def cosine_similarity(D, query, total_vocab):
    print("Cosine Similarity")
    preprocessed_query = preprocess(query)
    tokens = word_tokenize(str(preprocessed_query))
    print("Query:", query)
    print(tokens)
    d_cosines = []
    query_vector = gen_vector(398, tokens, total_vocab)
    for d in D:
        d_cosines.append(cosine_sim(query_vector, d)) 
    similarity = np.sort(d_cosines)[-10:][::-1] 
    out = np.array(d_cosines).argsort()[-10:][::-1] # 最相似的十個再倒序
    print(out)
    return out, similarity

def get_doc(filepath, id_list, similarity):
    with open(filepath) as file:
        jsondata = json.loads(file.read())
        article = []
        counter = 0
        for id in id_list:
            data = jsondata[id]
            data['similarity'] = similarity[counter]
            counter += 1
            print("Category:", data['category'])
            # print(data)
            article.append(data)
        return article

def get_ranking(request):
    if request.method == 'POST':
        word = request.POST.get('words')
        option = request.POST.get('options')
        method = int(option)
    all_article = 'hw4/data/all_articles.json'
    N = process_text(all_article)
    print(N)
    DF = calculate_df(N)
    total_vocab = [x for x in DF]
    total_vocab_size = len(total_vocab)
    calculate_dfidf(method, N)
    calculate_dfidf_title(method, N)
    merge_weight()
    # print(len(TF_IDF))
    match_score(word)
    D = vector_tfidf(N, total_vocab, total_vocab_size)
    top_list, similarity= cosine_similarity(D, word, total_vocab)
    articles = get_doc(all_article, top_list, similarity)
    return render(request, 'hw4.html', {
        'search': True,
        'query': word,
        'articles': articles,
        'method': method,
    })