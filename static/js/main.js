

async function getTopBikeStations() {
    const response = await fetch('../data/output.csv');
    const csvText = await response.text();
    const rows = csvText.split('\n').slice(1);

    const stations = [];

    rows.forEach(row => {
        if (row.trim() !== '') {
            const [
                number, contract_name, name, address, banking, bonus, bike_stands,
                available_bike_stands, available_bikes, status, last_update, latitude, longitude
            ] = row.split(',');

            stations.push({
                name,
                address,
                available_bikes: parseInt(available_bikes, 10),
                available_bike_stands: parseInt(available_bike_stands, 10),
                total_stands: parseInt(bike_stands, 10),
                latitude: parseFloat(latitude),
                longitude: parseFloat(longitude),
                status
            });
        }
    });

    // Sort and get top 10 stations
    stations.sort((a, b) => b.available_bikes - a.available_bikes);
    const topStations = stations.slice(0, 10);

    displayStations(topStations);
    renderChart(topStations);
}

function displayStations(stations) {
    const stationList = document.getElementById('station-list');
    stationList.innerHTML = '';

    stations.forEach(station => {
        const div = document.createElement('div');
        div.classList.add('station-info');
        div.innerHTML = `
            <h3>${station.name}</h3>
            <p><strong>Address:</strong> ${station.address}</p>
            <p><strong>Available Bikes:</strong> ${station.available_bikes}</p>
            <p><strong>Open Stands:</strong> ${station.available_bike_stands}</p>
            <p><strong>Status:</strong> ${station.status}</p>
        `;
        stationList.appendChild(div);
    });
}

function renderChart(stations) {
    const ctx = document.getElementById('bikesChart').getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: stations.map(s => s.name),
            datasets: [
                {
                    label: 'Available Bikes',
                    data: stations.map(s => s.available_bikes),
                    backgroundColor: '#4CAF50'
                },
                {
                    label: 'Available Bike Stands',
                    data: stations.map(s => s.available_bike_stands),
                    backgroundColor: '#FF9800'
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top'
                },
                title: {
                    display: true,
                    text: 'Top 10 Stations by Availability'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                },
                x: {
                    ticks: {
                        callback: function(value, index, tickValues) {
                            const label = this.getLabelForValue(value);
                            return label.length > 10 ? label.slice(0,10) + '...' : label;
                        },
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
            }
        }
    });
}

window.addEventListener('load', getTopBikeStations);



// Fetch CSV data and display top bike stations
async function getTopBikeStations() {
    const response = await fetch('../data/output.csv');
    const csvText = await response.text();
    const rows = csvText.split('\n').slice(1);

    const stations = [];

    rows.forEach(row => {
        if (row.trim() !== '') {
            const [
                number, contract_name, name, address, banking, bonus, bike_stands,
                available_bike_stands, available_bikes, status, last_update, latitude, longitude
            ] = row.split(',');

            stations.push({
                name,
                address,
                available_bikes: parseInt(available_bikes, 10),
                bike_stands: parseInt(bike_stands, 10),
                latitude: parseFloat(latitude),
                longitude: parseFloat(longitude),
                status
            });
        }
    });

    // Sort by available bikes descending
    stations.sort((a, b) => b.available_bikes - a.available_bikes);

    displayStations(stations.slice(0, 10));  // display top 10 stations
}

// Display stations data on the webpage
function displayStations(stations) {
    const stationList = document.getElementById('station-list');
    stationList.innerHTML = ''; // clear existing content

    stations.forEach(station => {
        const stationDiv = document.createElement('div');
        stationDiv.className = 'station';

        stationDiv.innerHTML = `
            <h3>${station.name}</h3>
            <p><strong>Address:</strong> ${station.address}</p>
            <p><strong>Available Bikes:</strong> ${station.available_bikes}</p>
            <p><strong>Total Stands:</strong> ${station.bike_stands}</p>
            <p><strong>Status:</strong> ${station.status}</p>
        `;

        stationList.appendChild(stationDiv);
    });
}

// Load stations on page load
window.addEventListener('load', getTopBikeStations);


// Function to fetch and parse bike_data.csv
fetch('./bike_data.csv') // confirm correct path to your CSV file
    .then(response => response.text())
    .then(data => {
        const rows = data.split('\n'); // splits by line breaks to create rows

        // Extract the header (assuming one exists)
        const headers = rows.shift().split(',');

        const bikesData = rows.map(row => {
            const columns = row.split(',');
            let bikeObject = {};
            headers.forEach((header, index) => {
                bikeObject[header.trim()] = columns[index].trim();
            });
            return bikeObject;
        });

        console.log(bikesData);  // log and inspect your array of objects
    })
    .catch(error => console.error('Error loading CSV:', error));

// Function to update the current time
function updateCurrentTime() {
    const timeDisplay = document.getElementById("current-time");
    const now = new Date();

    // Format time as HH:MM:SS
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');

    timeDisplay.textContent = `${hours}:${minutes}:${seconds}`;

    // Update every second
    setTimeout(updateCurrentTime, 1000);
}

// Start the clock when the page loads
window.addEventListener('load', updateCurrentTime);

// Initialize and add the map
function initMap() {
    // Set default location to Dublin, Ireland
    const dublin = { lat: 53.3498, lng: -6.2603 };

    // Create the map, centered at Dublin
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 13,
        center: dublin,
    });

    // Fetch the CSV file with coordinates
    fetch('./unique_coordinates.csv')
        .then(response => response.text())
        .then(data => {
            // Parse the CSV data
            const rows = data.split('\n');
            // Skip the header row
            rows.shift();

            // Create markers for each coordinate
            rows.forEach(row => {
                if (row.trim() !== '') {
                    const [longitude, latitude] = row.split(',');

                    // Create marker position
                    const position = {
                        lat: parseFloat(latitude),
                        lng: parseFloat(longitude)
                    };

                    // Add marker to the map
                    const marker = new google.maps.Marker({
                        position: position,
                        map: map,
                        title: `Bike Station at ${latitude}, ${longitude}`
                    });

                    // Optional: Add click listener to each marker
                    marker.addListener("click", () => {
                        document.getElementById("station-name").textContent = `Bike Station`;
                        document.getElementById("station-address").textContent =
                            `Location: ${latitude}, ${longitude}`;
                    });
                }
            });

            // Zoom control buttons
            const zoomControlDiv = document.createElement("div");

            // Zoom in button
            const zoomInButton = document.createElement("button");
            zoomInButton.innerHTML = "+";
            zoomInButton.style.cssText = "width: 30px; height: 30px; font-size: 20px; margin: 5px;";
            zoomInButton.onclick = () => map.setZoom(map.getZoom() + 1);

            // Zoom out button (add if necessary)
            const zoomOutButton = document.createElement("button");
            zoomOutButton.innerHTML = "-";
            zoomOutButton.style.cssText = "width: 30px; height: 30px; font-size: 20px; margin: 5px;";
            zoomOutButton.onclick = () => map.setZoom(map.getZoom() - 1);

            // Add buttons to div
            zoomControlDiv.appendChild(zoomInButton);
            zoomControlDiv.appendChild(zoomOutButton);

            // Add controls to map
            map.controls[google.maps.ControlPosition.TOP_LEFT].push(zoomControlDiv);
        })
        .catch(err => console.error('Error fetching CSV file:', err));
}