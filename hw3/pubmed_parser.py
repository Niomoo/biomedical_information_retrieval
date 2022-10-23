from Bio import Entrez
import json

def search(query):
    Entrez.email = 'jennyliu.lyh@iir.csie.ncku.edu.tw'
    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax='10000',
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
for i, paper in enumerate(papers['PubmedArticle']):
    if 'Abstract' in paper['MedlineCitation']['Article']:
        content = ''
        for text in paper['MedlineCitation']['Article']['Abstract']['AbstractText']:
            content += text
        abstractText.append(content)

with open('pubmed_data_10000.json', 'w') as f:
    json.dump(abstractText, f, indent=2)
    # print("{}) {}".format(i+1, paper['MedlineCitation']['Article']['ArticleTitle']))
