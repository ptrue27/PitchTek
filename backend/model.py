import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

def read_in_data(file_path):

    # Read in data
    df = pd.read_csv(file_path)

    # These are the columns I will use for the algorithm
    cols = ["pitch_type", "type", "balls", "strikes",
            "outs_when_up", "inning", "pitch_number", "next_pitch_type"]

    # Extract columns that I need
    df = df[cols]

    return df


def encode_data(df):

    # Get categorical columns
    categorical_columns = df.select_dtypes(include=['object']).columns

    # Create my OneHotEncoder and use it
    encoder = OneHotEncoder(sparse=False)  
    encoded_data = encoder.fit_transform(df[categorical_columns])

    # Convert the encoded data into a DataFrame and drop categorical columns
    encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_columns))

    # Concatenate the original DataFrame with the encoded DataFrame
    df_encoded = pd.concat([df.drop(columns=categorical_columns), encoded_df], axis=1)

    return df_encoded


def main():
    
    # Read in Data to df
    df = read_in_data('../uploads/savant_data_2_with_labels.csv')

    # extract the labels from df
    labels = df["next_pitch_type"]
    df.drop(columns="next_pitch_type", inplace=True)

    # Encode the data
    df = encode_data(df)
    
    # Split data into training and testing
    X_train, X_test, y_train, y_test = train_test_split(df, labels, test_size=0.2, random_state=42)


    dt_classifier = DecisionTreeClassifier()
    dt_classifier.fit(X_train, y_train)

    y_pred = dt_classifier.predict(X_test)

    #accuracy = accuracy_score(y_test, y_pred)
    #print(f"Accuracy: {accuracy}")

main()