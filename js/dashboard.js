async function fetchDashboardData() {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    const network = document.getElementById('network-filter').value;

    let url = `http://127.0.0.1:5000/dashboard-data?`;
    if (startDate) url += `start_date=${startDate}&`;
    if (endDate) url += `end_date=${endDate}&`;
    if (network) url += `network=${network}&`;

    try {
        const response = await fetch(url);
        const data = await response.json();

        document.getElementById('total-reports').textContent = data.total_reports || 0;

        // Update Network Chart
        const networkChart = document.getElementById('network-chart').getContext('2d');
        new Chart(networkChart, {
            type: 'pie',
            data: {
                labels: Object.keys(data.network_counts),
                datasets: [{
                    data: Object.values(data.network_counts),
                    backgroundColor: ['red', 'orange', 'blue', 'gray']
                }]
            },
            options: { responsive: true }
        });

        // Update Places Chart
        const placesChart = document.getElementById('places-chart').getContext('2d');
        new Chart(placesChart, {
            type: 'bar',
            data: {
                labels: Object.keys(data.places_counts),
                datasets: [{
                    label: 'Reports by Places',
                    data: Object.values(data.places_counts),
                    backgroundColor: 'teal'
                }]
            },
            options: { responsive: true }
        });

    } catch (error) {
        console.error('Error fetching dashboard data:', error);
    }
}

// Fetch data on page load
fetchDashboardData();
