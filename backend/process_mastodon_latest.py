import couchdb
import pandas as pd
import re
from nltk.tokenize import word_tokenize
import spacy
import nltk
from nltk.corpus import stopwords

def process_mastodon_latest():
    nltk.download('punkt')
    nltk.download('wordnet')
    nlp = spacy.load("en_core_web_sm")
    nltk.download('stopwords')

    # Get data from couch DB and store them in a pandas dataframe
    couch = couchdb.Server('http://admin:password@172.26.136.171:5984/')
    shortage_db = couch['shortage_mastodon']

    changes = shortage_db.changes(descending=True, limit=300)['results']

    shortage_list = []
    for change in changes:
        id = change['id']
        data = shortage_db[id]
        shortage_dict = {'content': data['content'], 'tags': data['tags']}
        shortage_list.append(shortage_dict)

    shortage_df = pd.DataFrame(shortage_list)

    # Analyse the data
    # Combine all words
    shortage_df['content'] = shortage_df['content'].astype(str)
    all_contents = shortage_df['content'].str.cat(sep=" ")

    all_tags = shortage_df['tags'].explode('tags')
    all_tags = all_tags.str.cat(sep=' ')

    all_words = all_contents + ' ' + all_tags

    # preprocess
    all_words = re.sub(r'[^\w\s]', '', all_words)

    stop_words = set(stopwords.words('english'))

    tokenized_texts = word_tokenize(all_words.lower())
    filtered_texts = [word for word in tokenized_texts if not word in stop_words]
    unique_texts = set(filtered_texts)

    # create bag of words
    bag_of_words = {key: 0 for key in unique_texts}
    for word in filtered_texts:
        bag_of_words[word] += 1

    # rank words
    rank_tokens = sorted(bag_of_words.items(), key=lambda x:x[1], reverse=True)

    # extract only Noun words
    nouns = []
    i = 0
    for word, freq in rank_tokens:
        i += 1
        if i < 500:
            doc = nlp(word)
            if any(token.pos_ == "NOUN" for token in doc):
                nouns.append((word, freq))
        else:
            break


    # Remove irrelevant words
    removed_words = ['team','story','sets','none','text','load','cock','seat','core','crap','fans','amount','rate','front','type','moment','lots','name','sense','woman','word','deal','plan','test','tomorrow','tonight','chance','people', 'time', 'day', 'way','things','year','life','today','thing','world','lot','years','days', 'women','content','lol','week','thanks', 'kids','man','bit','person','end', 'place','parts','other', 'system','part','others','family','times','party','battle', 'problem','election','twitter','head','children','news','stuff','lvl','future','shortage','friends','issues','men','mate','attention','ones','access','state','reason','food','project','online','case','guys','research','months','question','shortages','fun','hours','video','rest','issue','night','war','fact','hell', 'account','past','fuck','share','side','post','line','number','level','bill','weeks','course', 'mind','tests','price','list','season','self','nsw','step','body','risk','group','guy','half','term','tax','couple','details']
    final_words = {}
    i = 0
    for (word,count) in nouns:
        if (word not in removed_words) and (len(word) >3) and ('39' not in word): #there are words like they39r, we39re, there39s etc.
            i += 1
            if i < 100:
                final_words[word] = count
            else:
                break

    return final_words

if __name__ == '__main__':
    s = process_mastodon()

    print(s)
