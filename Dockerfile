FROM arm32v7/python:3.7

ENV token token_init

RUN apt install libatlas-base-dev

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt 

COPY . /app
WORKDIR /app

RUN bash setup.sh 
RUN python3.7 train_and_populate_recommendation_db.py

CMD ["sh", "-c", "python3.7 app.py ${token}" ]