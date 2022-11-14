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
    cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
    return cos_sim

def vector_tfidf(total_vocab, total_vocab_size):
    D = np.zeros((N, total_vocab_size))
    for i in TF_IDF:
        try:
            ind = total_vocab.index(i[1])
            D[i[0]][ind] = TF_IDF[i]
        except:
            pass
    return D

def gen_vector(tokens):
    Q = np.zeros((len(total_vocab)))
    counter = Counter(tokens)
    words_count = len(tokens)
    query_weights = {}
    for token in np.unique(tokens):
        tf = counter[token] / words_count
        df = doc_freq(token)
        idf = math.log((N + 1)/( df +1))
        try:
            ind = total_vocab.index(token)
            Q[ind] = tf * idf
        except:
            pass
    return Q

def cosine_similarity(D, k, query):
    print("Cosine Similarity")
    preprocessed_query = preprocess(query)
    tokens = word_tokenize(str(preprocessed_query))
    print("Query:", query)
    print(tokens)
    d_cosines = []
    query_vector = gen_vector(tokens)
    for d in D:
        d_cosines.append(cosine_sim(query_vector, d))   
    out = np.array(d_cosines).argsort()[-k:][::-1]
    print(out)

def get_doc(filepath, id):
    with open(filepath) as file:
        jsondata = json.loads(file.read())
        title = jsondata[id]['title']
        content = jsondata[id]['content']
        print("Title:", title)
        print(content)

cancer_file = 'data/cancer.json'
hemodialysis_file = 'data/hemodialysis.json'
N = process_text(cancer_file)
DF = calculate_df(N)
total_vocab = [x for x in DF]
total_vocab_size = len(total_vocab)
calculate_dfidf(N)
calculate_dfidf_title(N)
merge_weight()
print(len(TF_IDF))
match_score("Birth defects are established risk factors for childhood cancer.")
D = vector_tfidf(total_vocab, total_vocab_size)
cosine_similarity(D, 10, "Birth defects are established risk factors for childhood cancer.")
get_doc(cancer_file, 7)