import  couchdb, json, ijson, time,decimal
import pandas as pd
import numpy as np
COUCHDB_SERVER='http://admin:password@172.26.136.171:5984/'
server = couchdb.Server(COUCHDB_SERVER)

english_view = server['english_tweets'].view('filter/english_view', reduce=False)

data_dict = {}
for row in english_view:
    state = row['key']
    value = row['value']
    if state not in data_dict:
        data_dict[state] = {}
    data_dict[state] = value
    
data_dict.to_string()