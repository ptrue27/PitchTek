import joblib

def get_prediciton_func():
    # Load the model from the file
    loaded_model = joblib.load("DT.joblib")

    print("heyyyyy")