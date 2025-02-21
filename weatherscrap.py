import requests

API_KEY = '72e7bbdfdba07b96a4290bf1506742af'
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

if __name__ == "__main__":
    city = input("Enter city name: ")
    weather_data = get_weather(city)
    print(weather_data)