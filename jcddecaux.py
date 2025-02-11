import dbinfo
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


