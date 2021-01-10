FROM arm32v7/python:3.7

ENV token token_init

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt 
RUN bash setup.sh 
RUN python3.7 train_and_populate_recommendation_db.py

CMD ["sh", "-c", "python3.7 app.py ${token}" ]