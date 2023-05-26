########## Income Analysis ##########


import ijson
import time
import json
from matplotlib import pyplot as plt
import nltk
import spacy
import en_core_web_sm
from nltk.corpus import stopwords
import decimal

LOCATIONS = ['queensland','new south wales','tasmania','victoria','western australia','south australia']
CODES = [3,1,6,2,5,4]

def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i,y[i],y[i],ha = 'center')

start_time = time.time()
stop_words = set(stopwords.words('english'))

count = 0

# An encoder that deals with decimals
class DecimalEncoder(json.JSONEncoder):
    def default(self, i):
        if isinstance(i, decimal.Decimal):
            return str(i)
        return super(DecimalEncoder, self).default(i)

#setup
dictionary = {}
income = {}
unemployment = {}
output = {}
for loc in LOCATIONS:
    dictionary[loc] = [0,0,0,0]
    unemployment[loc] = 0
    income[loc] = [0,0]
    output[loc] = [0,0,0]

with open("data/abs_personal_income_total_income_distribution_gccsa_2017_18-4227938030852063387.json", "r") as f:
    parser = ijson.items(f, 'features.item.properties')
    for feature in parser:
        name = feature['gccsa_name']
        code = feature['gccsa_code']
        mean = feature['mean_aud']
        median = feature['median_aud']
        id = ''
        if ('Melbourne' in name) or ('Vic.' in name) or ('VIC' in code) or ('MEL' in code):
             id = 'victoria'
        elif ('Sydney' in name) or ('NSW' in name) or ('NSW' in code):
             id = 'new south wales'
        elif ('Brisbane' in name) or ('Qld' in name) or ('QLD' in code):
             id = 'queensland'
        elif ('WA' in code) or ('WA' in name):
             id = 'western australia'
        elif ('SA' in name) or ('SA' in name) or ('SA' in code) or ('Adelaide' in name):
             id = 'south australia'
        elif ('Tasmania' in name) or ('Tas.' in name) or ('TAS' in code) or ('Hobart' in name):
             id = 'tasmania'
        if id:
             income[id][0]+=1
             income[id][1]+= float(mean)
             output[id][0]+=1
             output[id][1]+= float(mean)
             output[id][2]+= float(median)

    for key,val in output.items():
        fmean = val[1]/val[0]
        fmedian = val[2]/val[0]
        output[key] = [fmean, fmedian]

    final = {}
    for key,val in income.items():
        final[key] = val[1]/val[0]

    states = list(final.keys())
    for i in range(len(states)):
        states[i] = states[i].title()        
    values = list(final.values())
    fig = plt.figure(figsize = (14, 8))
    plt.bar(states, values, color = 'blue', width = 0.4)
    addlabels(states, values)
    plt.xlabel("States")
    plt.ylabel("Income (AU$)")
    plt.title("Average Income per State")
    plt.savefig('Average Income.png', pad_inches=0.2)
    
with open("data/statistics/income_statistics.json", "w") as outfile:
    json.dump(output, outfile)

end_time = time.time()
total_time = end_time - start_time
print("total time: " + str(total_time/60)) 
