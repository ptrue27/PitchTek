import pandas as pd
import sqlite3
from pybaseball import playerid_lookup, statcast_pitcher

# This function gets me a list of every pitcher in the mlb.db database
def extract_unique_ids():
    # Connect to the SQLite database
    conn = sqlite3.connect('..\databases\mlb.db')
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
    connection = sqlite3.connect('..\databases\pitches.db')
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
    conn = sqlite3.connect('..\databases\pitches.db')
    conn.close()


# This function is used to download the data create the database.
def data_base_manager():
    # Get id for each pitcher
    unique_ids = extract_unique_ids()

    # Convert list of ids to strings
    unique_ids = [str(num) for num in unique_ids]

    # delete ids that are already in the database
    unique_ids = filter_out_ids(unique_ids)

    conn = sqlite3.connect('..\databases\pitches.db')

    for pitcher_id in unique_ids:
        # Get data for each id
        data = download_player_pitch_data(pitcher_id)

        # Add df to sqlite db as a table
        data.to_sql(pitcher_id, conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()


data_base_manager()