// Correct global variable
var map = null;
window.initMap = initMap;

// Initialize and add the map
function initMap() {
    // Set default location to Dublin, Ireland
    const dublin = {lat: 53.35014, lng: -6.266155};
    console.log("Dublin coordinates set: ", dublin);

    // Get the DOM element where the map will be rendered
    const mapElement = document.getElementById("map");
    if (!mapElement) {
        console.error("Map element not found in the DOM");
        return;
    }
    console.log("Map element found", mapElement);

    // Create the map, centered at Dublin - ONLY CREATE ONE MAP INSTANCE
    try {
        // Assign to the global map variable
        map = new google.maps.Map(mapElement, {
            zoom: 14,
            center: dublin,
        });
        console.log("Map created successfully");
    } catch (error) {
        console.error("Error creating map instance", error);
        return;
    }

    // Fetch stations data after the map is created
    getStations();
}

// getstation Functions to Fetch our Stations data from the API request call
// Included debugging logs which helped in debugging
function getStations() {
    fetch("/stations")
        .then((response) => {
            if (!response.ok) {
                throw new Error("HTTP error! status: " + response.status);
            }
            return response.json();
        })
        .then((data) => {
            console.log("Fetched station data:", data);
            addMarkers(data);  // Only call addMarkers after data is fetched
        })
        .catch((error) => {
            console.error("Error fetching stations:", error);
        });
}

// addMarkers Function connects to the JSON file of bike_stations to acquire data, display markers and map data to the releveant marker
// Enhanced to update the sidebar when a station is clicked
// Extra Javascript Console Log included for debugging.
// Load Google Charts
google.charts.load('current', {'packages':['corechart']});

// This function draws the chart into the Info Window
function drawTimeSeriesChart(dataArray, containerId) {
    const data = new google.visualization.DataTable();
    data.addColumn('string', 'Time');
    data.addColumn('number', 'Available Bikes');

    // Populate DataTable with your JSON data
    dataArray.forEach(item => {
        data.addRow([item.time, item.available_bikes]);
    });

    const options = {
        title: 'Trend of Available Bikes from 09:00 to 21:00',
        height: 200,
        legend: { position: 'bottom' },
        curveType: 'function',
        colors: ['#4285F4'],
        backgroundColor: { fill:'transparent' },
        chartArea: {width: '80%', height: '70%'}
    };

    const chart = new google.visualization.LineChart(document.getElementById(containerId));
    chart.draw(data, options);
}

// addMarkers Function connects to the JSON file of bike_stations to acquire data, display markers and map data to the releveant marker
// Enhanced to update the sidebar when a station is clicked
// Extra Javascript Console Log included for debugging.
function addMarkers(stations) {
    console.log("Adding markers for", stations.length, "stations");

    // Create a single infoWindow outside the loop to be reused
    const infoWindow = new google.maps.InfoWindow();

    // For loop to iterate through each station on JSON
    for (const station of stations) {
        if (
            station.position &&
            !isNaN(parseFloat(station.position.lat)) &&
            !isNaN(parseFloat(station.position.lng))
        ) {
            var marker = new google.maps.Marker({
                position: {
                    lat: parseFloat(station.position.lat),
                    lng: parseFloat(station.position.lng),
                },
                map: map,
                title: station.name || station.address,
                station_number: station.number,
                available_bikes: station.available_bikes,
                available_bike_stands: station.available_bike_stands,
                bike_stands: station.bike_stands,
            });

            // Convert the timestamp to a readable 24-hour format
            const lastUpdated = new Date(station.last_update);
            const formattedUpdate = lastUpdated.toLocaleString('en-GB', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                hour12: false // 24-hour format
            });

            // Create the content for this specific marker, including a div for the chart
            const contentString = `
                <div>
                    <h3>${station.name || station.address}</h3>
                    <p><strong>Address:</strong> ${station.address || "N/A"}</p>
                    <p><strong>Bikes Available:</strong> ${station.available_bikes || "N/A"}</p>
                    <p><strong>Bike Stands:</strong> ${station.bike_stands || "N/A"}</p>
                    <p><strong>Bikes Stands Available:</strong> ${station.available_bike_stands || "N/A"}</p>
                    <p><strong>Last Updated:</strong> ${formattedUpdate}</p>
                    <div id="chart_div_${station.number}" style="width: 300px; height: 200px;"></div>
                </div>`;

            // Add click event listener to the marker with closure for contentString and station
            marker.addListener("click", (function(contentString, stationNumber) {
                return function() {
                    // Set content for this specific marker
                    infoWindow.setContent(contentString);

                    // Open info window on this marker
                    infoWindow.open(map, this);

                    // Allow DOM to render before fetching data
                    setTimeout(() => {
                        // Fetch availability data and draw chart after the info window is opened
                        console.log("Fetching availability data for station:", stationNumber);
                        fetch('/availability?station=' + stationNumber)
                            .then(response => {
                                if (!response.ok) {
                                    throw new Error('Network response was not ok: ' + response.status);
                                }
                                return response.json();
                            })
                            .then(data => {
                                console.log("Received availability data:", data);
                                // The chart div should exist in the DOM now that the info window is open
                                drawTimeSeriesChart(data, 'chart_div_' + stationNumber);
                            })
                            .catch(error => {
                                console.error('Error fetching availability:', error);
                                const chartDiv = document.getElementById('chart_div_' + stationNumber);
                                if (chartDiv) {
                                    chartDiv.innerHTML = "<p>Failed to load chart data</p>";
                                }
                            });
                    }, 300); // Giving the info window time to open and render
                };
            })(contentString, station.number));
        }
    }
}