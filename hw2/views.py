from django.shortcuts import render, redirect
from django.http import HttpResponse
import xml.etree.ElementTree as ET
import json
import requests
from metapub import PubMedFetcher

# Create your views here.
def hw2(request):
    content = getPubMedContent()
    return render(request, 'hw2.html', {
        'uploaded': False,
        "content": content,
    })

def getPubMed():
    db = "pubmed"
    query = "monkeypox"
    base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    url = base + "esearch.fcgi?db=" + db + "&term=" + query + "&retmode=json"+ "&reldate=360&datetype=pdat" + "&retmax=100" + "&usehistory=y"
    re = requests.get(url)
    result = re.text
    data = json.loads(result)
    idlist = data['esearchresult']['idlist']
    string = ""
    lastone = idlist[len(idlist) - 1]
    for item in idlist:
        if item == lastone:
            string = string + item
        else:
            string = string + item + ","
    return string

def getPubMedContent():
    keyword = "Monkeypox"
    fetch = PubMedFetcher()
    pmids = fetch.pmids_for_query(keyword, retmax=5000)
    abstracts = {}
    for pmid in pmids:
        abstracts[pmid] = fetch.article_by_pmid(pmid).abstract
    print(abstracts)
    return abstracts