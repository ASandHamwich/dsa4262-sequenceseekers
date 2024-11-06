#!/bin/bash
if [[ ! -n $1 ]];
then
    echo "Usage: bash <predict.sh> <path_to_json_file>. Please try again."
else
  data_path=$(python3 data-prep.py "$1")
  python3 prediction-script.py "$data_path"
fi