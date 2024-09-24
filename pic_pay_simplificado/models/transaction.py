from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Relationship
from database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transactions(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, index=True)
    sender_id = Column(Integer, ForeignKey('users.id', nullable=False))
    sender = Relationship("Users", foreign_keys=[sender_id], back_populates="sent_transactions")
    receiver_id = Column(Integer, ForeignKey('users.id', nullable=False))
    receiver = Relationship("Users", foreign_keys=[receiver_id], back_populates="received_transactions")