# create directory.
mkdir models

# Download data and deep learning model
# https://drive.google.com/file/d/1roNy54XNf7HNXU9tZ0SDB_VcLwhkK8Jv/view?usp=sharing
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1roNy54XNf7HNXU9tZ0SDB_VcLwhkK8Jv' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1roNy54XNf7HNXU9tZ0SDB_VcLwhkK8Jv" -O models/resnet50_frozen_model.zip && rm -rf /tmp/cookies.txt
cd models && unzip resnet50_frozen_model.zip && rm resnet50_frozen_model.zip && cd ..

#https://drive.google.com/file/d/175ncKLJ71D2JwjbRIBB3--wVnERgNDY8/view?usp=sharing
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=175ncKLJ71D2JwjbRIBB3--wVnERgNDY8' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=175ncKLJ71D2JwjbRIBB3--wVnERgNDY8" -O data.zip && rm -rf /tmp/cookies.txt
unzip data.zip && rm data.zip