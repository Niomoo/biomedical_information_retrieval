from Bio import Entrez
from nltk.corpus import stopwords
from nltk import word_tokenize
import json

def search(query):
    Entrez.email = 'jennyliu.lyh@iir.csie.ncku.edu.tw'
    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax='1000',
                            retmode='xml', 
                            term=query)
    results = Entrez.read(handle)
    return results

def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'jennyliu.lyh@iir.csie.ncku.edu.tw'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results

results = search('breast cancer')
id_list = results['IdList']
papers = fetch_details(id_list)
abstractText = []
nltk_stopwords = set(stopwords.words('english'))
nltk_stopwords.update(['.', ',', ':', ';', '(', ')', '#', '--', '...', '"'])
for i, paper in enumerate(papers['PubmedArticle']):
    if 'Abstract' in paper['MedlineCitation']['Article']:
        content = ''
        for text in paper['MedlineCitation']['Article']['Abstract']['AbstractText']:
            for word in word_tokenize(text):
                if word not in nltk_stopwords:
                    content = content + word + ' '
        abstractText.append(content)

with open('data/pubmed_data_1000.json', 'w') as f:
    json.dump(abstractText, f, indent=2)
    # print("{}) {}".format(i+1, paper['MedlineCitation']['Article']['ArticleTitle']))
