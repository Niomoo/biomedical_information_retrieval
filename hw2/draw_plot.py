from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np
from porter import PorterStemmer

class WordCounter:
    def getWordList(content):
        words = Counter(content.split())
        top_words = words.most_common()
        return top_words

    def getPorterStemming(content):
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

    def list_to_df(frequency):
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
        plt.figure(figsize=(12,8))
        plt.plot(df['word'][:50], df['actual_frequency'][:50], color='red')
        plt.bar(df['word'][:50], df['actual_frequency'][:50], align='center', alpha=0.5)
        plt.xticks(df['word'][:50],rotation='vertical')
        plt.ylabel('Frequency')
        plt.xlabel('Top 50 tokens')
        plt.title('Top 50 tokens in PubMed')
        plt.tight_layout()
        plt.savefig('../static/img/pubMed_zipf.png')

    def drawPubMedPorter(df):
        plt.figure(figsize=(12,8))
        plt.plot(df['word'][:50], df['actual_frequency'][:50], color='red')
        plt.bar(df['word'][:50], df['actual_frequency'][:50], align='center', alpha=0.5)
        plt.xticks(df['word'][:50],rotation='vertical')
        plt.ylabel('Frequency')
        plt.xlabel('Top 50 tokens')
        plt.title('Top 50 tokens in PubMed using Porter Algorithm')
        plt.tight_layout()
        plt.savefig('../static/img/pubMed_porter.png')

    def drawTwitterZipf(df):
        plt.figure(figsize=(12,8))
        plt.plot(df['word'][:50], df['actual_frequency'][:50], color='red')
        plt.bar(df['word'][:50], df['actual_frequency'][:50], align='center', alpha=0.5)
        plt.xticks(df['word'][:50],rotation='vertical')
        plt.ylabel('Frequency')
        plt.xlabel('Top 50 tokens')
        plt.title('Top 50 tokens in Twitter')
        plt.tight_layout()
        plt.savefig('../static/img/twitter_zipf.png')

    def drawTwitterPorter(df):
        plt.figure(figsize=(12,8))
        plt.plot(df['word'][:50], df['actual_frequency'][:50], color='red')
        plt.bar(df['word'][:50], df['actual_frequency'][:50], align='center', alpha=0.5)
        plt.xticks(df['word'][:50],rotation='vertical')
        plt.ylabel('Frequency')
        plt.xlabel('Top 50 tokens')
        plt.title('Top 50 tokens in Twitter using Porter Algorithm')
        plt.tight_layout()
        plt.savefig('../static/img/twitter_porter.png')

# with open('data/pubmed/pubmed_data.json') as file:
#     data = json.loads(file.read())
#     content = ''
#     for text in data:
#         content += text
#     top_word = WordCounter.getWordList(content)
#     stem_word = WordCounter.getPorterStemming(content)
#     zipf_df = WordCounter.list_to_df(top_word)
#     porter_df = WordCounter.list_to_df(stem_word)
#     WordCounter.drawPubMedZipf(zipf_df)
#     WordCounter.drawPubMedPorter(porter_df)

# with open('data/tweets/tweet_data.json') as file:
#     data = json.loads(file.read())
#     content = ''
#     for text in data:
#         content += text['text']
#     top_word = WordCounter.getWordList(content)
#     stem_word = WordCounter.getPorterStemming(content)
#     zipf_df = WordCounter.list_to_df(top_word)
#     porter_df = WordCounter.list_to_df(stem_word)
#     WordCounter.drawTwitterZipf(zipf_df)
#     WordCounter.drawTwitterPorter(porter_df)
