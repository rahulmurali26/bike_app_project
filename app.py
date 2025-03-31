
from flask import Flask, render_template
# External Scripts required to get API Request Data
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

# Show all the stations in json
@app.route("/stations")
def stations():
    bike_data = jcddecaux.get_bike_data()
    return bike_data

# Route for the "about" page
# This is just a place holder for now, can mark up an about page or secondary page later (see lecture 5)
# def about():


if __name__ == '__main__':
    app.run(debug=True)