import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm.auto import tqdm
import squarify

tqdm.pandas()

# Load the data from the uploaded CSV file
# Replace 'your_uploaded_file.csv' with the actual file path
df = pd.read_csv('C:/Users/davis/PitchTek-1/uploads/savant_data_2_with_labels.csv')

# Summarize the data for the treemap
pitch_counts = df.groupby(['pitch_number', 'pitch_type']
                          ).size().reset_index(name='total')

# Get the counts for the largest category to set the scale for the treemap
max_count = pitch_counts['total'].max()

# Prepare the data
labels = pitch_counts.apply(lambda x: str(
    x['pitch_type']) + "\n" + str(x['pitch_number']), axis=1)
sizes = pitch_counts['total']
colors = [plt.cm.Spectral(i/float(len(labels))) for i in range(len(labels))]

# Plot
plt.figure(figsize=(12, 8))
squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.6)
plt.axis('off')
plt.title('Treemap of Pitch Types per Count')
plt.show()
