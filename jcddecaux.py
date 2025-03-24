import dbinfo
import json
import requests
import pandas as pd

# Fetch data from API
r = requests.get(dbinfo.STATION_URI, params={"7f53d1d974a374e40dfa9c54024728b0e13e8ce5": dbinfo.JCKEY, "contract": dbinfo.NAME})

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

df.to_csv("bike_data.csv", index=False)