import couchdb

def tweet_shortages():
    couch = couchdb.Server('http://admin:password@172.26.136.171:5984/')
    shortage_db = couch['shortage_tweets']

    shortage_dict = {}
    for id in shortage_db:
        data = shortage_db[id]
        shortage_dict[data['word']] = data['count']

    return shortage_dict

if __name__ == "__main__":
    print(tweet_shortages())

