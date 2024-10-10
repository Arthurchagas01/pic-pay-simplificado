from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from utils import SessionLocal
import models
from core import transactions_services, user_services, notification_service

router = APIRouter()

class Transactions_BaseModel(BaseModel):
    amount : int
    sender_id : int
    receiver_id : int
    
    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=None)
def create_transaction(transaction: Transactions_BaseModel, db: Session = Depends(get_db)):
    try:
        sender = db.query(models.Users).get(transaction.sender_id)
        receiver = db.query(models.Users).get(transaction.receiver_id)
        if not sender or not receiver:
            raise HTTPException(status_code=404, detail="Sender or Receiver not found")
        
        user_services.position_above_zero_validation(db, transaction.sender_id, transaction.amount)
        user_services.validation_and_updating_positions(db, transaction.sender_id, transaction.receiver_id, transaction.amount)
        
        result = transactions_services.authorization_service()
        authorization = result.get("data", {}).get("authorization")
        if authorization == False:
            notification_service.send_notification(False, transaction.sender_id, transaction.receiver_id, 3)
            raise HTTPException(status_code=404, detail="Not authorized")
        
        notification_service.send_notification(True, transaction.sender_id, transaction.receiver_id, 3)
        return transactions_services.create_transaction(db, transaction.sender_id, transaction.receiver_id, transaction.amount)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sent/{user_id}", response_model=None)
def get_transactions_sent(user_id: int, db: Session = Depends(get_db)):
    return transactions_services.get_transactions_sent_by_user(db, user_id)

@router.get("/received/{user_id}", response_model=None)
def get_transactions_received(user_id: int, db: Session = Depends(get_db)):
    return transactions_services.get_transactions_received_by_user(db, user_id)