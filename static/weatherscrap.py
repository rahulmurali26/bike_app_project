import requests
import csv
import json

API_KEY = '72e7bbdfdba07b96a4290bf1506742af'  # OpenWeather API from Rahul
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather_data():
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
            print("Raw JSON data saved to weather_data.json")

        # Extract the required fields for CSV
        extracted_data = {
            "City": data.get("name", "Unknown"),
            "Temperature": data["main"]["temp"],
            "Weather": data["weather"][0]["description"],
            "Humidity": data["main"]["humidity"],
            "Wind Speed": data["wind"]["speed"]
        }

        # Save to CSV
        save_to_csv(extracted_data)

        # Return the full original API response instead of the extracted data
        return data
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

    weather_data = get_weather_data()

    if "Error" not in weather_data:
        print(weather_data)
        # Note: CSV and JSON files are already saved in the get_weather_data function
    else:
        print(weather_data["Error"])
