import json
  
# dictionary where the lines from
# text will be stored
dict1 = {}
tweet = []
fields =['name', 'account', 'split', 'timestamp', 'text']
# creating dictionary
l = 1
for i in range(1, 11):
    with open('data/tweets/tweet'+str(i)+'.txt', encoding="utf-8") as f:
        counter = 1
        for line in f:
            if line.startswith('\n'):
                continue
            if line.startswith('-----'):
                counter = 1
                tweet.append(dict1)
                dict1 = {}
                continue
            field = (counter-1) % 5
            if field < 4:
                dict1[fields[field]] = line
                counter += 1
            else:
                if fields[field] in dict1:
                    dict1[fields[field]] += line
                else:
                    dict1[fields[field]] = line
        tweet.append(dict1)

out_file = open("data/tweets/tweet_data.json", "w")
json.dump(tweet, out_file, indent = 4, sort_keys = False)
out_file.close()