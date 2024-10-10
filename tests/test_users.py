import pytest
from pic_pay_simplificado import models
from pic_pay_simplificado.utils import SessionLocal


def delete_from_test():
    db = SessionLocal()
    obj = db.query(models.Users).where(models.Users.document == '66666666666').first()
    if obj is not None:
        db.delete(obj)
        db.commit()

def test_create_user():
    delete_from_test()
    db = SessionLocal()    
    new_user = models.Users(first_name="Pupie", last_name="Chagas", document="66666666666", email="test3@gmail.com", password="123456", balance=57, user_store=False)
    db.add(new_user)
    db.commit()
    
    created_user = db.query(models.Users).filter(models.Users.document == "66666666666").first()
    
    assert created_user is not None
    assert created_user.first_name == "Pupie"
    assert created_user.balance == 57
    assert created_user.user_store == False
    db.close()