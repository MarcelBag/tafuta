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
        const response = await fetch('/api/tracked-locations');
        const data = await response.json();

        console.log('Fetched tracked data:', data); // Debugging log

        const markers = []; // Array to store marker positions

        data.data.forEach(location => {
            if (location.lat && location.long) {
                const marker = L.marker([location.lat, location.long])
                    .addTo(map)
                    .bindTooltip(`
                        <strong>Phone Number:</strong> ${location.phone_number}<br>
                        <strong>Place:</strong> ${location.city}<br>
                        <strong>Date & Time:</strong> ${location.tracked_at}
                    `, {
                        permanent: false,     // Tooltip only shows on hover
                        direction: 'top'      // Position the tooltip above the marker
                    });

                markers.push([location.lat, location.long]); // Add marker position
            }
        });

        if (markers.length > 0) {
            map.fitBounds(markers); // Adjust the map view to fit all markers
        }
    } catch (error) {
        console.error('Error fetching tracked locations:', error);
    }
}

// Calling the function to load data on page load
fetchTrackedLocations();
