import ijson
import nltk
from nltk.tokenize import word_tokenize
import spacy
import json
from nltk.corpus import stopwords
import wordcloud
import matplotlib
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import re

nltk.download('wordnet')
nltk.download('punkt')
nlp = spacy.load("en_core_web_sm")
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

keywords = ['need', 'shortage', 'shortages', 'short supply', 'out of stock', 'running low', 'ran low', 'can\'t find', 'couldn\'t find', 
            'supply shortage', 'inventory shortage', 'limited supply', 'scarce', 'hard to find', 'sold out', 'backorder', 
            'delayed delivery', 'production delay', 'out of production', 'discontinued', 'unavailable', 
            'short on supply', 'low inventory', 'running out of', 'ran out of', 'can\'t get', 'couldn\'t get', 
            'out of circulation', 'stockout', 'depleted', 'unfulfilled orders', 'unmet demand', 'scarcity', 
            'limited availability', 'insufficient supply', 'backlogged', 'short-supplied', 'out-of-print', 
            'understocked', 'unavailable inventory', 'supply chain disruption', 'shipping delay', 
            'production backlog', 'out-of-stock items', 'out of stock', 'low stock', 'low supply', 'out-of-stock situation', 
            'inventory issues', 'supply problems', 'insufficient stock', 'insufficient inventory', 'supply chain disruption', 'supply chain crisis',
            'limited', 'ran short', 'scarce resources', 'short on hand', 'deficient supply', 'depleted stocks',
            'sold-out inventory', 'hard to come by', 'inventory drought', 'low availability', 'short in supply',
            'out-of-stock condition', 'backorder situation', 'delivery delay', 'product shortage', 
            'insufficient supply chain', 'unavailable', 'insufficient', "not available", "empty shelves", "panic buying",
            "hoarding", "hard to find", "need more", "hunting for", "seeking", "need more", "needed more", "needing more",
            "running low on", "ran low on", "running low",
            "almost out of", "was almost out of", "almost running out of",
            "depleted supply of", "supply depleted", "depleting supply of",
            "insufficient stock of", "stock was insufficient", "insufficiently stocked",
            "low quantity of", "quantity was low", "quantities running low",
            "inadequate supply of", "supply was inadequate", "inadequately supplied",
            "dwindling inventory of", "inventory dwindled", "inventory is dwindling",
            "scarce amount of", "amount was scarce", "scarcely supplied",
            "short supply of", "supply was short", "supplies running short",
            "out of stock", "ran out of stock", "running out of stock",
            "limited stock", "stock was limited", "stock is limited",
            "not enough", "wasn't enough", "not sufficient",
            "hard to find", "was hard to find", "finding it hard",
            "can't find", "couldn't find", "unable to find",
            "sold out", "was sold out", "selling out",
            "empty shelves", "shelves were empty", "shelves emptying",
            "supply chain issues", "had supply chain issues", "experiencing supply chain issues",
            "backordered", "was backordered", "backordering",
            "delayed shipment", "shipment was delayed", "shipments delayed",
            "waiting for restock", "restock was awaited", "awaiting restock",
            "where to buy", "where to purchase", "where to find",
            "looking for", "looked for", "looking out for",
            "seeking", "sought", "seeking out",
            "hunting for", "hunted for", "hunting down",
            "scarcity", "experiencing scarcity", "scarce supplies"]

keywords = list(set(keywords))

hashtags = [
    'shortage', 'outofstock', 'runninglow', 'cantfind', 'supplyshortage', 
    'inventoryshortage', 'limitedsupply', 'scarce', 'hardtofind', 'soldout', 
    'backorder', 'delayeddelivery', 'productiondelay', 'outofproduction', 
    'unavailable', 'shortonsupply', 'lowinventory', 'runningoutof', 
    'cantget', 'emptyshelves', 'panicbuying'
]

combined_patterns = '|'.join(keywords)

words = '\\b(' + combined_patterns + ')\\b'

# Part 1 : the first 1,000,000 tweets

with open('/content/drive/MyDrive/CC_Twitter/twitter-huge.json', 'r') as f, open("/content/drive/MyDrive/CC_Twitter/shortage_tweets.json", "w") as outfile:
    parser = ijson.items(f, 'rows.item')
    twitterdata = []
    for i, tweet in enumerate(parser):
      if i < 1000000:
        sentiment = tweet['doc']['data']['sentiment']
        text = tweet['doc']['data']['text']
        cleaned_text = re.sub(r'@\w+|https?://\S+', '', text)
        language = tweet["doc"]["data"]["lang"]
        twitter = {"text" : cleaned_text, "sentiment" : sentiment, "language" : language}
        twitterdata.append(twitter)
      else:
        break

    twitter_df = pd.DataFrame(twitterdata)

reduced_df = twitter_df[(twitter_df['language']=="en") & (twitter_df['text'].str.len() != 0)]

keys_df = reduced_df[reduced_df['text'].str.contains(words, case=False)]

# Part 2: the next 1,000,000 tweets

