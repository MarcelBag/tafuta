# /backend/routes/location_routes.py
import uuid
from flask import Blueprint, request, jsonify
from services.internet_location import store_location
from services.link_tracking import capture_metadata

location_bp = Blueprint('location', __name__)

def generate_tracking_link(phone_number):
    """Generate a unique tracking link."""
    unique_id = str(uuid.uuid4())  # Generate a unique ID
    tracking_link = f"http://yourdomain.com/track-link/{unique_id}"
    # Optionally, store the link in a database if needed
    return tracking_link

@location_bp.route('/api/send-tracking-link', methods=['POST'])
def api_send_tracking_link():
    """Generate and send a tracking link via SMS."""
    data = request.json
    phone_number = data.get('phone_number')

    if not phone_number:
        return jsonify({"error": "Phone number is required"}), 400

    tracking_link = generate_tracking_link(phone_number)
    message = f"Please click this link to verify your location: {tracking_link}"
    
    # Example: Send SMS function (you should replace this with your real SMS service)
    result = send_sms(phone_number, message)
    return jsonify(result)

@location_bp.route('/track-link/<unique_id>', methods=['GET'])
def track_link(unique_id):
    """Handle opened tracking link and capture metadata."""
    metadata = capture_metadata(unique_id)
    return jsonify(metadata)
