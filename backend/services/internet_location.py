# /services/internet_location.py

def store_location(phone_number, latitude, longitude):
    """Store the location data in the database."""
    from models.database import SessionLocal, TrackingLog
    from datetime import datetime

    db = SessionLocal()
    try:
        log = TrackingLog(
            phone_number=phone_number,
            latitude=latitude,
            longitude=longitude,
            tracked_at=datetime.utcnow()
        )
        db.add(log)
        db.commit()
        return {"status": "success", "message": "Location stored successfully"}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
