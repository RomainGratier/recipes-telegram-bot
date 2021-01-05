#! /bin/bash

mkdir models
wget -P /models https://drive.google.com/drive/folders/1k6R0KSj2f-9hBZGPC6nKBNgMuGJ5CU8x?usp=sharing

wget https://drive.google.com/drive/folders/1YqoaxXs9tOq6qN21zCyP5Br4bwYaFbk2?usp=sharing

set -e
source ../virtualenv/bin/activate
# virtualenv is now active.
python3.7 train_and_populate_recommendation_db.py