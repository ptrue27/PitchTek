import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import graphviz

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


# Main script
if __name__ == "__main__":
    # Load the data
    file_path = 'C:/Users/davis/PitchTek-1/uploads/savant_data_2_with_labels.csv'  # Change this to your file path
    pitch_data = pd.read_csv(file_path)

    # Preprocess the data
    selected_features = ['release_speed', 'release_pos_x',
                         'release_pos_z']  # Update as needed
    target_column = 'pitch_type'
    preprocessor = PitchPredictionPreprocessor(
        pitch_data, target_column, selected_features)
    X_train, X_test, y_train, y_test = preprocessor.preprocess()

    # Train the decision tree classifier
    dt_classifier = DecisionTreeClassifier(max_depth=3, random_state=42)
    dt_classifier.fit(X_train, y_train)

    # Export and visualize the decision tree
    dot_data = export_graphviz(dt_classifier, out_file=None,
                               feature_names=selected_features,
                               class_names=dt_classifier.classes_.astype(str),
                               filled=True, rounded=True,
                               special_characters=True)

    graph = graphviz.Source(dot_data)
    # Saves the visualization as 'decision_tree_visualization.pdf'
    graph.render("decision_tree_visualization")

    print("Decision tree model trained and visualization saved as 'decision_tree_visualization.pdf'.")
