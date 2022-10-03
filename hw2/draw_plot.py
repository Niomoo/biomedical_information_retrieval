from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np

def getWordList(content):
    words = Counter(content.split())
    top_words = words.most_common()
    return top_words

def drawZipf(frequency):
    zipf_table = []
    top_frequency = frequency[0][1]
    for index, item in enumerate(frequency, start=1):
        relative_frequency = "1/{}".format(index)
        zipf_frequency = top_frequency * (1 / index)
        difference_actual = item[1] - zipf_frequency
        difference_percent = (item[1] / zipf_frequency) * 100
        zipf_table.append({"word": item[0], 
                            "actual_frequency": item[1],
                            "relative_frequency": relative_frequency,
                            "zipf_frequency": zipf_frequency,
                            "difference_actual": difference_actual,
                            "difference_percent": difference_percent,
        })
    df = pd.DataFrame(zipf_table)
    return df

def drawPubMedZipf(df):
    plt.figure(figsize=(10,10))
    plt.plot(df['word'][:50], df['actual_frequency'][:50], color='red')
    plt.bar(df['word'][:50], df['actual_frequency'][:50], align='center', alpha=0.5)
    plt.xticks(df['word'][:50],rotation='vertical')
    plt.ylabel('Frequency')
    plt.xlabel('Top 50 tokens')
    plt.title('Top 50 tokens in PubMed')
    plt.savefig('../static/img/pubMed_zipf.png')

def drawTwitterZipf(df):
    plt.figure(figsize=(10,10))
    plt.plot(df['word'][:50], df['actual_frequency'][:50], color='red')
    plt.bar(df['word'][:50], df['actual_frequency'][:50], align='center', alpha=0.5)
    plt.xticks(df['word'][:50],rotation='vertical')
    plt.ylabel('Frequency')
    plt.xlabel('Top 50 tokens')
    plt.title('Top 50 tokens in Twitter')
    plt.savefig('../static/img/twitter_zipf.png')

with open('data/pubmed/pubmed_data.json') as file:
    data = json.loads(file.read())
    content = ''
    for text in data:
        content += text
    top_word = getWordList(content)
    df = drawZipf(top_word)
    drawPubMedZipf(df)

with open('data/tweets/tweet_data.json') as file:
    data = json.loads(file.read())
    content = ''
    for text in data:
        content += text['text']
    top_word = getWordList(content)
    df = drawZipf(top_word)
    drawTwitterZipf(df)
