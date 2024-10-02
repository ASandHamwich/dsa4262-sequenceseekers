import json
import pandas as pd
import os

cwd = os.getcwd() # Gets current working directory; ensure that .json file is in the same folder as this script.
path = os.path.join(cwd, 'dataset0.json')

with open(path) as r:
    data = r.read()
    split_data = data.split("\n") # .json file contains multiple JSON objects. Separate by newline.

# split_data: List of JSON String Objects
# To view first JSON object:
# print(split_data[0])

# JSON Object structure is as follows:
# { Transcript ID : { Middle Position : Combined_Nucleotide { : [ Read 1, Read 2, ..., Read n ] } } }

# Each read consists of 3 sets of: 
    # Length of direct RNA-Seq signal of 5-mer nucleotides (dwelling time)
    # s.d. of direct RNA-Seq signal
    # mean of signal

# Objective data structure should be as follows (for each JSON object)
# Transcript ID (str) | Nucleotide (str) | Position (str) | Read (list of int)
# Each JSON object should give 3 positions; each read is divided into 3 sets of 3 (total 9 values).

rows = []

count = 0
total = len(split_data)

for dp in split_data:
    if dp.strip() == '':
        continue

    obj = json.loads(dp) # Converts into a JSON (dictionary) object. 
    
    transcript_id = next(iter(obj))
    
    position2 = int(next(iter(obj[transcript_id])))
    position1 = position2 - 1
    position3 = position2 + 1

    cmbd_nucleotide = next(iter(obj[transcript_id][str(position2)]))

    nucleotide1 = cmbd_nucleotide[0:5]
    nucleotide2 = cmbd_nucleotide[1:6]
    nucleotide3 = cmbd_nucleotide[2:7]

    for read in obj[transcript_id][str(position2)][cmbd_nucleotide]:
        pos1_read = read[0:3]
        pos2_read = read[3:6]
        pos3_read = read[6:9]

        entry1 = [transcript_id, nucleotide1, position1, pos1_read]
        entry2 = [transcript_id, nucleotide2, position2, pos2_read]
        entry3 = [transcript_id, nucleotide3, position3, pos3_read]

        rows.extend([entry1, entry2, entry3])

    count += 1
    print(f"Object {count} completed. {total - count} left.")

print("Completed!")
data_df = pd.DataFrame(rows, columns=['Transcript ID', 'Nucleotide', 'Position', 'Read'])

print(data_df)

# To create a pkl file, for use in other Python as pd.DataFrame.
# output_path = os.path.join(cwd, 'parsed_data.pkl')
# data_df.to_pickle(output_path)

# Output as CSV file for visual analysis.
# output_path = os.path.join(cwd, 'parsed_data.csv')
# data_df.to_csv(output_path)






