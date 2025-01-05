from flask import Blueprint, jsonify, render_template
from models.database import SessionLocal
from models.database import TrackingLog

track_map_bp = Blueprint('track_map', __name__)
db = SessionLocal()

@track_map_bp.route('/track-map')
def track_map():
    """Render the map-based tracking page."""
    return render_template('track_map.html')

@track_map_bp.route('/api/tracked-locations', methods=['GET'])
def get_tracked_locations():
    """API endpoint to provide tracked locations for visualization on the map."""
    try:
        logs = db.query(TrackingLog).all()
        data = [
            {
                "phone_number": log.phone_number,
                "lat": log.latitude,
                "long": log.longitude,
                "city": log.city or "Unknown",
                "tracked_at": log.tracked_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            for log in logs
        ]
        return jsonify({"data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
