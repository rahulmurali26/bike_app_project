import pandas as pd

# Load the CSV file
df = pd.read_csv('bike_data.csv')

# Check the first few columns to find the correct longitude and latitude column names
print(df.columns)

# Assuming columns are named 'longitude' and 'latitude', get unique pairs
unique_coords = df[['longitude', 'latitude']].drop_duplicates()

# Display the result
print(unique_coords)

# Optional: save to a new CSV
unique_coords.to_csv('unique_coordinates.csv', index=False)
