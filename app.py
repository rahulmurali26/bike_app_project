from flask import Flask, render_template, jsonify, request
# External Scripts required to get API Request Data
# Here we are opting for server side data fetching
import static.jcddecaux as jcddecaux 
import static.dbinfo as dbinfo
import static.weatherscrap as weatherscrap
import csv
from datetime import datetime
from Machine_Learning.prediction_flask import get_station_prediction
import json
import pandas as pd

app = Flask(__name__)

# Routine for the home page
@app.route("/")
def main():
    bike_data = jcddecaux.get_bike_data()
    weather_data = weatherscrap.get_weather_data()


    # Temporary prints to verify structure
    print("Bike Data JSON:", bike_data)
    print("Weather Data JSON:", weather_data)


    return render_template("index.html", title='Homepage', bike_data=bike_data, weather_data=weather_data)

# Route to show all the stations in json
@app.route("/stations")
def stations():
    bike_data = jcddecaux.get_bike_data()
    return bike_data


# Route to access weather data
@app.route("/weather")
def weather():
    weather_data = weatherscrap.get_weather_data()
    return weather_data


@app.route("/availability")
def availability():
    # Get the station number from the query parameters
    station_number = request.args.get('station')

    if not station_number:
        return jsonify({"error": "No station specified"}), 400

    print(f"Looking for data for station: {station_number}")

    try:
        # Target hours from 9am to 9pm
        target_hours = list(range(9, 22))

        # Initialize result structure with zeros
        result_data = []
        for hour in target_hours:
            result_data.append({
                'time': f"{hour:02d}:38",
                'available_bikes': 0  # Default to 0
            })

        try:
            # Read and process the CSV file
            with open('12hr_bike_data.csv', 'r') as file:
                # Read all rows
                reader = csv.DictReader(file)

                # Process each row
                for row in reader:
                    # Use "number" instead of "station_number"
                    csv_station = row.get('number', '').strip()

                    # Compare station numbers (both as strings to be safe)
                    if str(csv_station) == str(station_number):
                        print(f"Found matching row for station {station_number}")

                        # Use "timestamp" instead of "time"
                        time_str = row.get('timestamp', '').strip()
                        bikes_str = row.get('available_bikes', '0').strip()

                        # Try to parse the time
                        try:
                            # Parse time in format "3/15/2025 9:38"
                            time_obj = datetime.strptime(time_str, '%m/%d/%Y %H:%M')
                            hour = time_obj.hour
                            minute = time_obj.minute

                            # Only consider entries for our target hours with minutes near 38
                            if hour in target_hours and 35 <= minute <= 45:
                                try:
                                    # Parse the number of available bikes
                                    available_bikes = int(bikes_str)

                                    # Update the corresponding entry in our result data
                                    index = target_hours.index(hour)
                                    result_data[index]['available_bikes'] = available_bikes

                                    print(f"Updated data for hour {hour}: {available_bikes} bikes")
                                except ValueError:
                                    print(f"Could not convert '{bikes_str}' to integer")
                        except ValueError:
                            print(f"Could not parse time: {time_str}")

        except FileNotFoundError:
            print("CSV file not found, using sample data")
            # Generate sample data for testing
            for i, hour in enumerate(target_hours):
                result_data[i]['available_bikes'] = 10 + (hour % 10)  # Sample data with variation

        return jsonify(result_data)

    except Exception as e:
        import traceback
        print(f"Error processing availability data: {e}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@app.route("/csv_debug")
def csv_debug():
    try:
        debug_info = {
            "file_exists": False,
            "headers": [],
            "first_5_rows": [],
            "sample_data_by_station": {}
        }

        try:
            with open('12hr_bike_data.csv', 'r') as file:
                debug_info["file_exists"] = True

                # Get headers
                first_line = file.readline().strip()
                headers = first_line.split(',')
                debug_info["headers"] = headers

                # Get first 5 data rows
                for i in range(5):
                    line = file.readline().strip()
                    if line:
                        debug_info["first_5_rows"].append(line.split(','))

                # Reset and get some sample data by station
                file.seek(0)
                reader = csv.DictReader(file)
                station_samples = {}

                for row in reader:
                    station = row.get('number', '').strip()
                    if station not in station_samples:
                        station_samples[station] = []

                    if len(station_samples[station]) < 2:  # Get up to 2 samples per station
                        station_samples[station].append(dict(row))

                debug_info["sample_data_by_station"] = station_samples

        except FileNotFoundError:
            debug_info["error"] = "File not found"

        return jsonify(debug_info)

    except Exception as e:
        import traceback
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        })
    
# Load station metadata for display (e.g. marker info)
with open('Bikes_data.json') as f:  # Make sure this file exists and is correct
    stations = json.load(f)


@app.route('/average-availability')
def average_availability():
    # Load your 12-hour bike data CSV
    df = pd.read_csv('12hr_bike_data.csv')

    # Parse timestamp and extract hour
    df['timestamp'] = pd.to_datetime(df['timestamp'], format="%m/%d/%Y %H:%M")
    df['hour'] = df['timestamp'].dt.strftime('%H:00')

    # Group by hour and calculate average
    grouped = df.groupby('hour')['available_bikes'].mean().reset_index()
    grouped.columns = ['Hour', 'Average Bikes Available']

    # Convert to list of dicts for JSON response
    return jsonify(grouped.to_dict(orient='records'))

@app.route('/')
def index():
    return render_template('index.html', title='UCD Bikes', weather_data={})  # add weather if needed

@app.route('/stations')
def get_stations():
    return jsonify(stations)

@app.route('/predict/<int:station_number>')
def predict(station_number):
    print(f"Received prediction request for station {station_number}")
    predictions = get_station_prediction(station_number)
    
    if predictions is None:
        print(f"No data found for station {station_number}")
        return jsonify({'error': 'Station not found'}), 404

    print(f"Prediction data returned for station {station_number}")
    return jsonify({'predictions': predictions})

if __name__ == '__main__':
    app.run(app.run(host='0.0.0.0', port=80))