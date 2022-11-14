from nltk.corpus import stopwords
from nltk import word_tokenize
import json
import re

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

def text_prepare(text):
    """
        text: a string
        return: modified initial string
    """
    # lowercase text
    # replace REPLACE_BY_SPACE_RE symbols by space in text
    # delete symbols which are in BAD_SYMBOLS_RE from text
    # delete stopwords from text
    lower = text.lower()
    replace_by_spaces = REPLACE_BY_SPACE_RE.sub(" ", lower)
    bad_symbols = BAD_SYMBOLS_RE.sub(" ", replace_by_spaces)
    text = ' '.join([word for word in bad_symbols.split() if word not in STOPWORDS])
    return text

with open('data/pubmed_data_1000.json') as file:
    jsondata = json.loads(file.read())
    data = [text_prepare(x) for x in jsondata]
    with open('data/pubmed_data_1000.txt', 'w', encoding='UTF-8') as f:
        f.writelines("%s\n" % t for t in data)

with open('data/pubmed_data_5000.json') as file:
    jsondata = json.loads(file.read())
    data = [text_prepare(x) for x in jsondata]
    with open('data/pubmed_data_5000.txt', 'w', encoding='UTF-8') as f:
        f.writelines("%s\n" % t for t in data)

with open('data/pubmed_data_10000.json') as file:
    jsondata = json.loads(file.read())
    data = [text_prepare(x) for x in jsondata]
    with open('data/pubmed_data_10000.txt', 'w', encoding='UTF-8') as f:
        f.writelines("%s\n" % t for t in data)

