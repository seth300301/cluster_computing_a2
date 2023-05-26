########## English Tweets ##########


import json
import ijson
import time
import matplotlib.pyplot as plt
import decimal
import numpy as np

LOCATIONS = ['queensland','new south wales','tasmania','victoria','western australia','south australia']
LABELS = ['Very Happy', 'Happy', 'Neutral', 'Sad', 'Very Sad']
COLOURS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i,y[i],y[i],ha = 'center')

start_time = time.time()
count = 0

dictionary = {}
foreigners = {}
for loc in LOCATIONS:
    dictionary[loc] = [0,0,0,0,0,0]
    foreigners[loc] = [0,0]

# Write the tweets with location
final = {}
final_output = {}
print("Percentage of non English Tweets")
with open("data/location_language.json", "r") as f:
    data = json.load(f)

    for key, value in data.items():
        final_output[key] = [value['total']-value['und'], value['en']]
        final_output[key].append(round(value['en']/(value['total']-value['und'])*100,2))
        final[key] = round(value['en']/(value['total']-value['und'])*100,2)

states = list(final.keys())
for i in range(len(states)):
    states[i] = states[i].title()        
values = list(final.values())
fig = plt.figure(figsize = (14, 8))
plt.bar(states, values, color = 'blue', width = 0.4)
addlabels(states, values)
plt.xlabel("States")
plt.ylabel("Percentage")
plt.title("Percentage of English Tweets")
plt.savefig('graphs/Percentage_english_tweets.png')
print(final_output)

with open("data/statistics/english_tweets_statistics.json", "w") as outfile1:
    json.dump(final_output, outfile1)


end_time = time.time()
total_time = end_time - start_time
print("total time: " + str(total_time/60)) 
