
from flask import Flask, render_template
# External Scripts required to get API Request Data
# Here we are opting for server side data fetching
import jcddecaux
import weatherscrap

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


if __name__ == '__main__':
    app.run(debug=True)