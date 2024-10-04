from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Transactions, Users
import requests
import time

def send_notification_of_transaction_payload(status: bool, sender_id: str, receiver_id: str):
    return {
        "status": status,
        "message": "Money transfered from "+ str(sender_id) + " to " + str(receiver_id)
    }
    
def send_notification(status: bool, sender_id: str, receiver_id: str, retries: int=3):
    payload = send_notification_of_transaction_payload(status, sender_id, receiver_id)
    
    for attempt in range(retries):
        try: 
            response = requests.post('https://util.devi.tools/api/v1/notify', json=payload)
            
            # if response.status_code == 200:
            #     return True
            # else:
            #     raise HTTPException(status_code=404, detail="Not authorized")
        except requests.exceptions.RequestException as e:
           raise HTTPException(status_code=404, detail=str(e))
        
        time.sleep(2)
       
    return False