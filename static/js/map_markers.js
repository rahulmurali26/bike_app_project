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
    fetch('/unique_coordinates.csv')
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
                        // Update sidebar with station information when clicked
                        document.getElementById("station-name").textContent = `Bike Station`;
                        document.getElementById("station-address").textContent =
                            `Location: ${latitude}, ${longitude}`;
                    });
                }
            });
        })
        .catch(error => {
            console.error('Error loading coordinates:', error);
        });
}