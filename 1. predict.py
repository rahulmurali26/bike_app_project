import pandas as pd
import pickle

# Load the saved model
with open("bike_availability_model.pkl", "rb") as file:
    model = pickle.load(file)

# Define new input data for prediction
new_data = pd.DataFrame({
    'station_id': [32],
    'max_grass_temperature_celsius': [20],
    'hour': [9],
    'day': [2]  # Example: 0 = Monday, 1 = Tuesday, etc.
})

# Make prediction
prediction = model.predict(new_data)
# Output prediction
print(f"Predicted number of available bikes: {prediction[0]}")

