import pandas as pd
import joblib

def load_data(path):
    return pd.read_csv(path)

def save_model(model, filename):
    joblib.dump(model, filename)

def load_model(filename):
    return joblib.load(filename)
