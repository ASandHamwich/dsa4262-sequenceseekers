# Prediction Script

# Imports
import os
import sys

import pandas as pd
import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

import joblib
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    print("Usage: python3 <prediction-script.py> <path_to_json_file>. Please try again.", file = sys.stderr)
    sys.exit(1)

def importAssets():
    model = load_model('../prediction_assets/rnn_model.keras')
    nucleotide_to_int = {'A': 0, 'C': 1, 'G': 2, 'T': 3, 'PAD': 4}

    scaler = joblib.load('../prediction_assets/scaler.joblib')
    if hasattr(scaler, 'mean_'):
        print("Scaler is fitted.", file = sys.stderr)
    else:
        print("Scaler is not fitted.", file = sys.stderr)

    with open('../prediction_assets/max_sequence_length.txt', 'r') as f:
        max_sequence_length = int(f.read())
    
    return model, nucleotide_to_int, scaler, max_sequence_length



# Encode sequences using the loaded nucleotide mapping
def encode_sequence(seq, mapping):
    return [mapping.get(nuc, mapping['PAD']) for nuc in seq]


def predict(model, scaler, nucleotide_to_int, max_sequence_length, new_data_path):
    # Load new data
    new_df = pd.read_csv(new_data_path)

    # Preprocessing steps
    # Concatenate sequences
    new_df['sequence'] = new_df['Nucleotide 1'] + new_df['Nucleotide 3'].str[-2:]
    new_df['encoded_sequence'] = new_df['sequence'].apply(lambda x: encode_sequence(x, nucleotide_to_int))
    new_df['padded_sequence'] = list(
        pad_sequences(
            new_df['encoded_sequence'],
            maxlen=max_sequence_length,
            padding='post',
            value=nucleotide_to_int['PAD']
        )
    )
    exclude_cols = [
        'Transcript ID', 'Position',
        'Nucleotide 1', 'Nucleotide 2', 'Nucleotide 3',
        'sequence', 'encoded_sequence', 'padded_sequence'
    ]
    numerical_cols = [col for col in new_df.columns if col not in exclude_cols]
    X_seq_new = np.stack(new_df['padded_sequence'].values)
    X_num_new = new_df[numerical_cols].values

    # Transform numerical features using the loaded, fitted scaler
    X_num_new = scaler.transform(X_num_new)

    # Make predictions
    y_pred_proba = model.predict([X_seq_new, X_num_new]).ravel()
    y_pred_class = (y_pred_proba >= 0.5).astype(int)

    new_df['Predicted Probability'] = y_pred_proba
    new_df['Predicted Label'] = y_pred_class

    return new_df

def graphPredictions(predictions, output_directory):
    plt.figure(figsize=(8,6))
    plt.hist(predictions['Predicted Probability'], bins=50, edgecolor='k')
    plt.xlabel('Predicted Probability')
    plt.ylabel('Frequency')
    plt.title('Distribution of Predicted Probabilities')
    
    output_path = os.path.join(output_directory, 'predicted_prob_graph.png')
    plt.savefig(output_path)

    return print("Graph saved as PNG.", file = sys.stderr)

def exportPredictions(predictions, output_directory):
    
    final_df = predictions[['Transcript ID', 'Position', 'Predicted Probability', 'Predicted Label']].copy()
    final_df.rename(columns={"Transcript ID":"transcript_id", 
                             "Position":"transcript_position", 
                             "Predicted Probability":"score",
                             "Predicted Label":"label"}, inplace=True)
    

    # final_df.drop('label', axis=1, inplace=True) ## Uncomment this line to remove the label column.

    output_path = os.path.join(output_directory, 'pred_results.csv')
    final_df.to_csv(output_path, index=False)

    return print("Results saved as CSV.", file = sys.stderr)



def main():
    print("Starting prediction...", file = sys.stderr)

    # Data CSV path
    data_path = sys.argv[1]

    # Output directory
    output_directory = os.path.dirname(data_path)

    # Running prediction
    model, nucleotide_to_int, scaler, max_sequence_length = importAssets()
    predictions = predict(model, scaler, nucleotide_to_int, max_sequence_length, data_path)

    # Results
    print("Predictions complete. Loading results...", file = sys.stderr)
    print(predictions.head(), file = sys.stderr)

    # Predicted label counts
    label_counts = predictions['Predicted Label'].value_counts()
    print("Predicted Label Counts:", file = sys.stderr)
    print(label_counts, file = sys.stderr)

    # Percentage of positive predictions
    total_predictions = len(predictions)
    num_positive = label_counts.get(1, 0)
    percentage_positive = (num_positive / total_predictions) * 100
    print(f"Percentage of instances predicted as positive: {percentage_positive:.2f}%", file = sys.stderr)
 
    # Saving results 
    print("Exporting results to CSV...", file = sys.stderr)
    exportPredictions(predictions, output_directory)
    
    # Saving visualisation
    print("Exporting visualisation...", file = sys.stderr)
    graphPredictions(predictions, output_directory)

    return print("Prediction Script complete.", file = sys.stderr)

if __name__ == "__main__":
    sys.exit(main())

