import sqlite3 as sq
import pandas as pd

def get_df_from_db(cuisine):
    db = sq.connect('recipes.db')
    sql_query = "SELECT title, instructions, ingredients, ingredients_query FROM main_recipes WHERE cuisine = ?"
    return pd.read_sql(sql_query, db, params=(cuisine,))