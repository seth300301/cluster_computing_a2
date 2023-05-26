########## Writes a dictionary with locations as keys and number of tweets per language to location_language.json ##########


import json
import time
import ijson
import decimal

NUM_LOCATION_TWEETS = 3233512
LOCATIONS = ['queensland','new south wales','tasmania','victoria','western australia','south australia']

start_time = time.time()
count = 0
lang = {}
for loc in LOCATIONS:
    lang[loc] = {}

# Write the tweets with location to a different .json file
with open("data/location-tweets.json", "r") as f:
    parser = ijson.items(f, 'item')

    for tweet in parser:
        if tweet.get('doc', {}).get('data', {}).get('lang', {}) and tweet.get('doc', {}).get('includes', {}):
            if isinstance(tweet.get('doc', {}).get('includes', {}), list):
                location = (tweet.get('doc', {}).get('includes', {})[0]).get('name',{})

            elif isinstance(tweet.get('doc', {}).get('includes', {}), dict):
                if ", " in ((tweet.get('doc', {}).get('includes', {}).get('places',{})[0]).get('full_name', {})):
                    location = ((tweet.get('doc', {}).get('includes', {}).get('places',{})[0]).get('full_name', {}))

            if ('Melbourne' in location) or ('Box Hill' in location) or ('Bendigo' in location) or ('Victoria' in location):
                location = 'victoria'
            elif ('New South Wales' in location) or ('Sydney' in location) or ('Canberra' in location):
                location = 'new south wales'
            elif ('Adelaide' in location) or ('South Australia' in location):
                location = 'south australia'
            elif ('Perth' in location) or ('Western Australia' in location):
                location = 'western australia'
            elif(('Hobart' in location) or ('Tasmania' in location)):
                location = 'tasmania'
            elif ('Brisbane' in location) or ('Gold Coast' in location) or ('Queensland' in location):
                location = 'queensland'

            if location in LOCATIONS:
                if 'total' not in lang[location].keys():
                    lang[location]['total'] = 1
                else:
                    lang[location]['total'] += 1
                if tweet.get('doc', {}).get('data', {}).get('lang', {}) in lang[location].keys():
                    lang[location][tweet.get('doc', {}).get('data', {}).get('lang', {})] += 1
                else:
                    lang[location][tweet.get('doc', {}).get('data', {}).get('lang', {})] = 1

# number of words per state
with open("data/location_language.json", "w") as outfile:
    json.dump(lang, outfile)
            
                            
end_time = time.time()
total_time = end_time - start_time
print("total time: " + str(total_time/60)) 