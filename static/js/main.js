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

// Getstation Functions to Fetch our Stations data from the API request call
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

// addMarkers Function connects to the JSON file of bike_stations to acquire data

function addMarkers(stations) {
    console.log("Adding markers for", stations.length, "stations");
// For loop to iterate through each station on JSON
    // Required to parse data as float or else data is unreadable as "object"
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
                map: map,  // This should now reference the global map variable
                // Here we are accessing the JSON file, and categorically assigning data to variables which we will access later on
                title: station.name || station.address,
                station_number: station.number,
                available_bikes: station.available_bikes,
                available_bike_stands: station.available_bike_stands,
                bike_stands: station.bike_stands,
            });

            // Add info window for each marker
            const infoWindow = new google.maps.InfoWindow({
                content: `
                    <div>
                        <h3>${station.name || station.address}</h3>
                        <p><strong>Address:</strong> ${station.address || "N/A"}</p>
                        <p><strong>Bikes Available:</strong> ${station.available_bikes || "N/A"}</p>
                        <p><strong>Bike Stands</strong>${station.bike_stands || "N/A"}</p>
                        <p><strong>Bikes Stands Available:</strong> ${station.available_bike_stands|| "N/A"}</p>
                    </div>
                `
            });

            // Add click event listener to open info window
            marker.addListener("click", () => {
                infoWindow.open(map, marker);
            });

            // Console log required for debugging on developer console.
            console.log("Marker added for:", marker.getTitle());
        } else {
            console.warn("Invalid position for station:", station);
        }
    }

}