import couchdb

COUCHDB_SERVER='http://admin:password@172.26.136.171:5984/'
server = couchdb.Server(COUCHDB_SERVER)

def entities_toots():
    toots = server['entities_mastodon'].view('filter/entities_toots', group=True)
    data_list = []

    for row in toots:
        entity = row['key'][0]
        entity_type = row['key'][1]
        count = row['value']
        data = {'Entity': entity, 'Entity Type': entity_type, 'Number of Tweets': count}

        data_list.append(data)

    return data_list

def hashtags_toots():
    toots = server['hashtags_mastodon'].view('filter/hashtags_toots', group=True)
    data_list = []

    for row in toots:
        hashtag = row['key']
        count = row['value']
        data = {'Hashtag': hashtag, 'Number of Tweets': count}

        data_list.append(data)

    return data_list

def english_view():
    english_view = server['english_tweets'].view('filter/english_view', reduce=False)

    labels = ["total_tweets", "eng_tweets", "eng_tweets_percentage"]
    data_dict = {}

    for label in labels:
        data_dict[label] = {}

    for row in english_view:
        state = row['key']
        value = row['value']
        for i in range(len(labels)):
            if state not in data_dict[labels[i]]:
                data_dict[labels[i]][state] = {}
            data_dict[labels[i]][state] = value[i]

    return data_dict


def foreigner_view():
    foreigner_view = server['foreigner_sudo'].view('filter/foreigner_view', reduce=False)

    labels = ["local_people", "foreign_people", "foreign_people_percentage"]
    data_dict = {}

    for label in labels:
        data_dict[label] = {}

    for row in foreigner_view:
        state = row['key']
        value = row['value']
        for i in range(len(labels)):
            if state not in data_dict[labels[i]]:
                data_dict[labels[i]][state] = {}
            data_dict[labels[i]][state] = value[i]

    return data_dict


def income_view():
    COUCHDB_SERVER='http://admin:password@172.26.136.171:5984/'
    server = couchdb.Server(COUCHDB_SERVER)

    income_view = server['income_sudo'].view('filter/income_view', reduce=False)

    labels = ["mean_income", "median_income"]
    data_dict = {}

    for label in labels:
        data_dict[label] = {}

    for row in income_view:
        state = row['key']
        value = row['value']
        for i in range(len(labels)):
            if state not in data_dict[labels[i]]:
                data_dict[labels[i]][state] = {}
            data_dict[labels[i]][state] = value[i]

    return data_dict


def mentalhealth_view():
    mentalhealth_view = server['mentalhealth_sudo'].view('filter/mentalhealth_view', reduce=False)

    labels = ["total_emergencies", "mental_emergencies", "mental_emergencies_percentage"]
    data_dict = {}

    for label in labels:
        data_dict[label] = {}

    for row in mentalhealth_view:
        state = row['key']
        value = row['value']
        for i in range(len(labels)):
            if state not in data_dict[labels[i]]:
                data_dict[labels[i]][state] = {}
            data_dict[labels[i]][state] = value[i]

    return data_dict


def sentiment_view():
    sentiment_view = server['sentiment_tweets'].view('filter/sentiment_view', reduce=False)

    labels = ["num_tweets", "avg_sentiment", "very_happy", "very_happy_percentage", "happy", "happy_percentage", "neutral", "neutral_percentage", "sad", "sad_percentage", "very_sad", "very_sad_percentage"]
    data_dict = {}

    for label in labels:
        data_dict[label] = {}

    for row in sentiment_view:
        state = row['key']
        value = row['value']
        for i in range(len(labels)):
            if state not in data_dict[labels[i]]:
                data_dict[labels[i]][state] = {}
            data_dict[labels[i]][state] = value[i]

    return data_dict


def weekly_rent():
    rent_view = server['rent_sudo'].view('filterrent/rent_view', reduce=False)

    data_dict = {}
    for row in rent_view:
        year, state = row['key']
        value = row['value']
        year_key = 'rent_' + str(year)
        if year_key not in data_dict:
            data_dict[year_key] = {}
        data_dict[year_key][state] = value

    return data_dict


def rent_tweets():
    rent_tweets_view = server['rent_tweets'].view('filterlocation/location_view', reduce=True, group_level=1)

    data_dict = {'rent_tweets': dict()}

    for row in rent_tweets_view:
        state = row.key
        tweets = row.value
        if (state != 'notaus'):
            data_dict['rent_tweets'][state] = tweets

    return data_dict


def tweet_shortages():
    shortage_db = server['shortage_tweets']

    shortage_dict = {}
    for id in shortage_db:
        data = shortage_db[id]
        shortage_dict[data['word']] = data['count']

    return shortage_dict
