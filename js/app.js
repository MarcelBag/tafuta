document.getElementById('track-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const phoneNumber = document.getElementById('phone-number').value;

    try {
        const response = await fetch('http://127.0.0.1:5000/track', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ phone_number: phoneNumber }),
        });
        const data = await response.json();
        document.getElementById('result').innerHTML = `
            <div class="alert alert-success">Tracking initiated for ${data.phone_number}</div>
        `;
    } catch (error) {
        document.getElementById('result').innerHTML = `
            <div class="alert alert-danger">Error: ${error.message}</div>
        `;
    }
});

// Handle Report Form Submission
document.getElementById('report-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const phoneNumber = document.getElementById('phone-number').value;

    try {
        const response = await fetch('/report', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ phone_number: phoneNumber }),
        });
        const data = await response.json();
        document.getElementById('report-result').innerHTML = `
            <div class="alert alert-success">
                Number ${data.phone_number} reported successfully! Total reports: ${data.reports}.
            </div>
        `;
        fetchReportedNumbers();
    } catch (error) {
        document.getElementById('report-result').innerHTML = `
            <div class="alert alert-danger">Error: ${error.message}</div>
        `;
    }
});

// Fetch Reported Numbers
async function fetchReportedNumbers() {
    try {
        const response = await fetch('/report');
        const data = await response.json();

        const numberList = document.getElementById('number-list');
        numberList.innerHTML = ''; // Clear existing list
        data.forEach((item) => {
            const listItem = document.createElement('li');
            listItem.className = 'list-group-item';
            listItem.textContent = `Number: ${item.phone_number}, Reports: ${item.reports}`;
            numberList.appendChild(listItem);
        });
    } catch (error) {
        console.error('Error fetching reported numbers:', error);
    }
}

// Fetch numbers on page load
fetchReportedNumbers();


