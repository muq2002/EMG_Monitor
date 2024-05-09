import os
import pickle
import numpy as np

def rf_model_run(features):
    model_path = "models/rf_model.pkl"  # Update this path as needed
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")

    with open(model_path, "rb") as f:
        rf_model = pickle.load(f)

    rf_prediction = rf_model.predict([features])
    return rf_prediction[0]


def calculate_rms(values):
    if not values:
        return 0
    squared_values = np.square(values)
    mean_squared = np.mean(squared_values)
    rms = np.sqrt(mean_squared)
    return rms


def calculate_zero_crossing(values):
    if not values:
        return 0
    zero_crossing_count = 0
    for i in range(1, len(values)):
        if values[i - 1] * values[i] < 0:
            zero_crossing_count += 1
    return zero_crossing_count


def determine_fatigue(rms_value, zc_value):
    prediction_value = rf_model_run([rms_value, zc_value])
    if prediction_value == 0:
        return "Normal"
    else:
        return "High"
