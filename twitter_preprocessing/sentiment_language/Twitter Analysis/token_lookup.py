########## Prints the word and its corresponding count ##########


import json
import time

WORD = "pandemic"
IGNORE = ["CARDINAL","DATE","TIME","ORDINAL"]

start_time = time.time()
count = 0

# check the word count in the dictionary
with open('data/word_dictionary.json', 'r') as f:
    data = json.load(f)

for key, value in data.items():
    count += 1
    # if key == WORD:
    print(count, key, value)
    if count == 50:
        break


end_time = time.time()
total_time = end_time - start_time
print("total time: " + str(total_time/60)) 

