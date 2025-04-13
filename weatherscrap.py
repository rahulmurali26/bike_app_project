import requests
import json
import csv

API_KEY = '72e7bbdfdba07b96a4290bf1506742af'  # OpenWeather API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}

    response = requests.get(BASE_URL, params=params)
    print("Response Status:", response.status_code)
    print("Raw Response:", response.text)  # Debugging line

    if response.status_code == 200:
        data = response.json()

        # Save JSON data to file
        with open("weather_data.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
            print("Raw JSON data saved to weather_data.json")

        # Extract needed fields
        extracted_data = {
            "City": data.get("name", "Unknown"),
            "Temperature": data["main"]["temp"],
            "Weather": data["weather"][0]["description"],
            "Humidity": data["main"]["humidity"],
            "Wind Speed": data["wind"]["speed"]
        }

        # Save to CSV
        save_to_csv(extracted_data)

        return extracted_data
    else:
        return {"Error": f"API error: {response.status_code}, {response.text}"}

def save_to_csv(data, filename="weather_data.csv"):
    headers = ["City", "Temperature", "Weather", "Humidity", "Wind Speed"]

    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerow(data)

if __name__ == "__main__":
    city = input("Enter city name: ")
    weather_data = get_weather(city)

    if "Error" not in weather_data:
        print(weather_data)
        print("Weather data saved to weather_data.csv and weather_data.json")
    else:
        print(weather_data["Error"])