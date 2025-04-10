from flask import Flask, request, jsonify
from datetime import datetime
import numpy as np
import pickle
import os
import requests

# Load the trained model
model_path = "bike_availability_model.pkl"
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

# Run the app if this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)