import json
import ijson
import csv
import time
import multiprocessing
from collections import defaultdict

start_time = time.time()
hashtag_csv = 'data/hashtags.csv'

def hashtag_count(string_list, hashtag_dict):
    for word in string_list:
        if word[0] == '#':
            hashtag_dict[word[1:].lower()] += 1


def sort_dict(hashtag_dict):
    hashtag = dict(sorted(hashtag_dict.items(), key=lambda item: item[1], reverse=True))

    return hashtag


hashtag_dict = defaultdict(int)

if __name__ == '__main__':    
    # Write the tweets with location to a different .json file
    with open('data/twitter-huge.json', 'r') as f:
        parser = ijson.items(f, 'rows.item')

        # count = 0

        for tweet in parser:
            # count += 1

            string = tweet.get('doc', {}).get('data', {}).get('text', {})
            if ('#' in string):
                hashtag_count(string.split(), hashtag_dict)

            # if (count == 50000):
            #     break

    pool = multiprocessing.Pool()
    results = []

    result = pool.apply_async(sort_dict, (hashtag_dict,))

    pool.close()
    pool.join()

    sorted_hashtags = result.get()

    with open(hashtag_csv, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(['Hashtag', 'Number of Tweets'])

        for hashtag in sorted_hashtags:
            writer.writerow([hashtag, sorted_hashtags[hashtag]])

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("Elapsed time: ", elapsed_time)