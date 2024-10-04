from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Users

def create_new_user(db: Session, first_name: str, last_name: str, document: int, email: str, password: str, balance: int, user_store: bool) -> Users:
    new_user = Users(first_name=first_name, last_name=last_name, document=document, email=email, password=password, balance=balance, user_store=user_store)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_document(db: Session, document: str) -> Users:
    return db.query(Users).filter(Users.document == document).first()

def get_all_users(db: Session):
    return db.query(Users).all()

def position_above_zero_validation(db: Session, id: int, amount: int):
    sender = db.query(Users).filter(Users.id == id).first()
    if sender.balance == 0:
        raise HTTPException(status_code=404, detail="This operation cannot be completed. Sender doesn't have enough money.")
    elif (amount - sender.balance) > 0:
        raise HTTPException(status_code=404, detail="This operation cannot be completed. Sender doesn't have enough money.")
    else:
        return sender
         
def validation_and_updating_positions(db: Session, sender_id: int, receiver_id, amount: int):
    sender = db.query(Users).filter(Users.id == sender_id).first()
    if sender.user_store == True:
        raise HTTPException(status_code=404, detail="Companies and other business are limited to receive money.")
    receiver = db.query(Users).filter(Users.id == receiver_id).first()
    sender.balance -= amount
    receiver.balance += amount

    