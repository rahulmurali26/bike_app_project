import pandas as pd
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.linear_model import LinearRegression # type: ignore
from sklearn.metrics import mean_absolute_error, r2_score # type: ignore
import joblib # type: ignore
import pickle
import os


# Load the dataset
data = pd.read_csv("final_merged_data.csv")

# Handle missing values (drop rows with NaN in lagged features)
data.dropna(inplace=True)

# Define features and target
features = ['station_id','max_grass_temperature_celsius','hour', 'day']
target = 'num_bikes_available'

X = data[features]
y = data[target]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Absolute Error: {mae}")
print(f"R² Score: {r2}")

# Display model coefficients
print("\nModel Coefficients:")
for feature, coef in zip(features, model.coef_):
    print(f"{feature}: {coef}")
print(f"Intercept: {model.intercept_}")

# Save the model to a file
model_filename = "bike_availability_model.joblib"
joblib.dump(model, model_filename)

print(f"Model saved to {model_filename}")

# Save the model to a .pkl file
model_filename = "bike_availability_model.pkl"
with open(model_filename, "wb") as file:
    pickle.dump(model, file)

print(f"Model saved to {model_filename}")
