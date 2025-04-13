import pandas as pd
import pickle
import os
import requests
from datetime import datetime

# Load model only if it exists
model_filename = "bike_availability_model.pkl"
if not os.path.exists(model_filename):
    raise FileNotFoundError(f"Model file '{model_filename}' not found.")

with open(model_filename, "rb") as file:
    model = pickle.load(file)

def get_weather_forecast(city, date_str):
    """
    Get current weather as proxy for temperature.
    """
    params = {
        "q": city,
        "appid": "OPEN_WEATHER_API_KEY",
        "units": "metric"
    }

    response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)

    if response.status_code == 200:
        data = response.json()
        return {
            "max_grass_temperature_celsius": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "weather": data["weather"][0]["description"]
        }
    else:
        raise Exception(f"API error: {response.status_code}, {response.text}")

def predict_bike_availability(station_id, city, date_str, time_str):
    """
    Predict available bikes based on input data and weather.
    """
    try:
        date_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        hour = date_time.hour
        day_of_week = date_time.weekday()

        weather_features = get_weather_forecast(city, date_str)

        input_data = pd.DataFrame([{
            'station_id': station_id,
            'max_grass_temperature_celsius': weather_features['max_grass_temperature_celsius'],
            'hour': hour,
            'day': day_of_week
        }])

        missing_features = set(model.feature_names_in_) - set(input_data.columns)
        if missing_features:
            raise ValueError(f"Missing features in input data: {missing_features}")

        prediction = model.predict(input_data)
        return prediction[0]

    except Exception as e:
        return f"Error in prediction: {str(e)}"

# Example usage - make sure ALL variables are defined before calling the function
if __name__ == "__main__":
    city = "Dublin"
    date_str = "2024-02-25"
    time_str = "09:00"
    station_id = 42  # ✅ Make sure this is defined here!

    predicted_bikes = predict_bike_availability(station_id, city, date_str, time_str)
    print(f"Predicted number of available bikes in {city} on {date_str} at {time_str}: {predicted_bikes}")
