from mastodon import Mastodon, StreamListener
import couchdb
import threading
import yaml
from bs4 import BeautifulSoup


def extract_hashtags(toot):
    created_at = str(toot["created_at"])
    content = toot["content"]
    soup = BeautifulSoup(content, 'html.parser')
    filtered_string = soup.get_text()

    hashtag_list = set()
    
    if ('#' in filtered_string):
        string_list = filtered_string.split()
        for word in string_list:
            if (word[0] == '#'):
                hashtag_list.add(word[1:].lower())

    if (hashtag_list):
        toot_with_key = {"created_at": created_at, "hashtags": list(hashtag_list)}
        return toot_with_key
    else:
        return


class Listener(StreamListener):
    def __init__(self, couch):
        super().__init__()
        self.couch = couch
        self.db = couch['hashtags_mastodon']

    def on_update(self, toot):
        hash_toot = extract_hashtags(toot)
        if hash_toot != None:
            self.db.save(hash_toot)
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
    #            (f'https://aus.social', 'z7vRVVkxu0hmQBuwTHni1GDiAIhDHUwLscCn6qWtISg'), meister
    #            (f'https://mastodon.au','6-0d4gKufAHdv8BCCZ3-W4xtWqrRYMz8T9LQv2Po7po'), child2
    #            (f'https://tictoc.social', '85MJprenneSpkiqGYQtHayL_xGLtOHeL2wMfln6Au-8')] child1

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