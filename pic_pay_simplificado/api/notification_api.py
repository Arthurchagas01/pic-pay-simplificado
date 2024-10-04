from fastapi import APIRouter, FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from utils import engine, SessionLocal
import models
from core import transactions_services, user_services
from models import Transactions, Users
from typing import Annotated, List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
