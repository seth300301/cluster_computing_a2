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

foreigners = {}
for loc in LOCATIONS:
    foreigners[loc] = [0,0]


print("\n")
final_for={}
output_dict ={}
print("Percentage of Foreigners")
with open("data/abs_2021census_g01_aust_lga-9136893769511344821.json", "r") as f2:
    parse = ijson.items(f2, 'features.item.properties')
    for feature in parse:
        code = feature['lga_code_2021']
        local = feature['birthplace_australia_p']
        foreign = feature['birthplace_elsewhere_p']
        id = ''
        if code[0] ==  '1':
             id = 'new south wales'
        elif code[0] ==  '2':
             id = 'victoria'
        elif code[0] ==  '3':
             id = 'queensland'
        elif code[0] ==  '4':
             id = 'south australia'
        elif code[0] ==  '5':
             id = 'western australia'
        elif code[0] ==  '6':
             id = 'tasmania'
        if id:
            foreigners[id][0] += int(local)
            foreigners[id][1] += int(foreign)

    sorted_dictionary = dict(sorted(foreigners.items(), key = lambda x: x[1], reverse = True))

    for key, val in sorted_dictionary.items():
        output_dict[key] = val
        output_dict[key].append(round(val[1]/(val[0]+val[1])*100,2))
        final_for[key] = round(val[1]/(val[0]+val[1])*100,2)



values_for = list(final_for.values())
fig_for = plt.figure(figsize = (14, 8))
plt.bar(states, values_for, color = 'blue', width = 0.4)
addlabels(states, values_for)
plt.xlabel("States")
plt.ylabel("Percentage")
plt.title("Percentage of Foreigners")
plt.savefig('graphs/Percentage_foreigners.png')

with open("data/statistics/foreigner_statistics.json", "w") as outfile:
    json.dump(output_dict, outfile)


end_time = time.time()
total_time = end_time - start_time
print("total time: " + str(total_time/60)) 
