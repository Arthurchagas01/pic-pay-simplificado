from fastapi import FastAPI
from api import users_api, transaction_api
from utils import engine, SessionLocal
import models

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
app.include_router(users_api.router, prefix="/users", tags=["users"])
app.include_router(transaction_api.router, prefix="/transactions", tags=["transactions"])




