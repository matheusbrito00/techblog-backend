from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.infra.config.database import get_db
from src.infra.providers import token_provider
from jose import JWTError
from src.infra.repositories.user import UserRepository

oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/login')

def get_logged_user(token: str = Depends(oauth2_schema), session: Session = Depends(get_db)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido')
    
    try:
        user_id = token_provider.verify_access_token(token)
        user = UserRepository(session).get_by_id(user_id)
    except JWTError:
        raise exception
    
    if not user_id or not user:
        raise exception
    
    return user