import dbinfo
<<<<<<< HEAD
import json
import requests
import pandas as pd

# Fetch data from API
r = requests.get(dbinfo.STATION_URI, params={"apiKey": dbinfo.JCKEY, "contract": dbinfo.NAME})

if r.status_code != 200:
    print(f"API request failed with status code {r.status_code}: {r.text}")
    exit()

# Load API response into JSON
data = json.loads(r.text)

if not data:
    print("No data received from API.")
    exit()

# Convert JSON data into DataFrame
df = pd.DataFrame(data)

# Extract latitude and longitude from 'position' field
df['latitude'] = df['position'].apply(lambda x: x['lat'])
df['longitude'] = df['position'].apply(lambda x: x['lng'])
df.drop("position", axis=1, inplace=True)

df.to_csv("output.csv", index=False)

import requests
import json

=======
<<<<<<< HEAD
import requests
import json

import csv

>>>>>>> cdd32fd (Final code)
import pandas as pd

r = requests.get(dbinfo.STATION_URI,params={"apiKey": dbinfo.JCKEY, "contract": dbinfo.NAME})

data = json.loads(r.text)

print(type(data))

csv_file = "output.csv"

df = pd.DataFrame(data)

df.to_csv("output.csv", index=False)


<<<<<<< HEAD

=======
=======
import json
import requests
import pandas as pd

API_KEY = dbinfo.JCKEY
CITY = dbinfo.NAME
URI = dbinfo.STATION_URI


# Function fetch data from API (API request)
def fetch_data_from_api():
    response = requests.get(URI, params={'contract': CITY, 'apiKey': API_KEY})
    response.raise_for_status()  # raises exception on failure
    return response.json()


# Function to save data as a JSON File
def save_json(data):
    with open('Bikes_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
        print("Raw JSON data saved to bike_data_raw.json")


# Function to save data as a CSV file
def json_to_csv(data):
    # Convert JSON data into DataFrame
    df = pd.DataFrame(data)
    # Extract latitude and longitude from 'position' field
    df['latitude'] = df['position'].apply(lambda x: x['lat'])
    df['longitude'] = df['position'].apply(lambda x: x['lng'])
    df.drop("position", axis=1, inplace=True)
    # Using the same name as the JSON file but with .csv extension
    df.to_csv('Bikes_data.csv', index=False)


# This Function returns the API request as bike_data and is accessed in our Flask App
def get_bike_data():
    bike_data = fetch_data_from_api()
    save_json(bike_data)  # Maintain existing JSON save
    json_to_csv(bike_data)  # Maintain existing CSV conversion
    return bike_data  # Returns JSON data directly for Flask***

if __name__ == "__main__":
    print("Starting bike data collection...")
    bike_data = get_bike_data()
    print(f"Successfully collected data for {len(bike_data)} bike stations")
>>>>>>> bb6317f (Updated front end)
>>>>>>> cdd32fd (Final code)
