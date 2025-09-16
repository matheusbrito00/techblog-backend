from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

# CONFIG
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRES_IN_MIN = int(os.getenv("EXPIRES_IN_MIN"))

def create_access_token(data: dict, duration: timedelta = timedelta(minutes=EXPIRES_IN_MIN)):
    data_aux = data.copy()
    expire = datetime.utcnow() + duration
    
    data_aux.update({'exp': expire})
    token_jwt = jwt.encode(data_aux, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

def verify_access_token(token: str):
    data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return int(data.get('sub'))