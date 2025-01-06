# /services/sms_service.py

import uuid
from twilio.rest import Client

TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'

def generate_tracking_link(phone_number):
    """Generate a unique tracking link for the given phone number."""
    unique_id = str(uuid.uuid4())
    tracking_link = f"http://your-domain.com/track-link/{unique_id}"
    # Store the link and phone number association in the database (omitted here)
    return tracking_link

def send_sms(phone_number, message):
    """Send an SMS using Twilio."""
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        return {"status": "success", "sid": message.sid}
    except Exception as e:
        return {"status": "error", "message": str(e)}
