#! /bin/bash

mkdir models
#wget -P /models https://drive.google.com/drive/folders/1k6R0KSj2f-9hBZGPC6nKBNgMuGJ5CU8x?usp=sharing
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1k6R0KSj2f-9hBZGPC6nKBNgMuGJ5CU8x' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1k6R0KSj2f-9hBZGPC6nKBNgMuGJ5CU8x" -O models && rm -rf /tmp/cookies.txt

#wget https://drive.google.com/drive/folders/1YqoaxXs9tOq6qN21zCyP5Br4bwYaFbk2?usp=sharing
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1YqoaxXs9tOq6qN21zCyP5Br4bwYaFbk2' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1k6R0KSj2f-9hBZGPC6nKBNgMuGJ5CU8x" -O data && rm -rf /tmp/cookies.txt

set -e
source ../virtualenv/bin/activate
# virtualenv is now active.
python3.7 train_and_populate_recommendation_db.py