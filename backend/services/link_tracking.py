# /backend/services/link_tracking.py
from flask import request
from models.database import SessionLocal, TrackingMetadata
from datetime import datetime

def capture_metadata(unique_id):
    """Capture metadata when a tracking link is opened."""
    db = SessionLocal()
    try:
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        timestamp = datetime.utcnow()

        # Log metadata in the database
        metadata = TrackingMetadata(
            unique_id=unique_id,
            ip_address=ip_address,
            user_agent=user_agent,
            captured_at=timestamp
        )
        db.add(metadata)
        db.commit()

        return {"status": "success", "metadata": {
            "ip_address": ip_address,
            "user_agent": user_agent,
            "timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
