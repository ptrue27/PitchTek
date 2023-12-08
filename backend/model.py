'''
I am going to use a Multilayer Perceptron for the fist version. 
Other potential models include a recurrent neural netowork and the encoder-decorer rnn.
'''
import csv
import pandas as pd
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification

file_path = '../uploads/savant_data_2_with_labels.csv'

df = pd.read_csv(file_path)

# Extract columns that I need
df =df[["pitch_type", "stand", "type", "balls", "strikes", "on_3b", "on_2b", "on_1b", 
        "outs_when_up", "inning", "pitch_number", "home_score", "away_score", "next_pitch_type"]]

# Split the dataset into training and testing sets
labels = df["next_pitch_type"]
df.drop(columns="next_pitch_type", inplace=True)
X_train, X_test, y_train, y_test = train_test_split(df, df, test_size=0.2, random_state=42)

# Build the MLP model
model = Sequential()
model.add(Dense(64, input_shape=(X_train.shape[1],), activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Evaluate the model on the test set
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}")

'''for i, column_name in enumerate(df.columns):
    print("COLUMN: ", i)
    print(column_name)
    print(df.iloc[0,i])
    print()
'''
