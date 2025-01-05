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
                const popupContent = `
                    <div>
                        <strong>Phone Number:</strong> ${location.phone_number}<br>
                        <strong>Place:</strong> ${location.city}<br>
                        <strong>Date & Time:</strong> ${location.tracked_at}
                    </div>
                `;

                const marker = L.marker([location.lat, location.long]).addTo(map);
                let popupClicked = false; // Flag to track if popup was clicked

                // Bind popup with selectable content
                marker.bindPopup(popupContent, { closeOnClick: false });

                // Open the popup on hover
                marker.on('mouseover', function () {
                    if (!popupClicked) {
                        marker.openPopup();
                    }
                });

                // Close the popup on mouseout if it wasn't clicked
                marker.on('mouseout', function () {
                    if (!popupClicked) {
                        marker.closePopup();
                    }
                });

                // Keep the popup open when clicked
                marker.on('click', function () {
                    popupClicked = true; // Set flag to true
                    marker.openPopup();
                });

                // Reset flag when the popup is manually closed
                map.on('popupclose', function () {
                    popupClicked = false; // Reset flag
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
}

// Calling the function to load data on page load
fetchTrackedLocations();
