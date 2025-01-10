# /backend/routes/export.py
from flask import Blueprint, jsonify, request, Response
import csv
from io import StringIO
from models.database import SessionLocal
from models.number import Number
from models.database import TrackingLog

export_bp = Blueprint('export', __name__)
db = SessionLocal()

@export_bp.route('/export/csv', methods=['GET'])
def export_csv():
    """Export reported numbers and tracking data as CSV."""
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Phone Number', 'Reports', 'Last Location', 'Places', 'Reported At'])

    # Query the reported numbers
    numbers = db.query(Number).all()
    for num in numbers:
        writer.writerow([
            num.phone_number,
            num.reports,
            num.last_location or "Unknown",
            num.places or "Unknown",
            num.reported_at.strftime('%Y-%m-%d %H:%M:%S') if num.reported_at else "Unknown"
        ])

    output.seek(0)
    return Response(output, mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=reported_numbers.csv"})
