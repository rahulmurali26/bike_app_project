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
=======
import requests
import json

import csv

import pandas as pd

r = requests.get(dbinfo.STATION_URI,params={"apiKey": dbinfo.JCKEY, "contract": dbinfo.NAME})

data = json.loads(r.text)

print(type(data))

csv_file = "output.csv"

df = pd.DataFrame(data)

df.to_csv("output.csv", index=False)


>>>>>>> 9135fdb018f7a8b0c4d50dc25c0d3c22857bd917
