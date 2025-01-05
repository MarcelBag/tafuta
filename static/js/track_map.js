// track_map.js

// Initialize the map
const map = L.map('map').setView([-1.286389, 36.817223], 6); // Default to Nairobi, Kenya

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Fetch tracked numbers with geolocation data
async function fetchTrackedLocations() {
    try {
        const response = await fetch('/api/tracked-locations'); // Ensure this endpoint exists in the backend
        const data = await response.json();

        data.forEach(location => {
            if (location.latitude && location.longitude) {
                // Add marker for each location
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

// Call the function to load data on page load
fetchTrackedLocations();
