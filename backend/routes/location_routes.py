from flask import Blueprint, request, jsonify
from services.internet_location import store_location
from services.sms_service import generate_tracking_link, send_sms
from services.link_tracking import capture_metadata

location_bp = Blueprint('location', __name__)

@location_bp.route('/api/store-location', methods=['POST'])
def api_store_location():
    """Receive geolocation data from the frontend and store it."""
    data = request.json
    phone_number = data.get('phone_number')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if not (phone_number and latitude and longitude):
        return jsonify({"error": "Missing required fields"}), 400

    result = store_location(phone_number, latitude, longitude)
    return jsonify(result)

@location_bp.route('/api/send-tracking-link', methods=['POST'])
def api_send_tracking_link():
    """Generate and send a tracking link via SMS."""
    data = request.json
    phone_number = data.get('phone_number')

    if not phone_number:
        return jsonify({"error": "Phone number is required"}), 400

    tracking_link = generate_tracking_link(phone_number)
    message = f"Please click this link to verify your location: {tracking_link}"
    result = send_sms(phone_number, message)
    return jsonify(result)

@location_bp.route('/track-link/<unique_id>', methods=['GET'])
def track_link(unique_id):
    """Handle opened tracking link and capture metadata."""
    metadata = capture_metadata(unique_id)
    return jsonify({"status": "success", "metadata": metadata})
