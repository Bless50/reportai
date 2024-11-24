#import neccessary types and functions from SQLALchemy
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func # for automatic timestamp


# import base class from base.py
from .base import Base

#define user model model that inherits from Base
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    full_name = Column(String)
    department = Column(String)
    level = Column(String)
    institution = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

# optional: Add string representation of user object 
    def __repr__(self):
        return f"<User {self.email}>"
     