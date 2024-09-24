from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Relationship
from database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    document = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, index=True)
    balance = Column(Integer, index=True)
    user_type = Column(String, index=True)
    
    sent_transactions = Relationship("Transaction", foreign_keys="[Transaction.sender_id]", back_populates="sender")
    received_transactions = Relationship("Transaction", foreign_keys="[Transaction.receiver_id]", back_populates="receiver")