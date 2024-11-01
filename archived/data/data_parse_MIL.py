# Data Parsing Script for MIL purposes.

# Libraries
import json
import numpy as np
import pandas as pd
import os
from io import StringIO
import sys

def import_X():
    cwd = os.getcwd() # Gets current working directory; ensure that .json file is in the same folder as this script.
    path = os.path.join(cwd, 'dataset0.json')

    with open(path) as r:
        data = r.read()
        split_data = data.split("\n") # .json file contains multiple JSON objects. Separate by newline.

    return split_data

def import_Y():
    cwd = os.getcwd() # Gets current working directory; ensure that .json file is in the same folder as this script.    
    labels_path = os.path.join(cwd, 'data.info.labelled')

    with open(labels_path) as r:
        labels = r.read()

    labels_df = pd.read_csv(StringIO(labels))
    return labels_df

def labelParsing(labels_data):

    labels = np.array(labels_data['label'])

    return labels

def dataParsing(X_data):
    bags = []

    for line in X_data:
        if line.strip() == '':
            continue

        obj = json.loads(line)
        
        transcript_id = next(iter(obj))
        position = int(next(iter(obj[transcript_id])))
        cmbd_nucleotide = next(iter(obj[transcript_id][str(position)]))

        reads = obj[transcript_id][str(position)][cmbd_nucleotide]
        bags.append(np.array(reads))

    bags = np.array(bags, dtype=object)

    return bags

def dataPadding(bags):
    max_length = max(bag.shape[0] for bag in bags)

    padded_bags = np.array([np.pad(bag, ((0, max_length - bag.shape[0]), (0, 0)), mode='constant', constant_values=0) for bag in bags], dtype=np.float32)

    return padded_bags



def main():
    try:
        print("Importing data...")
        X_data = import_X()
        y_data = import_Y()
        print("Imports done!")

        print("Parsing and bagging...")
        X_parsed = dataParsing(X_data)
        padded_bags = dataPadding(X_parsed)

        print(f"Shape of padded bags: {padded_bags.shape}")

        print("Loading labels...")
        labels = labelParsing(y_data)

        np.savez_compressed("MIL_padded_data", x=padded_bags, y=labels)
        return "Data parse completed! Data exported!"

    except SyntaxError: 
        print("Error occurred.")

if __name__ == "__main__":
    sys.exit(main())
