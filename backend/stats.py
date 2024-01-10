import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Data Preprocessing Class


class PitchPredictionPreprocessor:
    def __init__(self, dataframe, target_column, features):
        self.dataframe = dataframe
        self.target_column = target_column
        self.features = features

    def preprocess(self):
        df = self.dataframe[self.features + [self.target_column]].copy()
        imputer = SimpleImputer(strategy='mean')
        df[self.features] = imputer.fit_transform(df[self.features])
        label_encoder = LabelEncoder()
        df[self.target_column] = label_encoder.fit_transform(
            df[self.target_column])
        X = df[self.features]
        y = df[self.target_column]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        return X_train, X_test, y_train, y_test

# Model Training and Prediction Class


class PitchTypePredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X):
        return self.model.predict(X)

    def evaluate(self, X_test, y_test):
        y_pred = self.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        class_report = classification_report(y_test, y_pred)
        return accuracy, class_report

# Visualization Function


def create_and_save_visualizations(data, features, target_column, file_path_prefix):
    # Distribution of Pitch Types
    plt.figure(figsize=(10, 6))
    sns.countplot(data=data, x=target_column)
    plt.title('Distribution of Pitch Types')
    plt.ylabel('Frequency')
    plt.xlabel('Pitch Type')
    plt.savefig(f'{file_path_prefix}_pitch_type_distribution.png')

    # Release Speed Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(data[features[0]], kde=True)
    plt.title('Release Speed Distribution')
    plt.xlabel('Release Speed')
    plt.ylabel('Frequency')
    plt.savefig(f'{file_path_prefix}_release_speed_distribution.png')

    # Release Position Distribution
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=data[features[1]], y=data[features[2]])
    plt.title('Release Position Distribution')
    plt.xlabel('Release Position X')
    plt.ylabel('Release Position Z')
    plt.savefig(f'{file_path_prefix}_release_position_distribution.png')


# Main Script
if __name__ == "__main__":
    # Load the data
    file_path = 'C:/Users/davis/PitchTek-2/uploads/test_data.csv'
    pitch_data = pd.read_csv(file_path)

    # Preprocess the data
    selected_features = ['release_speed', 'release_pos_x', 'release_pos_z']
    target_column = 'pitch_type'
    preprocessor = PitchPredictionPreprocessor(
        pitch_data, target_column, selected_features)
    X_train, X_test, y_train, y_test = preprocessor.preprocess()

    # Train and evaluate the model
    predictor = PitchTypePredictor()
    predictor.train(X_train, y_train)
    accuracy, class_report = predictor.evaluate(X_test, y_test)

    # Print model evaluation results
    print(f"Model Accuracy: {accuracy}")
    print("Classification Report:")
    print(class_report)

    # Create and save visualizations
    visualization_file_path_prefix = 'C:/Users/davis/PitchTek-2/uploads'
    create_and_save_visualizations(
        pitch_data, selected_features, target_column, visualization_file_path_prefix)

    print("Visualizations created and saved.")
