// Correct global variable
var map = null;
window.initMap = initMap;
// Global variable to store station data (with marker references)
var stationsData = [];

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
            // Add some minimal styling for a cleaner map look
            styles: [
                {
                    featureType: 'poi',
                    elementType: 'labels',
                    stylers: [{ visibility: 'off' }]
                },
                {
                    featureType: 'transit',
                    elementType: 'labels',
                    stylers: [{ visibility: 'simplified' }]
                }
            ]
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
            stationsData = data; // Save the station data globally
            addMarkers(data);  // Create markers after data is fetched
        })
        .catch((error) => {
            console.error("Error fetching stations:", error);
        });
}

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
        colors: ['#29acf2'], // Match header blue color
        backgroundColor: { fill:'transparent' },
        chartArea: {width: '100%', height: '60%'}
    };

    const chart = new google.visualization.LineChart(document.getElementById(containerId));
    chart.draw(data, options);
}

// Updated addMarkers Function with custom styled markers
function addMarkers(stations) {
    console.log("Adding markers for", stations.length, "stations");

    // Create a single infoWindow outside the loop to be reused
    const infoWindow = new google.maps.InfoWindow({
        // Style the info window for a cleaner look
        pixelOffset: new google.maps.Size(0, -5),
        maxWidth: 400
    });

    // Define custom marker icons
    function getCustomMarkerIcon(availableBikes, totalStands) {
        // Calculate availability percentage
        const availability = availableBikes / totalStands;
        
        // Determine color based on availability
        let fillColor;
        if (availability < 0.2) {
        // Less than 20% bikes available - Red
        fillColor = '#e53935';  // Red
        } else if (availability < 0.5) {
        // Between 20% and 50% bikes available - Orange
        fillColor = '#ff9800';  // Orange
        } else {
        // More than 50% bikes available - Green
        fillColor = '#43a047';  // Green
        }
        
        // Custom SVG marker
        return {
        path: google.maps.SymbolPath.CIRCLE,
        fillColor: fillColor,
        fillOpacity: 0.9,
        strokeColor: '#ffffff',
        strokeWeight: 2,
        scale: 12, 
        // Add a label with the number of available bikes
        labelOrigin: new google.maps.Point(0, 0)
        };
    }

    // For loop to iterate through each station from the JSON data
    for (const station of stations) {
        if (
            station.position &&
            !isNaN(parseFloat(station.position.lat)) &&
            !isNaN(parseFloat(station.position.lng))
        ) {
            // Get the custom marker icon
            const markerIcon = getCustomMarkerIcon(
                station.available_bikes, 
                station.bike_stands
            );
            
            var marker = new google.maps.Marker({
                position: {
                    lat: parseFloat(station.position.lat),
                    lng: parseFloat(station.position.lng),
                },
                map: map,
                title: station.name || station.address,
                icon: markerIcon,
                // Add a label with the number of available bikes
                label: {
                    text: String(station.available_bikes),
                    color: 'white',
                    fontSize: '10px',
                    fontWeight: 'bold'
                },
                station_number: station.number,
                available_bikes: station.available_bikes,
                available_bike_stands: station.available_bike_stands,
                bike_stands: station.bike_stands,
                animation: google.maps.Animation.DROP // Subtle animation when markers first appear
            });

            // Attach the marker to the station object
            station.marker = marker;

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

            // Create info window content
            const contentString = `
                <div style="padding: 8px; max-width: 450px; font-family: Arial, sans-serif;">
                    <h3 style="margin: 0 0 8px 0; font-size: 16px; color: #333;">${station.name || station.address}</h3>
                    <div style="display: flex; margin-bottom: 12px;">
                        <div style="flex: 1; text-align: center; padding: 8px; background: #f0f8ff; border-radius: 4px; margin-right: 4px;">
                            <div style="font-size: 20px; font-weight: bold; color: #29acf2;">${station.available_bikes}</div>
                            <div style="font-size: 12px; color: #666;">Bikes</div>
                        </div>
                        <div style="flex: 1; text-align: center; padding: 8px; background: #f0f8ff; border-radius: 4px;">
                            <div style="font-size: 20px; font-weight: bold; color: #29acf2;">${station.available_bike_stands}</div>
                            <div style="font-size: 12px; color: #666;">Stands</div>
                        </div>
                    </div>
                    <p style="font-size: 12px; color: #666; margin-bottom: 8px;">
                        <strong>Address:</strong> ${station.address || "N/A"}
                    </p>
                    <p style="font-size: 11px; color: #999; margin-bottom: 12px;">
                        Last updated: ${formattedUpdate}
                    </p>
                    <div id="chart_div_${station.number}" style="width: 100%; height: 162px;"></div>
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
                                    chartDiv.innerHTML = "<p style='color:#666; font-size:12px; text-align:center;'>Failed to load chart data</p>";
                                }
                            });
                    }, 300); // Giving the info window time to open and render
                };
            })(contentString, station.number));
            
            // Add hover effect to make the marker larger when moused over
            marker.addListener('mouseover', function() {
                this.setIcon({
                    ...markerIcon,
                    scale: 12
                });
            });
            
            marker.addListener('mouseout', function() {
                this.setIcon(markerIcon);
            });
        }
    }
}

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
        colors: ['#29acf2'], // Match header blue color
        backgroundColor: { fill:'transparent' },
        chartArea: {width: '80%', height: '70%'}
    };

    const chart = new google.visualization.LineChart(document.getElementById(containerId));
    chart.draw(data, options);
}

// function to search through thee global array defined at the start for stations and open their pop up when found
function searchStation() {
    // Get the search query from the input with id "search-bar"
    var query = document.getElementById("search-bar").value.toLowerCase().trim();
    var found = false;
    
    // Loop through the global stationsData array
    for (var i = 0; i < stationsData.length; i++) {
        var station = stationsData[i];
        // Use station.name (or fallback to station.address) for matching
        var stationLabel = (station.name || station.address).toLowerCase();
        if (stationLabel.includes(query)) {
            if (station.marker) {
                // Pan the map to the station's marker and trigger its click event
                map.panTo(station.marker.getPosition());
                map.setZoom(15); // Zoom in slightly for better visibility
                google.maps.event.trigger(station.marker, "click");
                found = true;
                break; // Stop after the first match; adjust as needed
            }
        }
    }
    
    if (!found) {
        alert("No station found matching your search.");
    }
}
document.addEventListener("DOMContentLoaded", function() {
    var searchInput = document.getElementById("search-bar");
    if (searchInput) {
        searchInput.addEventListener("keydown", function(event) {
            if (event.key === "Enter") {
                searchStation();
            }
        });
    }
});