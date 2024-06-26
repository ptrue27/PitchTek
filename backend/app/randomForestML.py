import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from matplotlib.patches import Ellipse
from sklearn.metrics import accuracy_score

def load_and_preprocess_data(csv_path):
    data = pd.read_csv(csv_path)
    data = data[['release_speed', 'plate_x', 'plate_z',
                 'balls', 'strikes', 'pitch_type']].dropna()
    label_encoder = LabelEncoder()
    data['pitch_type_encoded'] = label_encoder.fit_transform(
        data['pitch_type'])
    return data, label_encoder


def train_model(X, y):
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    return model

def predict_and_estimate_error(model, label_encoder, release_speed, plate_x, plate_z, balls, strikes):
    global X_train, y_train  # Ensure these are defined globally
    input_features = pd.DataFrame({
        'release_speed': [release_speed],
        'plate_x': [plate_x],
        'plate_z': [plate_z],
        'balls': [balls],
        'strikes': [strikes]
    })
    pitch_type_encoded = model.predict(input_features)
    pitch_type = label_encoder.inverse_transform(pitch_type_encoded)[0]
    similar_pitches = X_train[y_train == pitch_type_encoded[0]]
    plate_x_mean = similar_pitches['plate_x'].mean()
    plate_z_mean = similar_pitches['plate_z'].mean()
    plate_x_std = similar_pitches['plate_x'].std()
    plate_z_std = similar_pitches['plate_z'].std()
    plate_x_error = plate_x_std
    plate_z_error = plate_z_std

    # Returning the pitch type, location as a tuple, and errors as another tuple
    return pitch_type, (plate_x_mean, plate_z_mean), (plate_x_error, plate_z_error)


def predict_next_pitch_type(data, balls, strikes):
    # Filter pitches by current count
    pitches_in_count = data[(data['balls'] == balls) &
                            (data['strikes'] == strikes)]
    if not pitches_in_count.empty:
        # Find the most common pitch type in this count
        most_common_pitch = pitches_in_count['pitch_type'].mode()[0]
        return most_common_pitch
    else:
        return "No data available for this count"


def visualize_prediction_with_error(pitch_type, location, error):
    fig, ax = plt.subplots()
    ax.set_xlim(-3, 3)
    ax.set_ylim(0, 6)
    ax.axhline(y=1.5, color='green', linestyle='--',
               label='Bottom of Strike Zone')
    ax.axhline(y=3.5, color='green', linestyle='--',
               label='Top of Strike Zone')
    ax.axvline(x=-0.708, color='green', linestyle='--',
               label='Left Edge of Strike Zone')
    ax.axvline(x=0.708, color='green', linestyle='--',
               label='Right Edge of Strike Zone')
    ax.set_title('Predicted Pitch Location with Error Margin')
    ax.set_xlabel('Plate X')
    ax.set_ylabel('Plate Z')
    ax.legend()
    ax.grid(True)
    ax.plot(location[0], location[1], 'ro', label='Estimated Pitch Location')
    error_ellipse = Ellipse(
        xy=location, width=2*error[0], height=2*error[1], edgecolor='r', fc='None', lw=2, label='Error Margin')
    ax.add_patch(error_ellipse)
    ax.legend()
    plt.show()



def main():
    csv_path = 'backend/uploads/file.csv'
    data, label_encoder = load_and_preprocess_data(csv_path)
    global X_train, y_train, X_test, y_test
    X = data[['release_speed', 'plate_x', 'plate_z', 'balls', 'strikes']]
    y = data['pitch_type_encoded']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = train_model(X_train, y_train)

    # Calculate accuracy on the test set
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred) * 100
    print(f"Model accuracy on test data: {accuracy:.2f}%")

        
    try:
        while True:
            release_speed_input = input("Enter the release speed of the pitch (mph) or type 'quit' to exit: ")
            if release_speed_input.lower() == 'quit':
                break

            release_speed = float(release_speed_input)
            if release_speed < 0 or release_speed > 110:
                raise ValueError("Release speed must be between 0 and 110 mph.")

            plate_x = float(input("Enter the last pitch's plate_x position: "))
            if plate_x < -4 or plate_x > 4:
                raise ValueError("Plate X position must be between -4 and 4.")

            plate_z = float(input("Enter the last pitch's plate_z position: "))
            if plate_z < 0 or plate_z > 6:
                raise ValueError("Plate Z position must be between 0 and 6.")

            balls = int(input("Enter the current number of balls: "))
            if balls < 0 or balls > 4:
                raise ValueError("Number of balls must be between 0 and 4.")

            strikes = int(input("Enter the current number of strikes: "))
            if strikes < 0 or strikes > 3:
                raise ValueError("Number of strikes must be between 0 and 3.")

            pitch_type, location, error = predict_and_estimate_error(
                model, label_encoder, release_speed, plate_x, plate_z, balls, strikes)
            visualize_prediction_with_error(pitch_type, location, error)

            # Predict the most likely next pitch type based on the count
            next_pitch_type = predict_next_pitch_type(data, balls, strikes)
            print(f"The most likely next pitch type is: {next_pitch_type}")

    except ValueError as e:
        print(f"Input error: {e}")
if __name__ == "__main__":
    main()