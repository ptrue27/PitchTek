# Dimensions of dummy heat map, strikezone.jpg: 195 x 258
#
# NOTE: The heat map is from the catchers perspective
#
#
import sqlite3
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.patches as patches
import random
import os


def get_dataframe(id):

    # Connect to SQLite database
    conn = sqlite3.connect('databases/pitches.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute a SQL query to fetch data from the table
    query = f"SELECT * FROM \"{id}\";"
    cursor.execute(query)

    # Fetch all rows from the executed query
    rows = cursor.fetchall()

    # Get the column names from the cursor description
    columns = [col[0] for col in cursor.description]

    # Create a pandas DataFrame with fetched data and column names
    df = pd.DataFrame(rows, columns=columns)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return df

# Given a player id and a pitch type, this function exports a jpg file that represents a heatmap for the given vars.
def make_heat_map(pitch_type, player_id, location):

    df = get_dataframe(player_id)

    # Extract values
    df = df[df['pitch_type'] == pitch_type]

    # Remove rows with NaN values
    df.dropna(subset=["plate_x", "plate_z"], inplace=True)

    # Create a 2D histogram
    heatmap, xedges, yedges = np.histogram2d(df["plate_x"], df["plate_z"], bins=20)

    # Change the backround color
    # plt.figure(facecolor="gray")

    # Plot the heat map
    plt.imshow(heatmap.T, extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], origin='lower', cmap='Reds')

    # Set custom limits for the x and y-axis
    plt.xlim(-2., 2)
    plt.ylim(.3, 4.7)

    # Add a custom box or rectangle
    custom_box = patches.Rectangle((-.9, 1.2), 1.8, 2.6, linewidth=2, edgecolor='black', facecolor='none', label='Custom Box')
    plt.gca().add_patch(custom_box)

    # Create horizontal lines
    for i in range(1, 3):
        plt.axhline(y=1.2 + i * 2.6 / 3, xmin=.28, xmax=.72, color='black', linestyle='-')

    # Create vertical lines
    for i in range(1, 3):
        plt.axvline(x=-.9 + i * 1.8 / 3, ymin=.21, ymax=.79, color='black', linestyle='-')


    # Add Pitch Location Prediction
    plt.plot(location[0], location[1], 'bo', markersize=30, alpha=0.5)

    # Remove the x and y-axis
    #plt.axis('off')

    # Set the dimensions of the plot
    #plt.figure(figsize=(1, 1.5))

    # Set custom limits to crop the plot
    #plt.xlim(2, 8)
    #plt.ylim(-2, 8)

    # Remove tics
    plt.xticks([])
    plt.yticks([])

    # Display the plot
    #plt.show()

    #Export the plot
    random_number = random.randint(0, 100000)
    directory = r"..\frontend\src\assets\heat_maps_v2"
    file_name = f"{player_id}_{pitch_type}_heat_map_{random_number}.jpg"
    file_path = os.path.join(directory, file_name)
    plt.savefig(file_path, bbox_inches='tight', pad_inches=0.1, dpi=500)

    plt.clf()

    return file_name


# This function is used to create the default strike zone
def create_default_strike_zone():
    path = '../uploads/434378_pitch_data.csv'
    df = pd.read_csv(path)

    # Extract values
    df = df[df['pitch_type'] == ""]

    # Create a 2D histogram
    heatmap, xedges, yedges = np.histogram2d(df["plate_x"], df["plate_z"], bins=20)

    # Change the backround color
    # plt.figure(facecolor="gray")

    # Plot the heat map
    plt.imshow(heatmap.T, extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], origin='lower', cmap="Greys")

    # Set custom limits for the x and y-axis
    plt.xlim(-2., 2)
    plt.ylim(.3, 4.7)

    # Add a custom box or rectangle
    custom_box = patches.Rectangle((-.9, 1.2), 1.8, 2.6, linewidth=2, edgecolor='black', facecolor='none', label='Custom Box')
    plt.gca().add_patch(custom_box)

    # Create horizontal lines
    for i in range(1, 3):
        plt.axhline(y=1.2 + i * 2.6 / 3, xmin=.28, xmax=.73, color='black', linestyle='-')

    # Create vertical lines
    for i in range(1, 3):
        plt.axvline(x=-.9 + i * 1.8 / 3, ymin=.21, ymax=.78, color='black', linestyle='-')

    # Remove tics
    plt.xticks([])
    plt.yticks([])

    # Display the plot
    # plt.show()

    # Export the plot
    file_name = r"..\frontend\src\assets\heat_maps\default_heat_map.jpg"
    plt.savefig(file_name, bbox_inches='tight', pad_inches=0.1)


def runtime_main():

    id = "434378"
    location = [0.5615384615384615, 1.9673992673992675]
    error = [0.5585559817570016, 0.8199079238523023]
    make_heat_map("FF", id, location, error)





