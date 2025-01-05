// track_map.js

// Initializing the OSMap
const map = L.map('map').setView([-1.67409, 29.22845], 13); // Default to Goma

// Adding OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Fetching tracked numbers with geolocation data
async function fetchTrackedLocations() {
    try {
        // backend endpoint for location
        const response = await fetch('/api/tracked-locations'); 
        const data = await response.json();

        data.data.forEach(location => {
            if (location.latitude && location.longitude) {
                // Adding a marker for each location
                L.marker([location.latitude, location.longitude])
                    .addTo(map)
                    .bindPopup(`
                        <strong>Phone Number:</strong> ${location.phone_number}<br>
                        <strong>Reports:</strong> ${location.reports}<br>
                        <strong>Last Location:</strong> ${location.last_location || 'Unknown'}<br>
                        <strong>Places:</strong> ${location.places || 'Unknown'}<br>
                        <strong>Network:</strong> ${location.network}
                    `);
            }
        });
    } catch (error) {
        console.error('Error fetching tracked locations:', error);
    }
}

// Calling the function to load data on page load
fetchTrackedLocations();
