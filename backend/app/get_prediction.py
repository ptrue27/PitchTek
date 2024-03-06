import joblib
import pandas as pd
import random

my_dict = {'FF': 'Fastball',
           'SL': 'Slider',
           'CU': 'Curve',
           'CH': 'Changeup'}

class Predictions_Class:
    def get_type(self, obj):

        # Load the model from the file
        loaded_model = joblib.load("DT.joblib")

        df = pd.DataFrame()

        df['outs_when_up'] = [obj['outs']]
        df['strikes'] = obj['strikes']
        df['balls'] = obj['balls']

        predictions = loaded_model.predict(df)

        return my_dict[predictions[0]]


    # Right now there is zero ML in this function.
    # It just randomly changes to demonstrate functionality
    def get_speed(self, pitch_type):

        margin =  random.uniform(-5, 5)
        margin = round(margin, 1)

        if pitch_type == "Fastball":

            return 94 + margin

        elif pitch_type == "Slider":

            return 87 + margin