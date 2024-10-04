from sqlalchemy.orm import Session
from models import Transactions, Users
import requests

def create_transaction(db: Session, sender_id: int, receiver_id: int, amount: int) -> Transactions:
    new_transaction = Transactions(sender_id=sender_id, receiver_id=receiver_id, amount=amount)
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

def get_transactions_sent_by_user(db: Session, user_id: int) -> Transactions:
    return db.query(Transactions).filter(Transactions.sender_id == user_id).all()

def get_transactions_received_by_user(db: Session, user_id: int) -> Transactions:
    return db.query(Transactions).filter(Transactions.receiver_id == user_id).all()
    
def get_all_transactions(db: Session, user_id: int) -> Transactions:
    return db.query(Transactions).all()

def authorization_service():
    response = requests.get('https://util.devi.tools/api/v2/authorize')
    data = response.json()
    return data