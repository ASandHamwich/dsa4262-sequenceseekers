# DSA4262 Project: Prediction of m6A RNA Modifications from Direct RNA-Seq Data

This project explores the use of Machine Learning methods to detect m6a RNA modifications from Nanopore Direct RNA Sequencing data, as part of NUS module DSA4262: Sense-making Case Analysis: Health and Medicine.

<i> This project was done by: Arnold, Jia Hui, Duocai, Amanda </i>

# Table of Contents
- **[Installing Prediction Software](#installing-prediction-software)**<br>
    - **[System Requirements](#system-requirements)**<br>
    - **[Prerequisites](#prerequisites-installation)**<br>
    - **[Installation of Prediction Software](#installation-of-prediction-software)**<br>
- **[Running Prediction Software](#running-prediction-software)**<br>
    - **[Running the Scripts](#running-the-scripts)**<br>
        - **[Input](#input)**<br>
        - **[Execution Commands](#execution-commands)**<br>
        - **[Output](#output)**<br>
    - **[Running the Python Notebooks](#running-the-python-notebooks)**<br>
        - **[Input](#input)**<br>
        - **[Execution Commands](#execution-commands)**<br>
        - **[Output](#output)**<br>

# Installing Prediction Software
_This installation guide recommends (and assumes) that you are running this software on an AWS remote Ubuntu instance._ 

## Required Files from this Repositry to be Uploaded to AWS Project Storage
Please pull the files below from GitHub and upload into your AWS Project Storage. 
1. `requirements.txt`
2. `setup.sh`
3. `predictions` (Please upload this folder as a whole to avoid confusion) <br>
    a) `prediction/prediction_assets`: contains the necessary assets for running the prediction model<br>
    b) `prediction/prediction_script`: contains the scripts for generating the predictions <br>
    c) `prediction/prediction_notebooks`: contains notebooks for generating the predictions <br>
    d) `prediction/sample_prediction`: sample data for testing <br>


## System Requirements
This software requires an Ubuntu system to run. On an AWS remote instance, we recommend running a large instance with more CPU processing power - at least `t3.2xlarge`.

## Prerequisites Installation
Please ensure that `setup.sh` and `requirements.txt` are in the same directory. This is required to install all necessary software and packages.

Run the following Shell script in your terminal as such: 

```
bash setup.sh
```

This installs Python 3.8.10, as well as all the necessary packages needed for running the prediction software.


# Running Prediction Software
If you have uploaded the predictions folder as a whole, this whole section should not be an issue and you may skip and move directly to the section "Execution Commands". <br>

To begin, ensure that you have your `data.json` file in its own subdirectory. The software will create outputs in the same directory as this file for ease of access. 

`prediction_assets` is necessary for the scripts and notebooks to work; do **ensure that the folder exists in the same subdirectory as `prediction_scripts` and `prediction_notebooks`.** 

**Do not remove the items from any of these 3 folders;** to run the software, navigate to the respective subdirectories. 

There are two methods of running the prediction software: either by using scripts or Python notebooks. For efficiency, we recommend using the scripts; however, if you would like to view each step of the prediction process, you are encouraged to use the Python notebooks. 

A test dataset has been provided under `prediction/sample_prediction`. 

_For those new to running Jupyter on remote instances, an additional README.md has been included in `prediction_notebooks` for your reference as a brief guide._

## Running the Scripts
`prediction_script` contains 
1. `data-prep.py` - data preprocessing
2. `prediction-script.py` - model loading and prediction
3. `predict.sh` - `bash` script for running the full workflow
   
### Input
The data preparation step `data-prep.py` takes in the data in a JSON format and processes it, which is then piped as a CSV file into the `prediction-script.py` for predicting.

### Execution Commands
To run the full workflow, navigate to the `prediction_script` directory. 
```
cd <relative-path>/prediction/prediction_script
```

Activate the bash script with this command:
```
bash predict.sh <path-to-json-file>
```
Sample usage: `bash predict.sh ../sample_prediction/test_data.json`

_(Optional)_
If you wish to run each script separately, you may do so with
```
python3 data-prep.py <path-to-json-file>
python3 prediction-script.py <path-to-cleaned-data-csv-file>
```

### Output
The data preparation step `data-prep.py` outputs the cleaned data CSV file `clean_data.csv` in the same subdirectory as the data JSON file.

The prediction step `prediction-script.py` outputs 
1. `pred_results.csv` - the prediction probability results in CSV format;
2. `predicted_prob_graph.png` - a bar graph visualisation of the results probablity into the same subdirectory as `clean_data.csv`.
![d1](https://github.com/user-attachments/assets/118af245-b7b1-4bc9-b37d-df06fb95c2e8)

If running via the bash script, all files will be found in the same subdirectory as the initial data JSON file.

## Running the Python Notebooks
`prediction_notebooks` contains
1. `prediction-data-preprocessing.ipynb`: data preprocessing notebook
2. `prediction-notebook.ipynb`: prediction notebook
   
### Input
The data preparation step `prediction-data-preprocessing.ipynb` takes in the data in a JSON format and processes it into a CSV file, which is then taken into `prediction-notebook.ipynb` for predicting.

### Execution Commands
First, navigate to the `prediction_notebooks` directory to access both `prediction-data-preprocessing.ipynb` and `prediction-notebook.ipynb`.
```
cd <relative-path>/prediction/prediction_notebooks
```
Access `prediction-data-preprocessing.ipynb` and run all the Python cells. Ensure that the path corresponds to the intended data JSON file. 
<p>
    <img width="1070" alt="Data Path - Data Preprocessing Notebook" src="https://github.com/user-attachments/assets/b6113d8d-059d-42dd-b9e5-5361349bf3e7">
    <em> Data Path - Data Preprocessing Notebook </em>
</p>

Access `prediction-notebook.ipynb` and run all the Python cells. Ensure that the path correspond correctly to the cleaned data CSV file generated from `prediction-data-preprocessing.ipynb`. 

<p>
    <img width="1072" alt="Data Path - Prediction Notebook" src="https://github.com/user-attachments/assets/1f594f09-36d0-4a71-ace8-94b0dfec69ce">
    <em> Data Path - Prediction Notebook </em>
</p>

### Output
`prediction-data-preprocessing.ipynb` creates the cleaned data CSV file in the same subdirectory as the initial data JSON file. 

`prediction-notebook.ipynb` creates `pred_results.csv` in the same subdirectory as the cleaned data CSV file. 
