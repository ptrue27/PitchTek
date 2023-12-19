import joblib
import pandas as pd


my_dict = {'FF': 'Fastball',
           'SL': 'Slider',
           'CU': 'Curve',
           'CH': 'Changeup'}


def get_prediciton_func(obj):

    # Load the model from the file
    loaded_model = joblib.load("DT.joblib")

    df = pd.DataFrame()

    df['outs_when_up'] = [obj['outs']]
    df['strikes'] = obj['strikes']
    df['balls'] = obj['balls']

    predictions = loaded_model.predict(df)

    return my_dict[predictions[0]]