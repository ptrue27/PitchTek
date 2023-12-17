import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

def read_in_data(file_path, cols):

    # Read in data
    df = pd.read_csv(file_path)

    # Extract columns that I need
    df = df[cols]

    return df


def encode_data(df):

    # Get categorical columns
    categorical_columns = df.select_dtypes(include=['object']).columns

    # Create my OneHotEncoder and use it
    encoder = OneHotEncoder(sparse_output=False)
    encoded_data = encoder.fit_transform(df[categorical_columns])

    # Convert the encoded data into a DataFrame and drop categorical columns
    encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_columns))

    # Concatenate the original DataFrame with the encoded DataFrame
    df_encoded = pd.concat([df.drop(columns=categorical_columns), encoded_df], axis=1)

    return df_encoded


def train(X_train, y_train):

    # Train the classifier
    dt_classifier = DecisionTreeClassifier()
    dt_classifier.fit(X_train, y_train)

    return dt_classifier


def get_accuracy(dt_classifier, X_test, y_test):
    y_pred = dt_classifier.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")


def create_dt(path, cols):

    # Read in Data to df
    df = read_in_data(path, cols)

    # extract the labels from df
    labels = df["pitch_type"]
    df.drop(columns="pitch_type", inplace=True)

    # Encode the data
    df = encode_data(df)

    # Split data into training and testing
    X_train, X_test, y_train, y_test = train_test_split(df, labels, test_size=0.2, random_state=42)

    # Train the data
    dt_classifier = train(X_train, y_train)

    # Get Predictions
    get_accuracy(dt_classifier, X_test, y_test)


def main():

    # First pitches
    create_dt(path='../uploads/first_pitch.csv',
              cols=["pitch_type","outs_when_up", "inning", "stand", "away_team", "home_score", "away_score"])

    # following pitches
    create_dt(path='../uploads/subsequent_pitches.csv',
              cols=["pitch_type","outs_when_up", "inning", "stand", "away_team", "home_score", "away_score",
                    "pitch_number", "previous_pitch_type", "previous_pitch_result"])

main()