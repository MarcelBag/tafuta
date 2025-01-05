// Initializing the OSMap
const map = L.map('map').setView([-1.67409, 29.22845], 13); // Default to Goma

// Adding OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Nominatim reverse geocoding API URL
const NOMINATIM_URL = 'https://nominatim.openstreetmap.org/reverse?format=jsonv2';

// Fetching tracked numbers with geolocation data
async function fetchTrackedLocations() {
    try {
        const response = await fetch('/api/tracked-locations');
        const result = await response.json(); // Correctly parse the result
        const locations = result.data; // Access the array using result.data

        console.log('Fetched tracked data:', locations); // Debugging log

        const markers = []; // Array to store marker positions

        // Use for...of loop for proper async handling
        for (const location of locations) {
            const lat = parseFloat(location.lat);
            const long = parseFloat(location.long);

            if (!isNaN(lat) && !isNaN(long)) {
                console.log(`Adding marker at Lat: ${lat}, Long: ${long}, Phone: ${location.phone_number}`);

                // Reverse geocode to get the street name
                const streetName = await getStreetName(lat, long);

                const popupContent = `
                    <div>
                        <strong>Phone Number:</strong> ${location.phone_number}<br>
                        <strong>Places:</strong> ${streetName || location.city}<br>
                        <strong>Date & Time:</strong> ${location.tracked_at}
                    </div>
                `;

                const marker = L.marker([lat, long]).addTo(map);
                let popupClicked = false; // Flag to track if popup was clicked

                marker.bindPopup(popupContent, { closeOnClick: false });

                marker.on('mouseover', function () {
                    if (!popupClicked) {
                        marker.openPopup();
                    }
                });

                marker.on('mouseout', function () {
                    if (!popupClicked) {
                        marker.closePopup();
                    }
                });

                marker.on('click', function () {
                    popupClicked = true;
                    marker.openPopup();
                });

                map.on('popupclose', function () {
                    popupClicked = false;
                });

                markers.push([lat, long]); // Add marker position
            } else {
                console.error(`Invalid coordinates for ${location.phone_number}: ${location.lat}, ${location.long}`);
            }
        }

        if (markers.length > 0) {
            map.fitBounds(markers); // Adjust the map view to fit all markers
        }
    } catch (error) {
        console.error('Error fetching tracked locations:', error);
    }
}

// Function to get the street name using Nominatim reverse geocoding
async function getStreetName(lat, long) {
    try {
        const response = await fetch(`${NOMINATIM_URL}&lat=${lat}&lon=${long}`);
        const data = await response.json();
        return data.address.road || data.display_name || 'Unknown Street';
    } catch (error) {
        console.error('Error fetching street name:', error);
        return 'Unknown Street';
    }
}

// Calling the function to load data on page load
fetchTrackedLocations();
