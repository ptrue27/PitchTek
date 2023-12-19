# This file is used for creating heatmaps for the 4 types of pitches
# Dimensions of dummy heat map, strikezone.jpg: 195 x 258
#
# NOTE: The heat map is from the catchers perspective
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.patches as patches

def make_heat_map(pitch_type):
    path='../uploads/savant_data_2.csv'
    df = pd.read_csv(path)

    # Extract values
    df = df[df['pitch_type'] == pitch_type]

    # Create a 2D histogram
    heatmap, xedges, yedges = np.histogram2d(df["plate_x"], df["plate_z"], bins=20)

    # Change the backround color
    #plt.figure(facecolor="gray")

    # Plot the heat map
    plt.imshow(heatmap.T, extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], origin='lower', cmap='Reds')

    # Set custom limits for the x and y-axis
    plt.xlim(-2., 2)
    plt.ylim(.3, 4.7)

    # Add a custom box or rectangle
    custom_box = patches.Rectangle((-.9, 1.2), 1.8, 2.6, linewidth=2, edgecolor='black', facecolor='none', label='Custom Box')
    plt.gca().add_patch(custom_box)

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
    plt.show()

    #Export the plot
    #file_name = r"..\frontend\src\assets\\" + pitch_type + "_heat_map.jpg"
    #file_name = pitch_type + "_heat_map.jpg"
    #plt.savefig(file_name, bbox_inches='tight', pad_inches=0.1)

def main():

    make_heat_map("FF")
    make_heat_map("SL")
    make_heat_map("CU")
    make_heat_map("CH")


main()