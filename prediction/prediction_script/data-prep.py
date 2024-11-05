import json
import pandas as pd
import os
import sys
import numpy as np

if len(sys.argv) != 2:
    print("Usage: python3 <data-prep.py> <path_to_json_file>. Please try again.", file = sys.stderr)
    sys.exit(1)

# Get the file path from command-line arguments
file_path = sys.argv[1]

# Output Directory
output_directory = os.path.dirname(file_path)

# Imports the data, aggregating the reads according to position and shaping the data. 
def importData():
    aggregated_data = []

    # Reads the JSON file
    try: 
        print("Importing data ...", file = sys.stderr)
        with open(file_path, 'r') as f:
            print("Parsing JSON lines ...", file = sys.stderr)

            count = 0
            for line in f:
                # Each line is expected to be a JSON object
                data = json.loads(line)

                for transcript_id, positions in data.items():
                    for pos, flanking_data in positions.items():
                        for sequence, reads in flanking_data.items():
                            
                            count += 1
                            print(f"Read #{count} loaded.", file = sys.stderr)

                            # Convert the list of reads to a NumPy array for aggregation
                            features_array = np.array(reads)
                            
                            # Split the sequence into three nucleotides
                            nucleotide1 = sequence[0:5]
                            nucleotide2 = sequence[1:6]
                            nucleotide3 = sequence[2:7]

                            # Calculate mean, median, min, and max for each feature
                            aggregated = {
                                'mean': np.mean(features_array, axis=0).tolist(),
                                'median': np.median(features_array, axis=0).tolist(),
                                'min': np.min(features_array, axis=0).tolist(),
                                'max': np.max(features_array, axis=0).tolist()
                            }

                            # Flatten the results into a single row
                            row = {
                                'Transcript ID': transcript_id,
                                'Position': int(pos),
                                'Nucleotide 1': nucleotide1,
                                'Nucleotide 2': nucleotide2,
                                'Nucleotide 3': nucleotide3
                            }

                            # Define the feature names
                            feature_names = [
                                'N1 Length', 'N1 SD', 'N1 Mean',
                                'N2 Length', 'N2 SD', 'N2 Mean',
                                'N3 Length', 'N3 SD', 'N3 Mean'
                            ]
                            
                            for i, feature_name in enumerate(feature_names):
                                row[f'{feature_name} Avg'] = aggregated['mean'][i]
                                row[f'{feature_name} Median'] = aggregated['median'][i]
                                row[f'{feature_name} Min'] = aggregated['min'][i]
                                row[f'{feature_name} Max'] = aggregated['max'][i]

                            aggregated_data.append(row)
            


        # Convert rows to a DataFrame
        data_df = pd.DataFrame(aggregated_data)


        # Print only the header (column names)
        print("JSON conversion to Pandas successful. Columns: ", file = sys.stderr)
        print(data_df.columns.tolist(), file = sys.stderr)

        return data_df
    
    except BaseException as err:
        print("Error occurred while parsing JSON file to convert into Pandas format. Please try again.", file = sys.stderr)
        print("Full error statement: " + str(err), file = sys.stderr)
        sys.exit(1)


def exportData(data_df):
    try:
        output_csv_path = os.path.join(output_directory,'clean_data.csv')

        print("Exporting DataFrame to CSV...", file = sys.stderr)
        data_df.to_csv(output_csv_path,index=False)
        print("DataFrame exported as .csv file.", file = sys.stderr)
        print(output_csv_path, file=sys.stdout)
    
    except BaseException as err:
        print("Error occurred while exporting to CSV format. Please try again.", file = sys.stderr)
        print("Full error statement: " + str(err), file = sys.stderr)
        sys.exit(1)

        
def main():
    data_df = importData()
    return exportData(data_df)


if __name__ == "__main__":
    sys.exit(main())