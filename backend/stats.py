import pandas as pd
import matplotlib.pyplot as plt

class Stats:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def plot_box_and_whisker_pitch_number(self):
        # Read the CSV file
        data = pd.read_csv(self.csv_file)

        # Check if 'pitch_number' column exists
        if 'pitch_number' not in data.columns:
            print("Column 'pitch_number' not found in the CSV file.")
            return

        # Extract the 'pitch_number' column
        pitch_data = data['pitch_number']

        # Create a box and whisker plot
        plt.figure(figsize=(10, 6))
        plt.boxplot(pitch_data, vert=False)
        plt.title("Box and Whisker Plot of 'pitch_number'")
        plt.xlabel("Pitch Number")
        plt.show()
