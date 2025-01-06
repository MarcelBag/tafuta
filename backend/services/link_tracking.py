# /services/link_tracking.py
from flask import request

def capture_metadata(unique_id):
    """Capture metadata when a tracking link is opened."""
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    # Optionally, request geolocation from the frontend

    # Log the metadata in the database (omitted here)
    return {"ip_address": ip_address, "user_agent": user_agent}
