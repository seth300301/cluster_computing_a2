from mastodon import Mastodon, StreamListener
import re
import couchdb
import threading
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
                hashtag_list.append(word[1:].lower())

    if (hashtag_list):
        toot_with_key = {"created_at": created_at, "has_hashtag": True, "hashtags": hashtag_list}
    else:
        toot_with_key = {"created_at": created_at, "has_hashtag": False, "hashtags": None}
    
    return toot_with_key


class Listener(StreamListener):
    def __init__(self, couch):
        super().__init__()
        self.couch = couch
        self.db = couch['hashtags_mastodon']

    def on_update(self, toot):
        hash_toot = extract_hashtags(toot)
        #if hash_toot != None:
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

    servers = [(f'https://mastodon.social', 'IEWFcZxezj2y-ihvxgfpGqwRyeWSs9xPyVWE3SA069E'),
               (f'https://aus.social', 'z7vRVVkxu0hmQBuwTHni1GDiAIhDHUwLscCn6qWtISg'),
               (f'https://mastodon.au','6-0d4gKufAHdv8BCCZ3-W4xtWqrRYMz8T9LQv2Po7po'),
               (f'https://tictoc.social', '85MJprenneSpkiqGYQtHayL_xGLtOHeL2wMfln6Au-8')]

    couch = couchdb.Server('http://admin:300301@127.0.0.1:5984/')

    # Create a thread for each server to retrieve toots
    threads = []
    for server in servers:
        thread = TootThread(*server, couch)
        threads.append(thread)

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()