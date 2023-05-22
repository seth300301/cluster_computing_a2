from mastodon import Mastodon, StreamListener
import re
import spacy
import couchdb
import threading
import yaml
from bs4 import BeautifulSoup

nlp = spacy.load('en_core_web_sm')

# Compile regular expressions
url_regex = re.compile(r'http\S+')
html_pattern = re.compile(r'<[^<]+?>')
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
    # Remove HTML
    string = html_pattern.sub('', string)
    # Remove usernames
    string = username_regex.sub('', string)
    # Remove hashtags
    string = hashtag_regex.sub('', string)
    # Remove newline characters
    string = newline_regex.sub(' ', string)
    # Remove emojis
    string = emoji_pattern.sub('', string)
    return string


def get_named_entities(text):
    FOCUSED_LABELS = ['GPE', 'NORP', 'EVENT']
    #IGNORED_LABELS = ['CARDINAL', 'ORDINAL', 'DATE', 'TIME', 'PERCENT']

    doc = nlp(text)
    named_entities = set()
    for ent in doc.ents:
        if (ent.label_ in FOCUSED_LABELS):
            named_entities.add(str(ent.text) + " " + str(ent.label_))
    return named_entities


def process_tweet(tweet):
    #string = tweet.get('doc', {}).get('data', {}).get('text', {})

    preprocessed_string = preprocess_string(tweet)
    named_entities = get_named_entities(preprocessed_string)

    return preprocessed_string, named_entities


def extract_entities(toot):
    created_at = str(toot["created_at"])
    content = toot["content"]
    soup = BeautifulSoup(content, 'html.parser')
    filtered_string = soup.get_text()
    
    preprocessed_string, named_entities = process_tweet(filtered_string)

    if (named_entities):
        toot_with_key = {"created_at": created_at, "content": preprocessed_string, "entities": list(named_entities)}
        return toot_with_key
    else:
        return


class Listener(StreamListener):
    def __init__(self, couch):
        super().__init__()
        self.couch = couch
        self.db = couch['entities']

    def on_update(self, toot):
        ent_toot = extract_entities(toot)
        if ent_toot != None:
            self.db.save(ent_toot)
            print("A new data entry is saved")

    def on_abort(self, err):
        print(err)
        return False


class TootThread(threading.Thread):
    def __init__(self, server_url, access_token, couch):
        threading.Thread.__init__(self)
        self.server_url = server_url
        self.access_token = access_token
        self.couch = couch

    def run(self):
        print("Connecting to Mastodon server : " + self.server_url)
        m = Mastodon(api_base_url=self.server_url, access_token=self.access_token)
        print("Start harvesting " + self.server_url)
        while True:
            try:
                stream = m.stream_local(listener=Listener(self.couch), timeout=3600, reconnect_async=True)
            except:
                print("Reconnecting to " + self.server_url + "...")
                pass


if __name__ == '__main__':
    with open('./config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # servers = [(f'https://mastodon.social', 'IEWFcZxezj2y-ihvxgfpGqwRyeWSs9xPyVWE3SA069E'),
    #            (f'https://aus.social', 'z7vRVVkxu0hmQBuwTHni1GDiAIhDHUwLscCn6qWtISg'),
    #            (f'https://mastodon.au','6-0d4gKufAHdv8BCCZ3-W4xtWqrRYMz8T9LQv2Po7po'),
    #            (f'https://tictoc.social', '85MJprenneSpkiqGYQtHayL_xGLtOHeL2wMfln6Au-8')]

    server_url = config['server_url']
    access_token = config['access_token']

    couch_username = config['couch_username']
    couch_password = config['couch_password']
    ip = config['ip']
    couch_server = f"http://{couch_username}:{couch_password}@{ip}:5984/"

    couch = couchdb.Server(couch_server)
    listener = Listener(couch)

    print("Connecting to Mastodon server: " + server_url)
    m = Mastodon(api_base_url=server_url, access_token=access_token)

    print("Start harvesting from " + server_url)
    try:
        stream = m.stream_local(listener=listener, timeout=3600, reconnect_async=True)
    except:
        print("An error occurred while connecting to " + server_url)