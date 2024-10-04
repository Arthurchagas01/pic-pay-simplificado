from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils import engine, SessionLocal
from pydantic import BaseModel
import models
from core import user_services
from typing import Annotated, List

router = APIRouter()

class Users_BaseModel(BaseModel):
    first_name : str
    last_name : str
    document : str
    email : str
    password : str
    balance : int
    user_store : bool
    
    class Config:
        orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@router.post("/", response_model=None)
def create_new_user(users : Users_BaseModel, db: Session = Depends(get_db)):
    db_user = user_services.get_user_by_document(db, users.document)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return user_services.create_new_user(db, users.first_name, users.last_name, users.document, users.email, users.password, users.balance, users.user_store)

@router.get("/", response_model=None)
def get_all_users(db: Session = Depends(get_db)):
    return user_services.get_all_users(db)