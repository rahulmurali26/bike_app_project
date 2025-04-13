import dbinfo
import json
import requests
import pandas as pd

API_KEY = dbinfo.JCKEY
CITY = dbinfo.NAME
URI = dbinfo.STATION_URI

# Function to fetch data from API
def fetch_data_from_api():
    response = requests.get(URI, params={'contract': CITY, 'apiKey': API_KEY})
    if response.status_code != 200:
        print(f"API request failed with status code {response.status_code}: {response.text}")
        exit()
    return response.json()

# Save JSON response to file
def save_json(data):
    with open('Bikes_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
        print("Raw JSON data saved to Bikes_data.json")

# Convert JSON to CSV
def json_to_csv(data):
    df = pd.DataFrame(data)
    df['latitude'] = df['position'].apply(lambda x: x['lat'])
    df['longitude'] = df['position'].apply(lambda x: x['lng'])
    df.drop("position", axis=1, inplace=True)
    df.to_csv("Bikes_data.csv", index=False)

# Main function
def get_bike_data():
    bike_data = fetch_data_from_api()
    save_json(bike_data)
    json_to_csv(bike_data)
    return bike_data

if __name__ == "__main__":
    print("Starting bike data collection...")
    data = get_bike_data()
    print(f"Successfully collected data for {len(data)} bike stations.")