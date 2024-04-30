import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

class DataVisualizer:

    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.df = pd.read_csv(csv_file_path)

    def generate_heatmap_of_counts(self):
        df = self.df
        df['count'] = df['balls'].astype(str) + '-' + df['strikes'].astype(str)
        pitch_count_summary = df.groupby(['count', 'pitch_type']).size().unstack(fill_value=0)
        plt.figure(figsize=(12, 8))
        sns.heatmap(pitch_count_summary, annot=True, fmt="d", cmap="YlGnBu")
        plt.title('Number of Pitches Thrown for Each Count')
        plt.xlabel('Pitch Type')
        plt.ylabel('Count (Balls-Strikes)')
        plt.xticks(rotation=45)
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf

    def generate_count_vs_description_heatmap(self):
        df = self.df
        df['count'] = df['balls'].astype(str) + '-' + df['strikes'].astype(str)
        count_description_summary = df.groupby(['count', 'description']).size().unstack(fill_value=0)
        plt.figure(figsize=(14, 10))
        sns.heatmap(count_description_summary, annot=True, fmt="d", cmap="YlGnBu", linewidths=.5)
        plt.title('Frequency of Pitch Outcomes for Each Count')
        plt.xlabel('Pitch Outcome')
        plt.ylabel('Count (Balls-Strikes)')
        plt.xticks(rotation=45, ha='right')
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf

    def generate_pitch_velocity_chart(self):
        df = self.df
        latest_game_date = df['game_date'].max()
        latest_game_data = df[df['game_date'] == latest_game_date]
        latest_game_sorted = latest_game_data.sort_values(by=['inning', 'inning_topbot', 'pitch_number'])
        pitch_types = latest_game_sorted['pitch_type'].unique()
        colors = plt.cm.tab10(range(len(pitch_types)))
        plt.figure(figsize=(16, 8))
        for pitch_type, color in zip(pitch_types, colors):
            pitch_type_data = latest_game_sorted[latest_game_sorted['pitch_type'] == pitch_type]
            chronological_order = range(len(pitch_type_data))
            plt.plot(chronological_order, pitch_type_data['release_speed'], label=pitch_type, marker='o', linestyle='-', color=color)
        plt.title(f'Pitch Velocity by Pitch Type Throughout the Latest Game on {latest_game_date}')
        plt.xlabel('Chronological Pitch Number')
        plt.ylabel('Pitch Velocity (mph)')
        plt.legend(title='Pitch Type')
        plt.grid(True)
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf
