from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///tafuta.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Existing tables...

# New table for tracking logs
class TrackingLog(Base):
    __tablename__ = "tracking_logs"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    city = Column(String)
    tracked_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)