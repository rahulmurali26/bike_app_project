import requests
import json

API_KEY = "32445a2ba7fec842626d4eb1b5248fe4f0ac3d9d"
CITY_NAME = "dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"

response = requests.get(STATIONS_URI, params={"apiKey": API_KEY, "contract": CITY_NAME})

if response.status_code == 200:  #Check if request was successful
    data = json.loads(response.text)
    print(json.dumps(data[0], indent=4))
else:
    print("Error:", response.status_code)  # Handle errors
