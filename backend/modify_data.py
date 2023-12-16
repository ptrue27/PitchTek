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


def add_labels(df):

    # Shift next Pitch up
    df['next_pitch_type'] = df['pitch_type'].shift(1)

    # Drop first row as the label equals 'None'
    df.drop(df.index[0], inplace=True)


def remove_features(df):

    # Indexes are derived from this link:
    # https://docs.google.com/spreadsheets/d/1YPk4Ht_ik9Fv__ZcWwB1SbodhqzvTOse7eczARbWEdk/edit?usp=sharing

    columns_to_remove = ["release_pos_x", "release_pos_z", "batter", "pitcher"]
    df.drop(columns=columns_to_remove, inplace=True)


def main():

    file_path = '../uploads/savant_data_2.csv'

    df = pd.read_csv(file_path)
    
    add_labels(df)

    new_file_path = '../uploads/savant_data_2_with_labels.csv'
    df.to_csv(new_file_path, index=False)

main()