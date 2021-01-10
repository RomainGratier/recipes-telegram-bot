import nltk
from src.recommendation_engine.create_model import create_model_cuisine_predictions, train_model_embeddings
from src.data_base.generate_db import create_and_populate_db

# train cuisine prediction model
create_model_cuisine_predictions()

# Populate sqlite db
create_and_populate_db()

# Train d2v model to predict similarity
train_model_embeddings()