from mastodon import Mastodon, StreamListener
import re
import couchdb
from gensim.parsing.preprocessing import remove_stopwords
import yaml

def remove_html(text):
    html_pattern = re.compile(r'<[^>]+>')
    return html_pattern.sub('', text)

def extract_key(toot, keyword):
    created_at = str(toot["created_at"])
    content = remove_stopwords(remove_html(toot["content"]))
    content = re.sub(r"http\S+", "", content)
    tag_names = []
    if toot["tags"]:
        for tag in toot["tags"]:
            tag_names.append(tag["name"])
    if (any(word in content for word in keyword)) or (any(word in tag_names for word in keyword)):
        toot_with_key = {"created_at": created_at, "content": content, "tags": tag_names}
        return toot_with_key
    else:
        return

class Listener(StreamListener):
    def __init__(self, couch):
        super().__init__()
        self.couch = couch
        self.db = couch['shortage_mastodon']

    def on_update(self, toot):
        key_toot = extract_key(toot, shortage_keywords)
        if key_toot is not None:
            self.db.save(key_toot)
            print("A new data entry is saved")

    def on_abort(self, err):
        print(err)
        return False

shortage_keywords = ['scarcity', 'deficiency', 'insufficiency', ' lack ', 'dearth', 'inadequacy', 'famine', 'rarity', 'shortfall',
                     'inability to meet demand', 'underproduction', 'reduced supply', 'shortage', 'supply chain issues',
                     'out of stock', 'back ordered', 'low inventory', 'reduced supplies', 'product scarcity', 'stock shortage',
                     'limited availability', 'bare shelves', 'empty shelves', 'out of supplies', 'limited stock', 'supply deficit',
                     'understocked', 'shortage of supply', 'failure to meet demand', 'supply shortage', 'inadequate supply',
                     'insufficient supply', 'inability to keep up with demand', 'low stock levels', 'out of stock',
                     'stock shortage', 'inventory shortage', 'backordered items', 'backorder situation', 'needing more', 'backordering',
                     'waiting for restock', 'inadequate supply of', 'not available', 'not enough', 'need more', 'short in supply', 'sold-out inventory',
                     'out of production', 'shortages', 'not sufficient', 'ran out of', 'unmet demand', 'shipping delay',
                     'quantity was low', 'low availability', 'was hard to find', 'understocked', 'limited supply', 'was sold out',
                     'sought', 'out of stock', 'discontinued', 'scarcity', ' need ', 'supply was inadequate', 'unavailable inventory',
                     'ran out of stock', 'supply problems', 'depleted stocks', 'where to find', 'out-of-stock items',
                     'out-of-stock situation', 'out of circulation', 'finding it hard', 'short on hand', 'supply was short',
                     'inventory drought', 'inventory shortage', 'panic buying', 'short-supplied', 'ran low', 'shelves emptying',
                     'running low on', 'needed more', 'deficient supply', 'running out of stock', 'inventory issues', 'low supply',
                     'unable to find', 'insufficient supply', 'shortage', 'backlogged', 'out-of-print', 'almost running out of',
                     'scarcely supplied', 'delivery delay', 'looking out for', "wasn't enough", 'product shortage', 'running low', "can't find",
                     'hunting down', 'production backlog', 'supply chain crisis', 'stock was limited', 'delayed shipment', "couldn't find",
                     'looked for', 'insufficient inventory', 'limited', 'production delay', 'hard to find', 'where to purchase', 'dwindling inventory of',
                     'hoarding', 'supply depleted', 'supplies running short', 'quantities running low', 'inventory is dwindling', 'awaiting restock',
                     'hunting for', 'unavailable', 'insufficiently stocked', 'out-of-stock condition', 'shipment was delayed', 'insufficient stock',
                     'depleting supply of', 'was backordered', 'almost out of', 'supply shortage', 'sold out', 'supply chain disruption', 'short supply',
                     'looking for', 'scarce', 'scarce resources', 'stockout', 'low inventory', 'hunted for', 'insufficient', "can't get",
                     'insufficient supply chain', 'low stock', 'limited availability', 'amount was scarce', 'inventory dwindled',
                     'depleted supply of', 'experiencing supply chain issues', 'limited stock', 'short on supply',
                     'stock is limited', 'shelves were empty', 'running out of', 'backorder', 'hard to come by', 'insufficient stock of',
                     'delayed delivery', 'low quantity of', 'empty shelves', 'scarce supplies', 'unfulfilled orders',
                     'seeking', 'had supply chain issues', 'supply chain issues', 'selling out', 'shipments delayed',
                     'where to buy', 'experiencing scarcity', 'backorder situation', 'backordered', 'ran low on', 'stock was insufficient',
                     'scarce amount of', "couldn't get", 'inadequately supplied', 'depleted', 'short supply of', 'restock was awaited',
                     'was almost out of', 'seeking out', 'ran short']

shortage_keywords = list(set(shortage_keywords))

if __name__ == '__main__':
    with open('./config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    server_url = config['Settings']['server_url']
    access_token = config['Settings']['access_token']

    couch_username = config['Settings']['couch_username']
    couch_password = config['Settings']['couch_password']
    ip = config['Settings']['ip']
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