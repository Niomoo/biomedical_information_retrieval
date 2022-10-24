import json

with open('pubmed_data_1000.json') as file:
    data = json.loads(file.read())
    with open('pubmed_data_1000.txt', 'w', encoding='UTF-8') as f:
        f.writelines(data)

with open('pubmed_data_5000.json') as file:
    data = json.loads(file.read())
    with open('pubmed_data_5000.txt', 'w', encoding='UTF-8') as f:
        f.writelines(data)

with open('pubmed_data_10000.json') as file:
    data = json.loads(file.read())
    with open('pubmed_data_10000.txt', 'w', encoding='UTF-8') as f:
        f.writelines(data)

