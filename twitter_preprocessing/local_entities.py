import json
import ijson
import re
import nltk
import spacy
import csv
import time
import multiprocessing
from collections import defaultdict

start_time = time.time()
nlp = spacy.load('en_core_web_sm')
entity_csv = 'data/entities7.csv'
# hashtag_csv = 'data/hashtags.csv'


# Compile regular expressions
url_regex = re.compile(r'http\S+')
username_regex = re.compile(r'@[^\s]+')
hashtag_regex = re.compile(r'#')
newline_regex = re.compile(r'\n')
emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    u"\U00002500-\U00002BEF"  # chinese char
    u"\U00002702-\U000027B0"
    u"\U00002702-\U000027B0"
    u"\U000024C2-\U0001F251"
    u"\U0001f926-\U0001f937"
    u"\U00010000-\U0010ffff"
    u"\u200d"
    u"\u2640-\u2642"
    u"\u2600-\u2B55"
    u"\u23cf"
    u"\u23e9"
    u"\u231a"
    u"\u3030"
    u"\ufe0f"
    "]", flags=re.UNICODE)

# Define preprocess_string function using precompiled regex patterns
def preprocess_string(string):
    # Remove URLs
    string = url_regex.sub('', string)
    # Remove usernames
    string = username_regex.sub('', string)
    # Remove hashtags
    string = hashtag_regex.sub('', string)
    # Remove newline characters
    string = newline_regex.sub(' ', string)
    # Remove emojis
    string = emoji_pattern.sub('', string)
    return string


# def hashtag_dict_count(string_list, hashtag_dict):
#     for word in string_list:
#         if word[0] == '#':
#             hashtag_dict[word[1:].lower()] += 1


def get_named_entities(text):
    FOCUSED_LABELS = ['GPE', 'NORP', 'EVENT']
    #IGNORED_LABELS = ['CARDINAL', 'ORDINAL', 'DATE', 'TIME', 'PERCENT']

    doc = nlp(text)
    named_entities = set()
    for ent in doc.ents:
        if (ent.label_ in FOCUSED_LABELS):
            named_entities.add((ent.text, ent.label_))
    return named_entities


def entity_dict_count(entity_list, entity_dict):
    for entity in entity_list:
        key = (entity[0].lower(), entity[1])
        if (key in entity_dict):
            num = entity_dict[key]
            entity_dict[key] += 1
        else:
            entity_dict[key] = 1


def process_tweet(tweet):
    string = tweet.get('doc', {}).get('data', {}).get('text', {})

    preprocessed_string = preprocess_string(string)
    named_entities = get_named_entities(preprocessed_string)

    return named_entities
    #return string, named_entities


def sort_dict(entity_dict):#, hashtag_dict):
    entity = dict(sorted(entity_dict.items(), key=lambda item: item[1], reverse=True))
    #hashtag = dict(sorted(hashtag_dict.items(), key=lambda item: item[1], reverse=True))

    return entity#, hashtag


# hashtag_dict = defaultdict(int)
entity_dict = defaultdict(int)


if __name__ == '__main__':
    pool = multiprocessing.Pool()
    results = []
    
    # Write the tweets with location to a different .json file
    with open('data/twitter-huge.json', 'r') as f:
        parser = ijson.items(f, 'rows.item')

        count = 0

        for tweet in parser:
            count += 1

            #if (count > 40000000):

            result = pool.apply_async(process_tweet, (tweet,))
            results.append(result)

            if count == 100:
                break

    for result in results:
        named_entities = result.get()
        #string, named_entities = result.get()

        # if ('#' in string):
        #     hashtag_dict_count(string.split(), hashtag_dict)

        entity_dict_count(named_entities, entity_dict)

    entities_to_delete = []
    for entity in entity_dict:
        num = entity_dict[entity]

        if num == 1:
            entities_to_delete.append(entity)

    for entity in entities_to_delete:
        del entity_dict[entity]

    #hashtag_dict = {key: value for key, value in hashtag_dict.items() if value != 1}

    result = pool.apply_async(sort_dict, (entity_dict,))#, hashtag_dict))

    pool.close()
    pool.join()

    sorted_entities = result.get()
    #sorted_entities, sorted_hashtags = result.get()

    with open(entity_csv, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(['Entity', 'Entity Type', 'Number of Tweets'])

        for entity in sorted_entities:
            ent_data = sorted_entities[entity]
            newline = [entity[0], entity[1], ent_data]
            writer.writerow(newline)


    # with open(hashtag_csv, "w", newline="") as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['Hashtags', 'Number of Tweets'])

    #     for hashtag in sorted_hashtags:
    #         writer.writerow([hashtag, sorted_hashtags[hashtag]])

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("Elapsed time: ", elapsed_time)