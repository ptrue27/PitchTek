import sqlite3
from create_heatmap import make_heat_map
import os


def get_already_made_images():
    directory = '..\..\\frontend\src\\assets\heat_maps'

    files = os.listdir(directory)

    first_six_chars_list = []

    for file in files:
        # Get the first 6 characters of the file name
        first_six_chars_list.append(file[:9])

    return first_six_chars_list


def get_pitch_types_from_player():

    # Connect to the SQLite database
    conn = sqlite3.connect('..\databases\pitches.db')
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
            cursor.execute(f"SELECT DISTINCT pitch_type FROM \"{table_name}\";")
            unique_values = cursor.fetchall()

            # Step 5: Print the unique values
            print("Unique values of 'pitch_type':")
            for value in unique_values:
                print(value[0])
                if(value[0] != None) and ((table_name + "_" + value[0]) not in images):
                    make_heat_map(value[0], table_name)

    # Close the connection
    conn.close()


def main():

    get_pitch_types_from_player()

main()