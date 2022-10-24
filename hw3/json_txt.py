import json

with open('data/pubmed_data_1000.json') as file:
    data = json.loads(file.read())
    with open('data/pubmed_data_1000.txt', 'w', encoding='UTF-8') as f:
        f.writelines("%s\n" % t for t in data)

with open('data/pubmed_data_5000.json') as file:
    data = json.loads(file.read())
    with open('data/pubmed_data_5000.txt', 'w', encoding='UTF-8') as f:
        f.writelines("%s\n" % t for t in data)

with open('data/pubmed_data_10000.json') as file:
    data = json.loads(file.read())
    with open('data/pubmed_data_10000.txt', 'w', encoding='UTF-8') as f:
        f.writelines("%s\n" % t for t in data)

