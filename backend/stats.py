import pandas as pd

# Replace 'your_file.csv' with the path to your CSV file
df = pd.read_csv('uploads\savant_data_2_with_labels.csv')

# Initialize the main list and a temporary sublist
main_list = []
sublist = []

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    # Add row data to the sublist
    sublist.append(row.tolist())

    # Check if the 'events' column has a value
    if pd.notna(row['events']):
        # If an event is found, append the sublist to the main list and start a new sublist
        main_list.append(sublist)
        sublist = []

# Don't forget to add the last sublist if it's not empty
if sublist:
    main_list.append(sublist)

# main_list now contains your data organized as a list of lists
print(main_list)