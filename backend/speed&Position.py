import numpy as np
from sklearn.ensemble import RandomForestRegressor


class PositionPredictor:
    def __init__(self):
        """
        Initialize the PositionPredictor class.
        """
        self.model = RandomForestRegressor()

    def train(self, X_train, y_train):
        """
        Train the model with the given training data.

        :param X_train: Training data features (e.g., current positions, timestamps)
        :param y_train: Training data labels (e.g., next positions)
        """
        self.model.fit(X_train, y_train)

    def predict(self, X):
        """
        Predict the next position based on the input data.

        :param X: Input data for making predictions
        :return: Predicted next positions
        """
        return self.model.predict(X)


# Example usage
if __name__ == "__main__":
    # Example data (this should be replaced with your actual data)
    X_train = np.array([[1, 2], [2, 3], [3, 4]])  # Current positions
    y_train = np.array([[2, 3], [3, 4], [4, 5]])  # Next positions

    predictor = PositionPredictor()
    predictor.train(X_train, y_train)

    # Predict the next position for a new data point
    X_new = np.array([[4, 5]])
    next_position = predictor.predict(X_new)
    print(f"Predicted next position: {next_position}")
