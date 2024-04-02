import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file into a DataFrame
df = pd.read_csv('C:/Users/davis/PitchTek-2/uploads/first_pitch.csv')

# Combine 'balls' and 'strikes' into a single 'count' column to represent the pitch count as a string (e.g., "0-0", "1-2")
df['count'] = df['balls'].astype(str) + '-' + df['strikes'].astype(str)

# Group the data by 'count' and 'pitch_type', then count the occurrences
pitch_count_summary = df.groupby(['count', 'pitch_type']).size().unstack(fill_value=0)

# Plot the data
plt.figure(figsize=(12, 8))
sns.heatmap(pitch_count_summary, annot=True, fmt="d", cmap="YlGnBu")
plt.title('Number of Pitches Thrown for Each Count')
plt.xlabel('Pitch Type')
plt.ylabel('Count (Balls-Strikes)')
plt.xticks(rotation=45)

# Save the figure to a specific directory
save_path = './frontend/src/assets/heatMapOFCounts.png'  # Replace 'your_directory/your_filename.png' with your desired path and filename
plt.savefig(save_path)  # Show the plot as well (optional, can be removed if you only want to save the file)


# Combine 'balls' and 'strikes' into a single 'count' column to represent the pitch count as a string (e.g., "0-0", "1-2")
df['count'] = df['balls'].astype(str) + '-' + df['strikes'].astype(str)

# Group the data by 'count' and 'description', then count the occurrences
count_description_summary = df.groupby(['count', 'description']).size().unstack(fill_value=0)

# Plot the data using a heatmap
plt.figure(figsize=(14, 10))
sns.heatmap(count_description_summary, annot=True, fmt="d", cmap="YlGnBu", linewidths=.5)
plt.title('Frequency of Pitch Outcomes for Each Count')
plt.xlabel('Pitch Outcome')
plt.ylabel('Count (Balls-Strikes)')
plt.xticks(rotation=45, ha='right')

# Save the figure to a specific directory
save_path = './frontend/src/assets/count_vs_description_heatmap.png'  # Replace with your desired path and filename
plt.savefig(save_path)

# Select the latest game date from the dataset
latest_game_date = df['game_date'].max()

# Filter the data for the latest game date
latest_game_data = df[df['game_date'] == latest_game_date]

# Sort the data chronologically by inning, inning top or bottom, and pitch number
latest_game_sorted = latest_game_data.sort_values(by=['inning', 'inning_topbot', 'pitch_number'])

# Unique pitch types in the latest game
pitch_types = latest_game_sorted['pitch_type'].unique()

# Generate a color palette with enough colors for each pitch type
colors = plt.cm.tab10(range(len(pitch_types)))

plt.figure(figsize=(16, 8))

# Plotting each pitch type in a loop
for pitch_type, color in zip(pitch_types, colors):
    # Filter the data for the current pitch type
    pitch_type_data = latest_game_sorted[latest_game_sorted['pitch_type'] == pitch_type]
    
    # Create a chronological order for pitches regardless of the inning
    chronological_order = range(len(pitch_type_data))
    
    # Plot the pitch velocities for this pitch type
    plt.plot(chronological_order, pitch_type_data['release_speed'], label=pitch_type, marker='o', linestyle='-', color=color)

plt.title(f'Pitch Velocity by Pitch Type Throughout the Latest Game on {latest_game_date}')
plt.xlabel('Chronological Pitch Number')
plt.ylabel('Pitch Velocity (mph)')
plt.legend(title='Pitch Type')
plt.grid(True)

# Save the figure to a specific directory
save_path = './frontend/src/assets/pitchVeloLastGame.png'  # Replace with your desired path and filename
plt.savefig(save_path)

plt.show()