with open('/content/drive/MyDrive/CC_Twitter/twitter-huge.json', 'r') as f, open("/content/drive/MyDrive/CC_Twitter/shortage_tweets.json", "w") as outfile:
    parser = ijson.items(f, 'rows.item')
    twitterdata = []
    for i, tweet in enumerate(parser):
      if i < 1000000:
        continue
      if (i >= 1000000) and (i < 2000000): 
        sentiment = tweet['doc']['data']['sentiment'] 
        # tokens = tweet['value']['tokens'].replace("|", ",")
        # tokens = tokens.lower()
        text = tweet['doc']['data']['text']
        cleaned_text = re.sub(r'@\w+|https?://\S+', '', text)
        language = tweet["doc"]["data"]["lang"]
        twitter = {"text" : cleaned_text, "sentiment" : sentiment, "language" : language}
        twitterdata.append(twitter)
      else:
        break

    twitter_df = pd.DataFrame(twitterdata)

reduced_df = twitter_df[(twitter_df['language']=="en") & (twitter_df['text'].str.len() != 0)]

keys_df_2 = reduced_df[reduced_df['text'].str.contains(words, case=False)]

keys_twitter = pd.concat([keys_df, keys_df_2])


# Part 3: the next 1,000,000 tweets
with open('/content/drive/MyDrive/CC_Twitter/twitter-huge.json', 'r') as f, open("/content/drive/MyDrive/CC_Twitter/shortage_tweets.json", "w") as outfile:
    parser = ijson.items(f, 'rows.item')
    twitterdata = []
    for i, tweet in enumerate(parser):
      if i < 2000000:
        continue
      if (i >= 2000000) and (i < 3000000): 
        sentiment = tweet['doc']['data']['sentiment'] 
        # tokens = tweet['value']['tokens'].replace("|", ",")
        # tokens = tokens.lower()
        text = tweet['doc']['data']['text']
        cleaned_text = re.sub(r'@\w+|https?://\S+', '', text)
        language = tweet["doc"]["data"]["lang"]
        twitter = {"text" : cleaned_text, "sentiment" : sentiment, "language" : language}
        twitterdata.append(twitter)
      else:
        break

    twitter_df = pd.DataFrame(twitterdata)

reduced_df = twitter_df[(twitter_df['language']=="en") & (twitter_df['text'].str.len() != 0)]

keys_df_3 = reduced_df[reduced_df['text'].str.contains(words, case=False)]

keys_twitter = pd.concat([keys_twitter, keys_df_3])

# Create bag of words

all_texts = keys_twitter['text'].str.cat(sep=" ")

all_texts = re.sub(r'[^\w\s]', '', all_texts)

tokenized_texts = word_tokenize(all_texts.lower())

filtered_texts = [word for word in tokenized_texts if not word in stop_words]

unique_texts = set(filtered_texts)

bag_of_words = {key: 0 for key in unique_texts}
for word in filtered_texts:
    bag_of_words[word] += 1

# Rank bag of words
rank_tokens = sorted(bag_of_words.items(), key=lambda x:x[1], reverse=True)

# Only keep the nouns
nouns = []
for word, freq in rank_tokens:
  doc = nlp(word)
  if any(token.pos_ == "NOUN" for token in doc):
    nouns.append((word, freq))

# Remove non-meaningful words
removed_words = ['team','story','sets','none','text','load','cock','seat','core','crap','fans','amount','rate','front','type','moment','lots','name','sense','woman','word','deal','plan','test','tomorrow','tonight','chance','people', 'time', 'day', 'way','things','year','life','today','thing','world','lot','years','days', 'women','content','lol','week','thanks', 'kids','man','bit','person','end', 'place','parts','other', 'system','part','others','family','times','party','battle', 'problem','election','twitter','head','children','news','stuff','lvl','future','shortage','friends','issues','men','mate','attention','ones','access','state','reason','food','project','online','case','guys','research','months','question','shortages','fun','hours','video','rest','issue','night','war','fact','hell', 'account','past','fuck','share','side','post','line','number','level','bill','weeks','course', 'mind','tests','price','list','season','self','nsw','step','body','risk','group','guy','half','term','tax','couple','details']

final_words = {}
i = 0
for (word,count) in nouns:
  if (word not in removed_words) and (len(word) >3):
    i += 1
    if i < 100:
        final_words[word] = count
    else:
      break

# Convert data to the form that can be stored in CouchDB
complete_data = {"docs" : []}
for key in final_words:
  word_dic = {'word' : key, 'count' : final_words[key]}
  complete_data["docs"].append(word_dic)


# Also, save data in JSON file
with open('/content/drive/MyDrive/CC_Twitter/words_for_cloud.json', 'w') as f:
  json.dump(complete_data, f)


# Create a word cloud
wordcloud = WordCloud(colormap='gist_rainbow', width=600, height=400)
wordcloud.generate_from_frequencies(final_words)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

wordcloud.to_file("/content/drive/MyDrive/CC_Twitter/shortage_wordcloud.png")