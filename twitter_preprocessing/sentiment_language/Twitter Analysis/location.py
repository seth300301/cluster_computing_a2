########## Writes Tweets with locations to location-tweets.json ##########

import json
import time
import ijson
import decimal

NUM_LOCATION_TWEETS = 3233512

start_time = time.time()
count = 0


# An encoder that deals with decimals
class DecimalEncoder(json.JSONEncoder):
    def default(self, i):
        if isinstance(i, decimal.Decimal):
            return str(i)
        return super(DecimalEncoder, self).default(i)

# Write the tweets with location to a different .json file
with open('data/twitter-huge.json', 'r') as f, open("data/location-tweets.json", "w") as outfile:
    parser = ijson.items(f, 'rows.item')
    outfile.write('[')

    for tweet in parser:
        if tweet.get('doc', {}).get('includes', {}):
            json.dump(tweet, outfile, cls = DecimalEncoder)
            count += 1
            if count == NUM_LOCATION_TWEETS:
                outfile.write(']')
                break
            else:
                outfile.write(',')


end_time = time.time()
total_time = end_time - start_time
print("total count  : " + str(count)) 
print("total time   : " + str(total_time/60)) 