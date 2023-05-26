########## Sentiment Analysis ##########


import json
import time
import matplotlib.pyplot as plt
import decimal
import numpy as np
from scipy.stats import f_oneway

LOCATIONS = ['queensland','new south wales','tasmania','victoria','western australia','south australia']
LABELS = ['Very Happy', 'Happy', 'Neutral', 'Sad', 'Very Sad']
COLOURS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

start_time = time.time()
count = 0
anova_data = []

# Write the tweets with location to a different .json file
# number of words per state
with open("data/location_count.json", "r") as f:
    data = json.load(f)

    for key, value in data.items():
        sizes = value[::-1]
        total = sizes[5]
        t_happy = (sizes[0])/total*100
        t_sad = (sizes[3])/total*100
        
        percentages = [round(x/total*100,2) for x in sizes]
        anova_data.append(percentages)
        final_label = [x + " - " + str(y) + "%" for x, y in zip(LABELS, percentages)]
        plt.pie(sizes, colors=COLOURS, startangle=90, shadow=False)
        plt.legend(final_label, loc='upper left', bbox_to_anchor=(-0.35, 0.2), fontsize=8)
        plt.savefig('graphs/' + str(key).title() + '_sentiment.png', pad_inches=0.2)

f_value, p_value = f_oneway(*anova_data)
duplicate = data
for key, val in duplicate.items():
    sentiment = val[0]
    total   = val[1]
    vsad    = (val[2], round(val[2]/total*100, 2))
    sad     = (val[3], round(val[3]/total*100, 2))
    neu     = (val[4], round(val[4]/total*100, 2))
    hap     = (val[5], round(val[5]/total*100, 2))
    vhap    = (val[6], round(val[6]/total*100, 2))
    avg     = sentiment/total
    duplicate[key] = [total, avg, vhap, hap, neu, sad, vsad]
    
with open("data/statistics/sentiment_statistics.json", "w") as outfile1:
    json.dump(duplicate, outfile1)

# print the results
print("p-value:", p_value) 

end_time = time.time()
total_time = end_time - start_time
print("total time: " + str(total_time/60)) 
