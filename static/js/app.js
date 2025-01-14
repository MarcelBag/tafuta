console.log('app.js is loaded successfully');

// Form submissiong handling
document.getElementById('track-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const phoneNumber = document.getElementById('phone-number').value;

    try {
        const response = await fetch('http://127.0.0.1:5000/track', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ phone_number: phoneNumber }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        // Debugging log for response
        console.log('Response data:', data); 
        const { phone_number, location } = data;
        // Debuging log for location
        console.log('Extracted location:', location); 


        document.getElementById('result').innerHTML = `
            <div class="alert alert-success">
                Tracking initiated for ${phone_number}.<br>
                Location: ${location.city} (Lat: ${location.latitude.toFixed(3)}, Long: ${location.longitude.toFixed(3)}).
            </div>
        `;
    } catch (error) {
        document.getElementById('result').innerHTML = `
            <div class="alert alert-danger">Error: ${error.message}</div>
        `;
        console.error('Tracking Error:', error);
    }
});

// Handling report submission
document.getElementById('report-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const phoneNumber = document.getElementById('report-phone-number').value;

    try {
        const response = await fetch('http://127.0.0.1:5000/report', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ phone_number: phoneNumber }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        document.getElementById('report-result').innerHTML = `
            <div class="alert alert-success">
                Number ${data.phone_number} reported successfully! Total reports: ${data.reports}.
            </div>
        `;

        document.getElementById('reported-numbers').classList.remove('d-none');
        fetchReportedNumbers();
    } catch (error) {
        document.getElementById('report-result').innerHTML = `
            <div class="alert alert-danger">Error: ${error.message}</div>
        `;
        console.error('Reporting Error:', error);
    }
});

// Fetch Reported Numbers
async function fetchReportedNumbers() {
    try {
        const response = await fetch('http://127.0.0.1:5000/report');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        const numberList = document.getElementById('number-list');
        numberList.innerHTML = '';

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


// all fetch numbers on page load
fetchReportedNumbers();
