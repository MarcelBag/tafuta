from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # Removed extend_existing
    username = Column(String, unique=True, nullable=False)  # Removed extend_existing
    password = Column(String, nullable=False)  # Removed extend_existing
