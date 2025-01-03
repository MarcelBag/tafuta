from sqlalchemy import Column, Integer, String
from flask_login import UserMixin
from .database import Base

class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)       # New field
    surname = Column(String, nullable=False)    # New field
    company = Column(String, nullable=False)    # New field
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
