from flask import Blueprint, request, jsonify
from models.database import SessionLocal, TrackingLog
from datetime import datetime
from models.number import Number
import random

track_number_bp = Blueprint('track_number', __name__)

@track_number_bp.route('/track', methods=['POST'])
def track_number():
    db = SessionLocal()
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

        # Log the tracking request in the TrackingLog table
        tracking_log = TrackingLog(
            phone_number=phone_number,
            latitude=location['latitude'],
            longitude=location['longitude'],
            city=location['city']
        )
        db.add(tracking_log)

        # Sync the data with the reports table
        report = db.query(Number).filter_by(phone_number=phone_number).first()
        if not report:
            report = Number(
                phone_number=phone_number,
                last_location=f"Lat: {location['latitude']}, Long: {location['longitude']}",
                reports=1, 
                reported_at=datetime.utcnow()
            )
            db.add(report)
        else:
            report.last_location = f"Lat: {location['latitude']}, Long: {location['longitude']}"
            report.reports += 1
            report.reported_at = datetime.utcnow()

        db.commit()

        return jsonify({
            "status": "success",
            "phone_number": phone_number,
            "location": location
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
