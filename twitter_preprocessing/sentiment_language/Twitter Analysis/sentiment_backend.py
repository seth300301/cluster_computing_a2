########## Writes number of tweets and number of tweets with location to tweet_count.json ##########


import json
import time
import ijson
import decimal

NUM_LOCATION_TWEETS = 3233512
LOCATIONS = ['queensland','new south wales','tasmania','victoria','western australia','south australia']

start_time = time.time()
count = 0

location_count = {}

for loc in LOCATIONS:
    location_count[loc] = [0,0,0,0,0,0,0]

# Write the tweets with location to a different .json file
with open("data/location-tweets.json", "r") as f:
    parser = ijson.items(f, 'item')

    for tweet in parser:
        if tweet.get('doc', {}).get('includes', {}):
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
                if tweet.get('doc', {}).get('data', {}).get('sentiment',{}):
                    if float(tweet.get('doc', {}).get('data', {}).get('sentiment',{})) >= -0.3 and float(tweet.get('doc', {}).get('data', {}).get('sentiment',{})) <= 0.3:
                        location_count[location][4] += 1
                    elif float(tweet.get('doc', {}).get('data', {}).get('sentiment',{})) > 0.3 and float(tweet.get('doc', {}).get('data', {}).get('sentiment',{})) <= 0.7:
                        location_count[location][5] += 1
                    elif float(tweet.get('doc', {}).get('data', {}).get('sentiment',{})) > 0.7:
                        location_count[location][6] += 1
                    elif float(tweet.get('doc', {}).get('data', {}).get('sentiment',{})) < -0.3 and float(tweet.get('doc', {}).get('data', {}).get('sentiment',{})) >= -0.7:
                        location_count[location][3] += 1
                    elif float(tweet.get('doc', {}).get('data', {}).get('sentiment',{})) < -0.7:
                        location_count[location][2] += 1
                    location_count[location][1] += 1
                    location_count[location][0] += float(tweet.get('doc', {}).get('data', {}).get('sentiment',{}))
                
sorted_dictionary = dict(sorted(location_count.items(), key = lambda x: x[1], reverse = True))
            
# number of words per state
with open("data/location_count.json", "w") as outfile:
    json.dump(sorted_dictionary, outfile)

end_time = time.time()
total_time = end_time - start_time
print("total time: " + str(total_time/60)) 