import requests
import csv
import json

API_KEY = '72e7bbdfdba07b96a4290bf1506742af'  # OpenWeather API from Rahul
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather():  # Set default city to Dublin
    params = {"id": "2964574", "appid": API_KEY, "units": "metric"}

    response = requests.get(BASE_URL, params=params)
    print("Response Status:", response.status_code)
    print("Raw Response:", response.text)  # Debugging line

    if response.status_code == 200:
        # Get the raw data as JSON
        data = response.json()

        # Save the raw JSON data to a file
        with open("weather_data.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
            print("Raw JSON data saved to weather_data_raw.json")

        # Extract the required fields for CSV
        extracted_data = {
            "City": data.get("name", "Unknown"),
            "Temperature": data["main"]["temp"],
            "Weather": data["weather"][0]["description"],
            "Humidity": data["main"]["humidity"],
            "Wind Speed": data["wind"]["speed"]
        }
        return extracted_data
    else:
        return {"Error": f"API error: {response.status_code}, {response.text}"}


def save_to_csv(data, filename="weather_data.csv"):
    # Define the CSV file headers
    headers = ["City", "Temperature", "Weather", "Humidity", "Wind Speed"]

    # Write data to CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerow(data)


if __name__ == "__main__":
    # Use Dublin as the city without asking for input
    city = "Dublin"
    print(f"Getting weather data for {city}...")

    weather_data = get_weather()

    if "Error" not in weather_data:
        print(weather_data)
        save_to_csv(weather_data)
        print(f"Weather data saved to weather_data.csv")
    else:
        print(weather_data["Error"])
