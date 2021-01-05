import sqlite3 as sq
import pandas as pd
import os

from src.recommendation_engine.data import import_recipes_main
from src.recommendation_engine.feature_engineering import process_recipes
from src.recommendation_engine.inference import load_pkl

MODEL_PATH = 'models/nlp'

def create_and_populate_db():
    data = import_recipes_main()
    
    # Process the data
    data = process_recipes(data)
    
    # Predict cuisine from trained model
    model = load_pkl(os.path.join(MODEL_PATH, 'pickle_model.pkl'))
    data["cuisine"] = model.predict(data["ingredients_query"].tolist())
    
    db = sq.connect('recipes.db')
    #Verify dtypes
    for col in data.columns:
        data[col] = data[col].astype('str')

    print(' ------------------ Check data before populating the db ------------------')
    print(data.columns)
    print(data.head())
    print(data.shape)
    data.to_sql('main_recipes', db, if_exists='replace')