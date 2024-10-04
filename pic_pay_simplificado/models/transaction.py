from sqlalchemy import Boolean, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from models.user import Users

Base = declarative_base()

class Transactions(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, index=True)
    sender_id = Column(Integer, ForeignKey(Users.id))
    sender = relationship(Users, foreign_keys=[sender_id])
    receiver_id = Column(Integer, ForeignKey(Users.id))
    receiver = relationship(Users, foreign_keys=[receiver_id])


