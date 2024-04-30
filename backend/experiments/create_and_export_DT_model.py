import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import sqlite3


def encode_dataframe(df):
    # Get categorical columns
    categorical_columns = df.select_dtypes(include=['object']).columns

    # Create my OneHotEncoder and use it
    encoder = OneHotEncoder(sparse_output=False)
    encoded_data = encoder.fit_transform(df[categorical_columns])

    # Convert the encoded data into a DataFrame and drop categorical columns
    encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_columns))

    # Reset index of the original DataFrame
    df_reset = df.reset_index(drop=True)

    # Concatenate the original DataFrame with the encoded DataFrame
    df_encoded = pd.concat([df_reset.drop(columns=categorical_columns), encoded_df], axis=1)

    return df_encoded


def train(X_train, y_train):

    # Train the classifier
    dt_classifier = RandomForestClassifier(random_state=42)
    dt_classifier.fit(X_train, y_train)

    return dt_classifier


def get_accuracy(dt_classifier, X_test, y_test):
    y_pred = dt_classifier.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")


def create_dt(df, id):

    cols = ["pitch_type", 'release_speed', 'plate_x', 'plate_z', 'balls', 'strikes']

    # extract necessary columns
    df = df[cols]

    # Remove rows with faulty data
    df = df.dropna()

    # extract the labels from df
    labels = df["pitch_type"]
    df = df.drop(columns="pitch_type").copy()

    # Encode the data
    df = encode_dataframe(df)

    # Split data into training and testing
    X_train, X_test, y_train, y_test = train_test_split(df, labels, test_size=0.2, random_state=42)

    # Train the data
    dt_classifier = train(X_train, y_train)

    # Get Predictions
    get_accuracy(dt_classifier, X_test, y_test)

    # Export DT
    model_fileid = "../random_forest_models/" + str(id) + '.joblib'
    joblib.dump(dt_classifier, model_fileid)

def main():

    conn = sqlite3.connect('..\databases\pitches.db')
    id = 434378
    df = pd.read_sql_query(f"SELECT * FROM \"{id}\";", conn)

    create_dt(df, id)

    conn.close()


if __name__ == "__main__":
    main()
