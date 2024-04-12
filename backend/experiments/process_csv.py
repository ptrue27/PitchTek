import pandas as pd

# Load the CSV file
# Replace with the path to your CSV file
file_path = 'C:/Users/davis/PitchTek-2/uploads/test_data.csv'
df = pd.read_csv(file_path)

# Function to determine the data type of a column


def determine_data_type(series):
    if pd.api.types.is_numeric_dtype(series):
        return 'numeric'
    elif pd.api.types.is_datetime64_any_dtype(series):
        return 'datetime'
    elif pd.api.types.is_string_dtype(series):
        return 'string'
    else:
        return 'unknown'


# Creating a global dictionary to store each column's data
global_data_structures = {}

# Process each column in the dataframe and create a specific data structure
for column in df.columns:
    data_type = determine_data_type(df[column])

    # Convert datetime to string for JSON compatibility
    if data_type == 'datetime':
        df[column] = pd.to_datetime(df[column]).astype(str)

    global_data_structures[column] = df[column].tolist()

# Accessor function for the global data structures


def get_global_data(column_name):
    return global_data_structures.get(column_name)


# Testing the function with a sample column name
# Example: Access data from the 'release_speed' column
sample_data = get_global_data('release_speed')

# Print sample data for verification (you can remove this in production)
# Prints the first 5 elements of the 'release_speed' column
print(sample_data[:5])
