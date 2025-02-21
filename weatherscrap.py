import requests
import csv

API_KEY = 'apikey'  # Replace with your actual API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    
    response = requests.get(BASE_URL, params=params)
    print("Response Status:", response.status_code)
    print("Raw Response:", response.text)  # Debugging line
    
    if response.status_code == 200:
        data = response.json()
        return {
            "City": data.get("name", "Unknown"),
            "Temperature": data["main"]["temp"],
            "Weather": data["weather"][0]["description"],
            "Humidity": data["main"]["humidity"],
            "Wind Speed": data["wind"]["speed"]
        }
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
    city = input("Enter city name: ")
    weather_data = get_weather(city)
    
    if "Error" not in weather_data:
        print(weather_data)
        save_to_csv(weather_data)
        print(f"Weather data saved to weather_data.csv")
    else:
        print(weather_data["Error"])