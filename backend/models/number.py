from sqlalchemy import Column, Integer, String
from .database import Base

class Number(Base):
    __tablename__ = "numbers"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    last_location = Column(String, nullable=True)
    reports = Column(Integer, default=0)
