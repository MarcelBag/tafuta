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
