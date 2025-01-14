async function fetchReports(network = '') {
    try {
        const response = await fetch(`/api/report?network=${network}`);
        const data = await response.json();

        const tableBody = document.getElementById('report-table-body');
        tableBody.innerHTML = '';

        // Handle filter visibility
        const filters = document.getElementById('network-filters').querySelectorAll('.list-group-item');
        filters.forEach((filter) => {
            if (network && filter.textContent !== network) {
                // Hide filters that don't match the selected network
                filter.style.display = 'none'; 
            } else {
                // Show filters
                filter.style.display = 'block'; 
            }
        });

        // Populating table with reports
        data.data.forEach((item) => {
            const row = document.createElement('tr');
            let bgColor = '';

            // Apply background color based on network
            if (item.network === 'Orange') {
                bgColor = 'orange';
            } else if (item.network === 'Airtel') {
                bgColor = 'red';
            } else if (item.network === 'Vodacom') {
                bgColor = 'blue';
            }

            row.innerHTML = `
                <td>${item.phone_number}</td>
                <td>${item.reports}</td>
                <td>${item.reported_at || 'Unknown'}</td>
                <td>${item.last_location || 'Unknown'}</td>
                <td>${item.places || 'Unknown'}</td>
                <td style="background-color: ${bgColor}; color: white;">${item.network}</td>
            `;
            tableBody.appendChild(row);
        });

        // Add "Reset Filters" button
        const resetButton = document.getElementById('reset-filters');
        if (network) {
            resetButton.style.display = 'block'; // Show reset button
        } else {
            resetButton.style.display = 'none'; // Hide reset button
        }
    } catch (error) {
        console.error('Error fetching reports:', error);
    }
}

function filterNetwork(network) {
    fetchReports(network);
}

function resetFilters() {
    // Fetch all reports
    fetchReports(); 
    const filters = document.getElementById('network-filters').querySelectorAll('.list-group-item');
    filters.forEach((filter) => (filter.style.display = 'block')); // Show all filters
}

// Fetch all reports on page load
fetchReports();
