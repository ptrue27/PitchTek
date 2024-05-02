import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from matplotlib.patches import Ellipse
import joblib

def load_and_preprocess_data(data):

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


def RF_prediction(release_speed, plate_x, plate_z, balls, strikes, pitcher_id):

    conn = sqlite3.connect('..\databases\pitches.db')
    data = pd.read_sql_query(f"SELECT * FROM \"{pitcher_id}\";", conn)
    conn.close()

    data, label_encoder = load_and_preprocess_data(data)

    global X_train, y_train
    X = data[['release_speed', 'plate_x', 'plate_z', 'balls', 'strikes']]
    y = data['pitch_type_encoded']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)
    model = train_model(X_train, y_train)


    pitch_type, location, error = predict_and_estimate_error(
        model, label_encoder, release_speed, plate_x, plate_z, balls, strikes)

    #visualize_prediction_with_error(pitch_type, location, error)

    # Predict the most likely next pitch type based on the count
    next_pitch_type = predict_next_pitch_type(data, balls, strikes)

    # calculate average speed for pitch type
    filtered_data = data.loc[data['pitch_type'] == next_pitch_type]
    average_release_speed = filtered_data['release_speed'].mean()

    # Temp code to generate all heat maps
    #unique_values = data['pitch_type'].unique()

    return next_pitch_type, location, average_release_speed


#def create_all_heatmaps(:)

if __name__ == "__main__":
    next_pitch_type, location, average_release_speed =(
        RF_prediction(85,0,0,0,0,"434378"))

    print(next_pitch_type, location, average_release_speed)
