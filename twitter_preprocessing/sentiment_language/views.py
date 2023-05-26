import couchdb

def english_view():
    COUCHDB_SERVER='http://admin:password@172.26.136.171:5984/'
    server = couchdb.Server(COUCHDB_SERVER)

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
    COUCHDB_SERVER='http://admin:password@172.26.136.171:5984/'
    server = couchdb.Server(COUCHDB_SERVER)

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
    COUCHDB_SERVER='http://admin:password@172.26.136.171:5984/'
    server = couchdb.Server(COUCHDB_SERVER)

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


def rent_sudo_view():
    COUCHDB_SERVER='http://admin:password@172.26.136.171:5984/'
    server = couchdb.Server(COUCHDB_SERVER)

    rent_sudo_view = server['rent_sudo'].view('filterrent/rent_view', reduce=False)

    data_dict = {}
    for row in rent_sudo_view:
        year, state = row['key']
        value = row['value']
        year_key = 'rent_' + str(year)
        if year_key not in data_dict:
            data_dict[year_key] = {}
        data_dict[year_key][state] = value

    return data_dict


# def rent_tweets_view():
#     COUCHDB_SERVER='http://admin:password@172.26.136.171:5984/'
#     server = couchdb.Server(COUCHDB_SERVER)

#     rent_tweets_view = server['rent_tweets'].view('filterrent/rent_view', reduce=False)

#     data_dict = {}
#     for row in rent_tweets_view:
#         year, state = row['key']
#         value = row['value']
#         year_key = 'rent_' + str(year)
#         if year_key not in data_dict:
#             data_dict[year_key] = {}
#         data_dict[year_key][state] = value

#     return data_dict


def sentiment_view():
    COUCHDB_SERVER='http://admin:password@172.26.136.171:5984/'
    server = couchdb.Server(COUCHDB_SERVER)

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



if __name__ == '__main__':
    print(sentiment_view())
