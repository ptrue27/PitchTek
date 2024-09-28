import sqlite3
from pybaseball import playerid_lookup, statcast_pitcher
from backend.app.create_heatmap import make_heat_map
import os

import pandas as pd
# This function gets me a list of every pitcher in the mlb.db database


def extract_unique_ids():

    # Connect to the SQLite database
    conn = sqlite3.connect('databases\mlb.db')
    cursor = conn.cursor()

    query = f"SELECT DISTINCT {'id'} FROM {'PITCHERS'};"
    cursor.execute(query)

    unique_ids = cursor.fetchall()

    cursor.close()
    conn.close()

    # Extract and add to list
    return list([row[0] for row in unique_ids])


# This function filters out the ids that are already in the database
def filter_out_ids(ls):

    connection = sqlite3.connect('databases/pitches.db')
    cursor = connection.cursor()

    # Execute a query to get the list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    # Fetch all the rows from the result
    tables = cursor.fetchall()

    # Extract table names from the result
    table_names = [table[0] for table in tables]

    cursor.close()
    connection.close()

    i = 0
    # Remove duplicate entries
    ls = [x for x in ls if x not in table_names]

    return ls


def download_player_pitch_data(id):

    # pull from pybaseball db/server
    pitch_data = statcast_pitcher('2023-01-01', '2023-12-31', id)

    # Filter the DataFrame to include only regular season games
    return pitch_data[pitch_data['game_type'] == 'R']


# Create database file
def create_database():

    conn = sqlite3.connect('databases\pitches.db')
    # cursor = conn.cursor()
    # conn.commit()
    conn.close()


# This function is used to download the data create the database.
def data_base_manager():

    # Get id for each pitcher
    unique_ids = extract_unique_ids()

    # Convert list of ids to strings
    unique_ids = [str(num) for num in unique_ids]

    # delete ids that are already in the database
    unique_ids = filter_out_ids(unique_ids)

    conn = sqlite3.connect('databases\pitches.db')

    for pitcher_id in unique_ids:

        # Get data for each id
        data = download_player_pitch_data(pitcher_id)

        # Add df to sqlite db as a table
        data.to_sql(pitcher_id, conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()


def get_already_made_images():

    directory = '..\\frontend\src\\assets\heat_maps'

    files = os.listdir(directory)

    first_six_chars_list = []

    for file in files:
        # Get the first 6 characters of the file name
        first_six_chars_list.append(file[:9])

    return first_six_chars_list


def get_pitch_types_from_player():

    # Connect to the SQLite database
    conn = sqlite3.connect('databases\pitches.db')
    cursor = conn.cursor()

    # Step 2: Retrieve the list of tables from the database schema
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Get list of images that are already made
    images = get_already_made_images()

    # Step 3: Iterate over each table
    for table in tables:
        table_name = table[0]
        print(f"Table: {table_name}")

        # Step 4: Execute a query to retrieve the unique values of a certain column
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]

        if 'pitch_type' in column_names:
            cursor.execute(f"SELECT DISTINCT pitch_type FROM \"{
                           table_name}\";")
            unique_values = cursor.fetchall()

            # Step 5: Print the unique values
            print("Unique values of 'pitch_type':")
            for value in unique_values:
                print(value[0])
                if (value[0] != None) and ((table_name + "_" + value[0]) not in images):
                    make_heat_map(value[0], table_name)

    # Close the connection
    conn.close()


def main():

    data_base_manager()

    get_pitch_types_from_player()


main()
