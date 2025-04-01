/**
 * weather.js - Handles the weather data display for UCD Bikes App
 * This file contains functions to update the UI with weather data
 * from the OpenWeather API
 */

// Function to update the weather UI with data from the API
function updateWeatherUI(weatherData) {
    console.log("Updating weather UI with data:", weatherData);

    try {
        // Update temperature (rounded to nearest integer)
        const tempElement = document.getElementById('weather-temp');
        const tempCelsius = Math.round(weatherData.main.temp);
        tempElement.textContent = `${tempCelsius}°`;

        // Update weather icon using OpenWeather icon codes
        // See: https://openweathermap.org/weather-conditions
        const iconElement = document.getElementById('weather-icon');
        const iconCode = weatherData.weather[0].icon;
        iconElement.innerHTML = `<img src="https://openweathermap.org/img/wn/${iconCode}@2x.png" 
                                alt="${weatherData.weather[0].description}" 
                                title="${weatherData.weather[0].main}">`;

        // Update wind speed (km/h)
        const windElement = document.getElementById('weather-wind');
        const windSpeed = Math.round(weatherData.wind.speed);
        windElement.textContent = `${windSpeed} km/h`;

        // Update humidity percentage
        const humidityElement = document.getElementById('weather-humidity');
        humidityElement.textContent = `${weatherData.main.humidity}%`;

        // Update temperature range (min/max)
        const tempRangeElement = document.getElementById('weather-temp-range');
        const minTemp = Math.round(weatherData.main.temp_min);
        const maxTemp = Math.round(weatherData.main.temp_max);
        tempRangeElement.textContent = `${minTemp}° / ${maxTemp}°`;

        // Update location and description
        const locationElement = document.getElementById('weather-location');
        locationElement.textContent = `${weatherData.name}, ${weatherData.weather[0].description}`;

        console.log("Weather UI updated successfully");
    } catch (error) {
        console.error("Error updating weather UI:", error);
    }
}

/**
 * Function to refresh weather data from the server
 * This can be called periodically to keep the weather information up-to-date
 */
function refreshWeatherData() {
    fetch("/weather")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Fresh weather data received:", data);
            updateWeatherUI(data);
        })
        .catch(error => {
            console.error("Error fetching weather data:", error);
        });
}

// Initialize weather data when the page loads
document.addEventListener('DOMContentLoaded', function() {
    refreshWeatherData();

    // Set up automatic weather refresh every 30 minutes (1800000 ms)
    setInterval(refreshWeatherData, 1800000);
});