########## Writes words and the number of times they appear in the file to word_dictionary_pos.json ##########


import json
import time
import nltk
import ijson
from nltk.corpus import stopwords

start_time = time.time()
stop_words = set(stopwords.words('english'))
word_list = {}    

count = 0
with open('data/twitter-huge.json', 'r') as f:
    # Create an ijson parser that iterates over each tweet object
    parser = ijson.items(f, 'rows.item')

    for tweet in parser:
        if tweet.get('value', {}).get('tokens', {}):
            token_list = tweet.get('value', {}).get('tokens', {})
            tokens = token_list.split('|')
            tokens = list(set(tokens))
            pos_tags = nltk.pos_tag(tokens)
            pos_tags = [(t[0].lower(), *map(str.lower, t[1:])) for t in pos_tags]
            count += 1
            for word in pos_tags:
                if word[0] in stop_words:
                    continue
                else:
                    if word in word_list.keys():
                        word_list[word] += 1
                    else:
                        word_list[word] = 1


sorted_dictionary = dict(sorted(word_list.items(), key = lambda x: x[1], reverse = True))
            
with open("data/word_dictionary_pos.json", "w") as outfile:
    # write dictionary to file
    json.dump(sorted_dictionary, outfile)
        
end_time = time.time()
total_time = end_time - start_time
print("total time: " + str(total_time/60)) 

