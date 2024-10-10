import pytest
from fastapi.testclient import TestClient
from pic_pay_simplificado.main import app
from pic_pay_simplificado import models
from pic_pay_simplificado.utils import SessionLocal


client = TestClient(app)

def delete_from_test():
    db = SessionLocal()
    obj = db.query(models.Users).where(models.Users.document == '77777777777').first()
    if obj is not None:
        db.delete(obj)
        db.commit()

def test_create_user():
    delete_from_test()
    response = client.post("/users/", json={"first_name": "Arthur", "last_name": "Pereira", "document": "77777777777", "email": "teste@hotmail.com", "password": "123456", "balance": 10, "user_store": False})
    assert response.status_code == 200
    assert response.json()["first_name"] == "Arthur"
    
def test_create_transaction():
    response = client.post("/transactions/", json={"sender_id": "13", "receiver_id": "14", "amount": 1})
    assert response.status_code == 200