import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone

# Set the absolute path to the database file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get the directory of this file
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'tafuta.db')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# TrackingLog table definition
class TrackingLog(Base):
    __tablename__ = "tracking_logs"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    city = Column(String)
    tracked_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Timezone-aware datetime

# Initialize database tables
Base.metadata.create_all(bind=engine)
