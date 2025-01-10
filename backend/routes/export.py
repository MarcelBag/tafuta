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
