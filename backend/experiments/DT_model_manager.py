# This file creates all the decison tree models
import sqlite3
import os
import pandas as pd
from experiments.create_and_export_DT_model import create_dt

def get_already_made_models():

    directory = 'decision_tree_models/'

    files = os.listdir(directory)

    first_six_chars_list = []

    for file in files:
        # Get the first 6 characters of the file name
        first_six_chars_list.append(file[:6])

    return first_six_chars_list

def make_models():

    # Connect to the SQLite database
    conn = sqlite3.connect('databases\pitches.db')
    cursor = conn.cursor()

    # Step 2: Retrieve the list of tables from the database schema
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Get list of models that are already made
    made_models = get_already_made_models()

    # Loop through each table
    for table in tables:

        table_name = table[0]

        # Read the table into a DataFrame
        df = pd.read_sql_query(f"SELECT * FROM \"{table_name}\";", conn)

        if table_name not in made_models:
            # Process the DataFrame
            create_dt(df, table)



    # Close the database connection
    conn.close()

def main():

    make_models()

main()