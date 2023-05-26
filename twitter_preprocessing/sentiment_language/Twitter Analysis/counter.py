########## Writes number of tweets and number of tweets with location to tweet_count.json ##########


import json
import time
import ijson
from nltk.corpus import stopwords

start_time = time.time()
num_tweets = 0
location_tweets = 0

# most common words stored in word_dictionary
with open('data/twitter-huge.json', 'r') as f:
    parser = ijson.items(f, 'rows.item')

    for tweet in parser:
        num_tweets += 1
        if tweet.get('doc', {}).get('includes', {}):
            location_tweets += 1

dictionary = {}
dictionary['total'] = num_tweets
dictionary['with_location'] = location_tweets

with open("data/tweet_count.json", "w") as outfile:
    json.dump(dictionary, outfile)

print("total tweets     : " + str(num_tweets))
print("tweets w location: " + str(num_tweets))
end_time = time.time()
total_time = end_time - start_time
print("total time       : " + str(total_time/60)) 

