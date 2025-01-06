// Initializing the OSMap
const map = L.map('map').setView([-1.67409, 29.22845], 13); // Default to Goma

// Adding OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Nominatim reverse geocoding API URL
const NOMINATIM_URL = 'https://nominatim.openstreetmap.org/reverse?format=jsonv2';

let markersData = []; // Store fetched markers data globally
let userLocation = null; // Store user's current location

// Fetching tracked numbers with geolocation data
async function fetchTrackedLocations() {
    try {
        const response = await fetch('/api/tracked-locations');
        const result = await response.json();
        const locations = result.data;

        console.log('Fetched tracked data:', locations); // Debugging log

        markersData = locations; // Store data globally for search functionality
        const markers = []; // Array to store marker positions

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

                // Bind popup with the content
                marker.bindPopup(popupContent, { closeOnClick: false });

                // Show popup on hover
                marker.on('mouseover', function () {
                    if (!popupClicked) {
                        marker.openPopup();
                    }
                });

                // Hide popup on mouse out
                marker.on('mouseout', function () {
                    if (!popupClicked) {
                        marker.closePopup();
                    }
                });

                // Keep popup open on click
                marker.on('click', function () {
                    popupClicked = true;
                    marker.openPopup();
                });

                // Reset flag when popup is closed manually
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

// Function to search for a phone number
async function searchNumber() {
    const searchBox = document.getElementById('search-box');
    const phoneNumber = searchBox.value.trim();

    if (!phoneNumber) {
        alert('Please enter a phone number to search.');
        return;
    }

    const location = markersData.find(loc => loc.phone_number === phoneNumber);
    if (location) {
        const lat = parseFloat(location.lat);
        const long = parseFloat(location.long);

        map.setView([lat, long], 15);
        L.popup()
            .setLatLng([lat, long])
            .setContent(`
                <strong>Phone Number:</strong> ${location.phone_number}<br>
                <strong>Places:</strong> ${location.city}<br>
                <strong>Date & Time:</strong> ${location.tracked_at}
            `)
            .openOn(map);
    } else {
        alert('This number is not tracked. Please track it first.');
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

// Function to share the current map view
function shareLocation() {
    const searchBox = document.getElementById('search-box');
    const phoneNumber = searchBox.value.trim();
    if (phoneNumber) {
        const url = `${window.location.origin}/track-map?phone=${phoneNumber}`;
        navigator.clipboard.writeText(url).then(() => {
            alert('Link copied to clipboard!');
        });
    } else {
        alert('Please enter a phone number to share.');
    }
}

// Function to start directions from the user's current location
function startDirections() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            userLocation = [position.coords.latitude, position.coords.longitude];
            const searchBox = document.getElementById('search-box');
            const phoneNumber = searchBox.value.trim();
            const location = markersData.find(loc => loc.phone_number === phoneNumber);

            if (location) {
                const lat = parseFloat(location.lat);
                const long = parseFloat(location.long);

                L.Routing.control({
                    waypoints: [
                        L.latLng(userLocation),
                        L.latLng(lat, long)
                    ],
                    routeWhileDragging: false
                }).addTo(map);
            } else {
                alert('Please track this number first.');
            }
        });
    } else {
        alert('Geolocation is not supported by your browser.');
    }
}

// Calling the function to load data on page load
fetchTrackedLocations();
