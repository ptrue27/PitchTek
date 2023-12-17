'''
DATA CLEANING
***************
This file is used to manipulate and save the data. I will be used one time on raw data and will NOT
be run every time the software runs.

What this file does:

1. Add labels

2. Add id for each at-bat(not yet)

3. Remove Useless Data(not yet)

4. Combine multiple csv into one big csv(not yet)
'''

import csv
import pandas as pd

def handle_first_pitch():

    file_path = '../uploads/savant_data_2.csv'
    df = pd.read_csv(file_path)

    df = df[df["pitch_number"] == 1]

    new_file_path = '../uploads/first_pitch.csv'
    df.to_csv(new_file_path, index=False)

#
def handle_subsequent_pitches():

    file_path = '../uploads/savant_data_2.csv'
    df = pd.read_csv(file_path)

    # Shift data down
    df['previous_pitch_type'] = df['pitch_type'].shift(-1)
    df['previous_pitch_result'] = df['type'].shift(-1)

    # Extract all the first pitches
    df = df[df["pitch_number"] != 1]

    # Export to csv
    new_file_path = '../uploads/subsequent_pitches.csv'
    df.to_csv(new_file_path, index=False)


def remove_features(df):

    # Indexes are derived from this link:
    # https://docs.google.com/spreadsheets/d/1YPk4Ht_ik9Fv__ZcWwB1SbodhqzvTOse7eczARbWEdk/edit?usp=sharing

    columns_to_remove = ["release_pos_x", "release_pos_z", "batter", "pitcher"]
    df.drop(columns=columns_to_remove, inplace=True)


def main():

    handle_subsequent_pitches()

main()