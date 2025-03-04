import requests
import csv
import time
from datetime import datetime
import os

API_KEY = "72e7bbdfdba07b96a4290bf1506742af"  # Replace with your actual API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
CSV_FILE = "weather_data.csv"
INTERVAL = 5  # Time interval in seconds (e.g., 60s = 1 min)

def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}

    response = requests.get(BASE_URL, params=params)
    print("Response Status:", response.status_code)

    if response.status_code == 200:
        data = response.json()
        return {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "City": data.get("name", "Unknown"),
            "Temperature": data["main"]["temp"],
            "Weather": data["weather"][0]["description"],
            "Humidity": data["main"]["humidity"],
            "Wind Speed": data["wind"]["speed"]
        }
    else:
        print("API Error:", response.text)
        return None

def save_to_csv(data, filename=CSV_FILE):
    headers = ["Timestamp", "City", "Temperature", "Weather", "Humidity", "Wind Speed"]

    file_exists = os.path.isfile(filename)

    # Open file in append mode
    with open(filename, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        # If file does not exist or is empty, write headers first
        if not file_exists or os.stat(filename).st_size == 0:
            writer.writeheader()
        
        writer.writerow(data)

if __name__ == "__main__":
    city = input("Enter city name: ")
    
    while True:
        weather_data = get_weather(city)
        
        if weather_data:
            print(weather_data)
            save_to_csv(weather_data)
            print(f"Weather data saved at {weather_data['Timestamp']}")
        
        print(f"Waiting {INTERVAL} seconds before next update...\n")
        time.sleep(INTERVAL)  # Wait for the specified interval before fetching again