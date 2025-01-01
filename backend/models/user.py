from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, extend_existing=True)
    username = Column(String, unique=True, nullable=False, extend_existing=True)
    password = Column(String, nullable=False, extend_existing=True)
