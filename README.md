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
```

### `templates/index.html`
- Jinja2 HTML template rendered by Flask  
- Embeds map, charts, and weather display logic  

---

## 🎨 Frontend Files

### `static/js/main.js`
- Initializes Google Map  
- Places and styles bike station markers  
- Loads availability trends  
- Handles station search  

### `static/js/weather.js`
- Updates weather data in the sidebar  
- Displays weather icon, temp, wind, humidity, etc.  

### `static/css_html/style.css`
- Custom styling for the app  
- Includes sidebar, map layout, buttons, weather blocks  

---

## 📦 Data Sources

- **JCDecaux API** — live bike availability: https://developer.jcdecaux.com/  
- **OpenWeatherMap API** — weather data: https://openweathermap.org/api  
- **Historic CSV File** — `12hr_bike_data.csv` for sample trend display  

---

## 🚀 How to Run the Project

1. Ensure Python is installed.
2. Install Flask:
   ```bash
   pip install flask
   ```
3. Create a file called `dbinfo.py` with your API keys:
   ```python
   JCKEY = "your_jcdecaux_api_key"
   OPENWEATHER_KEY = "your_openweather_api_key"
   ```
4. Run the server:
   ```bash
   python app.py
   ```
5. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```

---

## 📌 Notes

- Place your `index.html` in the `templates/` folder so Flask can render it.  
- Static files like JS and CSS go into the `static/` directory.
- Be sure your API keys are correct or the app will fail to fetch data.
