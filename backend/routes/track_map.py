from flask import Blueprint, jsonify, render_template
from models.database import SessionLocal
from models.number import Number

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
        numbers = db.query(Number).all()
        data = []
        for number in numbers:
            if number.last_location:  # Ensure there's a location to show
                lat, long = map(float, number.last_location.replace('Lat: ', '').replace('Long: ', '').split(','))
                data.append({
                    "phone_number": number.phone_number,
                    "reports": number.reports,
                    "places": number.places or "Unknown",
                    "lat": lat,
                    "long": long,
                    "reported_at": number.reported_at.strftime('%Y-%m-%d %H:%M:%S') if number.reported_at else "Unknown"
                })
        return jsonify({"data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
