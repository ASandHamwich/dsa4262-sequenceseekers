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
- **[Software License](#software-license)**<br>

# Installing Prediction Software
_This installation guide recommends (and assumes) that you are running this software on an AWS remote Ubuntu instance._

## System Requirements
This software requires an Ubuntu system to run. 

## Prerequisites Installation
To install all necessary software and packages, ensure that `setup.sh` and `requirements.txt` are in the same directory. 

Run the following Shell script in your terminal as such: 
```
bash setup.sh
```

This installs Python 3.8, as well as all the necessary packages needed for running the prediction software.

## Installation of Prediction Software
To install and use this prediction software, ensure that you pull the following files from the `prediction` directory: 
1. `prediction/prediction_assets`
2. `prediction/prediction_script`
3. `prediction/prediction_notebooks`


`prediction_assets` is necessary for the scripts and notebooks to work; do ensure that the file exists in the same subdirectory as either `prediction_scripts` or `prediction_notebooks`.

_For ease of use, simply pull the `prediction` directory._

# Running Prediction Software
To begin, ensure that you have your `data.json` file in a subdirectory.

There are two methods of running the prediction software: either by using scripts or Python notebooks. For efficiency, we recommend using the scripts; however, if you would like to view each step of the prediction process, you are encouraged to use the Python notebooks. 

## Running the Scripts
`prediction_script` contains 
1. `data-prep.py` - data preprocessing
2. `prediction-script.py` - model loading and prediction
3. `predict.sh` - `bash` script for running the full workflow
   
### Input

### Execution Commands
To run the full workflow, activate the bash script with this command:
```
bash predict.sh <path-to-json-file>
```

### Output

## Running the Python Notebooks
### Input

### Execution Commands

### Output

# Software License
