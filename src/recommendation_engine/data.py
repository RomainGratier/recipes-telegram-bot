import os
import pandas as pd

DATA_CUISINE_PATH = "data/cuisine_data/"
DATA_RECIPES_PATH = "data/recipes_data/"

def import_data():
    train = pd.read_json(os.path.join(DATA_CUISINE_PATH, 'train.json'))
    test = pd.read_json(os.path.join(DATA_CUISINE_PATH, 'test.json'))
    return pd.concat([train,test],axis=0)

def import_recipes_main():
    data_path_ar = os.path.join(DATA_RECIPES_PATH, "recipes_raw_nosource_ar.json")
    data_path_epi = os.path.join(DATA_RECIPES_PATH, "recipes_raw_nosource_epi.json")
    data_path_fn = os.path.join(DATA_RECIPES_PATH, "recipes_raw_nosource_fn.json")
    
    data =  pd.concat([pd.read_json(data_path_ar, orient='index'), pd.read_json(data_path_epi, orient='index'), pd.read_json(data_path_fn, orient='index')])
    data = data.reset_index()
    data = data.drop(columns=['picture_link', 'index'])
    return data