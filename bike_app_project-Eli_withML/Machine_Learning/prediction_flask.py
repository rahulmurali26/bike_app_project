from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import numpy as np
import pickle
import os
import requests
import joblib
import pandas as pd

# Dynamically build paths based on the current file's location
base_dir = os.path.dirname(__file__)
model_path = os.path.join(base_dir, "bike_availability_model.pkl")
csv_path = os.path.join(base_dir, "final_merged_data (1).csv")

# Confirm files exist
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at: {model_path}")
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV file not found at: {csv_path}")

# Load the model and data
model = joblib.load(model_path)
data = pd.read_csv(csv_path)
# Load the trained model
model_path = "Machine_Learning/bike_availability_model.pkl"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file '{model_path}' not found.")

with open(model_path, "rb") as file:
    model = pickle.load(file)

# Weather fetch function (replace with real API if needed)
def fetch_openweather_forecast(city, date):
    """
    Fetch weather forecast for a given city using OpenWeatherMap API.
    """
    API_KEY = "72e7bbdfdba07b96a4290bf1506742af"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)
        response.raise_for_status()
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "precipitation": 0.0  # OpenWeather current API doesn't give direct precipitation; set default
        }
    except Exception as e:
        raise Exception(f"Weather API error: {str(e)}")

# Initialize Flask app
app = Flask(__name__)

@app.route("/predict", methods=["GET"])
def predict():
    try:
        # Get query parameters
        date = request.args.get("date")       # format: YYYY-MM-DD
        time = request.args.get("time")       # format: HH:MM:SS
        station_id = request.args.get("station_id")
        city = request.args.get("city", "Dublin")  # default to Dublin if not provided

        if not date or not time or not station_id:
            return jsonify({"error": "Missing date, time, or station_id parameter"}), 400

        # Convert station_id to int
        station_id = int(station_id)

        # Fetch weather forecast
        weather = fetch_openweather_forecast(city, date)

        # Parse date and time
        dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
        hour = dt.hour
        day_of_week = dt.weekday()

        # Input features for prediction
        input_features = [
            station_id,
            weather["temperature"],  # This should correspond to 'max_grass_temperature_celsius'
            hour,
            day_of_week
        ]
        input_array = np.array(input_features).reshape(1, -1)

        # Predict
        prediction = model.predict(input_array)

        return jsonify({
            "predicted_available_bikes": round(prediction[0], 2),
            "inputs": {
                "station_id": station_id,
                "temperature": weather["temperature"],
                "hour": hour,
                "day": day_of_week
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@app.route("/predict/<int:station_id>", methods=["GET"])
def predict_24_hours(station_id):
    try:
        city = request.args.get("city", "Dublin")
        now = datetime.now()

        # Use your existing weather fetch function
        weather = fetch_openweather_forecast(city, now.date().isoformat())

        results = []

        for i in range(24):
            future_time = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=i)
            hour = future_time.hour
            day_of_week = future_time.weekday()

            input_features = [
                station_id,
                weather["temperature"],
                hour,
                day_of_week
            ]
            input_array = np.array(input_features).reshape(1, -1)
            prediction = model.predict(input_array)

            results.append([
                future_time.strftime("%H:%M"),
                round(float(prediction[0]), 2)
            ])

        return jsonify({
            "station_id": station_id,
            "predictions": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Load dataset used for prediction (adjust filename if needed)
data = pd.read_csv("Machine_Learning/final_merged_data (1).csv")
# Load the trained model (adjust path if needed)
model = joblib.load("Machine_Learning/bike_availability_model.pkl")

# Function to return predicted availability for a given station
def get_station_prediction(station_number):
    # Filter for the station of interest using the column 'station_id'
    station_data = data[data["station_id"] == station_number]
    
    if station_data.empty:
        return None


    expected_features = ['station_id','max_grass_temperature_celsius','hour', 'day']

    hourly_data = station_data.copy()

    predictions = []
    for hour in range(9, 22):
        hourly_data["hour"] = hour  # only if 'hour' is one of your expected features
        
        # If 'hour' is not in the trained feature list, you may have to remove it:
        hourly_data_for_prediction = hourly_data[expected_features]
        pred = model.predict(hourly_data_for_prediction)[0]
        predictions.append((f"{hour}:00", int(pred)))
    
    return predictions
# Run the app if this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)