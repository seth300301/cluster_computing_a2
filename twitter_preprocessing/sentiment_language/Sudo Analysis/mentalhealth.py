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
mental_health = {}
for loc in LOCATIONS:
    mental_health[loc] = [0,0]

with open("data/aihw_mental_hlth_serv_emrgncy_presentations_demo_sa3_2014_18-5941719138775776286.json", "r") as f:
    parser = ijson.items(f, 'features.item.properties')
    for feature in parser:
        code = feature['sa3_code']
        mental = feature['mentalhlth_rel_pres_tot']
        total = feature['tot_emerg_dep_pres_tot']
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
             mental_health[id][0] += int(total)
             mental_health[id][1] += int(mental)

    duplicate = mental_health

    final = {}
    for key,val in mental_health.items():
        duplicate[key].append(round(val[1]/val[0]*100,2))
        final[key] = round(val[1]/val[0]*100,2)

    states = list(final.keys())
    for i in range(len(states)):
        states[i] = states[i].title()        
    values = list(final.values())
    fig = plt.figure(figsize = (14, 8))
    plt.bar(states, values, color = 'blue', width = 0.4)
    addlabels(states, values)
    plt.xlabel("States")
    plt.ylabel("Percentage")
    plt.title("Percentage of Mental Health Related Emergencies")
    plt.savefig('graphs/Mental Health.png', pad_inches=0.2)

with open("data/statistics/mentalhealth_statistics.json", "w") as outfile:
    json.dump(duplicate, outfile)

end_time = time.time()
total_time = end_time - start_time
print("total time: " + str(total_time/60)) 
