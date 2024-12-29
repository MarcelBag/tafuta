from flask import Blueprint, request, jsonify
import random

track_number_bp = Blueprint('track_number', __name__)

@track_number_bp.route('/track', methods=['POST'])
def track_number():
    try:
        data = request.json
        phone_number = data.get('phone_number')
        if not phone_number:
            return jsonify({"error": "Phone number is required"}), 400

        # Simulated triangulation logic
        dummy_locations = [
            {"latitude": random.uniform(-1.5, -1.0), "longitude": random.uniform(29.0, 29.5), "city": "Goma"},
            {"latitude": random.uniform(-1.0, -0.5), "longitude": random.uniform(29.5, 30.0), "city": "Bukavu"},
            {"latitude": random.uniform(-0.5, 0.0), "longitude": random.uniform(28.5, 29.0), "city": "Kisangani"}
        ]
        location = random.choice(dummy_locations)

        return jsonify({
            "status": "success",
            "phone_number": phone_number,
            "location": location
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
