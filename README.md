# 🚲 UCD Bikes Web App

## 📍 Overview

This is an interactive web application designed to visualize real-time Dublin Bikes availability and weather data. The application fetches live bike station data from JCDecaux and current weather conditions from OpenWeatherMap, and displays this data on a dynamic Google Map with custom-styled markers and side-panel visualizations.

---

## 🌐 Features

- 📌 Interactive map showing all Dublin bike stations with live data
- 📊 Real-time graph of bike availability per station (9 AM to 9 PM)
- 🌤️ Current weather: temperature, wind, humidity, conditions
- 🔍 Station search with instant zoom and info panel
- 📈 Station-specific trends with visual charts

---

## 🗂 File Descriptions

### `app.py`
- Main Flask server
- Handles routes:
  - `/`: homepage rendering
  - `/stations`: returns bike station data as JSON
  - `/weather`: returns current weather data
  - `/availability`: loads historical availability from CSV
  - `/csv_debug`: optional route for CSV inspection

### `jcddecaux.py`
- Connects to the JCDecaux API
- Fetches current bike station data
- Requires API key from `dbinfo.py`

### `weatherscrap.py`
- Connects to OpenWeatherMap API
- Fetches current weather for Dublin
- Uses API key from `dbinfo.py`

### `dbinfo.py`
- Stores API keys
- Example:
  ```python
  JCKEY = "your_jcdecaux_api_key"
  OPENWEATHER_KEY = "your_openweather_api_key"
