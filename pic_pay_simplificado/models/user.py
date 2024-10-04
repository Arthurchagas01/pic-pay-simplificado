from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    document = Column(String, unique=True,  index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, index=True)
    balance = Column(Integer, index=True)
    user_store = Column(Boolean, index=True)