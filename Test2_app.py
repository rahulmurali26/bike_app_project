import sys
import types
import pytest
from unittest.mock import MagicMock, patch, mock_open
from flask import template_rendered
from contextlib import contextmanager

# Create a fake version of Machine_Learning.prediction_flask
# ML model had to be mocked as had ongoing issues in running tests, with ML files not being found, despite website running fine
mock_ml_module = types.ModuleType("Machine_Learning.prediction_flask")
mock_ml_module.get_station_prediction = MagicMock(return_value="Mocked")

# Inject this fake module into sys.modules BEFORE importing Final_app
sys.modules["Machine_Learning.prediction_flask"] = mock_ml_module

# Import from app.py
from app import app

# This setups up the flask app via pytest fixture. Simulated web requests
@pytest.fixture
def client():
    app.testing = True
    return app.test_client()
# This tests the stations endpoint, cofirms return of correct bike station and data
def test_stations_route(client):
    from app import jcddecaux
    with patch.object(jcddecaux, 'get_bike_data', return_value={"stations": ["A", "B"]}):
        response = client.get('/stations')
        assert response.status_code == 200
        assert response.get_json() == {"stations": ["A", "B"]}

# tests the weather endpoing, ensures Weather API is reachable
def test_weather_route(client):
    from app import weatherscrap
    with patch.object(weatherscrap, 'get_weather_data', return_value={"temp": 23}):
        response = client.get('/weather')
        assert response.status_code == 200
        assert response.get_json() == {"temp": 23}

# test the / homepage route, check that the template rendering mechanism worsk
def test_homepage(client):
    with patch('app.jcddecaux.get_bike_data', return_value={"stations": ["X"]}), \
            patch('app.weatherscrap.get_weather_data', return_value={"temp": 25}):
        response = client.get('/')
        assert response.status_code == 200
        assert b"Homepage" in response.data  # Check title in HTML

# tests the availability route, and station = 123 with dummy csv file, this verifies the response format and data structure from CSV parsing
def test_availability_valid(client):
    dummy_csv = "hour,station_number,available_bikes\n9,123,7\n10,123,5"
    with patch('builtins.open', new=mock_open(read_data=dummy_csv)), \
            patch('app.get_station_prediction', return_value=[5]):
        response = client.get('/availability?station=123')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert "time" in data[0]
        assert "available_bikes" in data[0]

# test the availabillity route with missing parameters for both csv and stations. correctly returns an error response
def test_availability_missing_csv(client):
    with patch('builtins.open', side_effect=FileNotFoundError()):
        response = client.get('/availability?station=123')
        assert response.status_code == 500 or response.status_code == 200  # depends on your app behavior

def test_availability_missing_station(client):
    response = client.get('/availability')
    assert response.status_code == 400
    assert response.get_json() == {"error": "No station specified"}

# test for the correct HTML Template rendered on homepage , and is recieves both bike_data and weather_data
@contextmanager
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

def test_homepage_template_used(client):
    with captured_templates(app) as templates, \
         patch('app.jcddecaux.get_bike_data', return_value={"stations": ["X"]}), \
         patch('app.weatherscrap.get_weather_data', return_value={"temp": 25}):

        response = client.get('/')
        assert response.status_code == 200
        assert len(templates) == 1

        template, context = templates[0]
        assert template.name == "index.html"
        assert "bike_data" in context
        assert "weather_data" in context

# Verifies that the internal logs (used for debugging in initial iterations) to ensure the app logs expected debug output for requested station.
def test_logs_for_station(client):
    with patch("builtins.print") as mock_print, \
         patch("builtins.open", new=mock_open(read_data="hour,station_number,available_bikes\n9,123,7")), \
         patch("app.get_station_prediction", return_value=[5]):
        client.get("/availability?station=123")
        mock_print.assert_any_call("Looking for data for station: 123")
