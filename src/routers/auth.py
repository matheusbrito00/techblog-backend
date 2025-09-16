from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from src.schemas.schemas import UserBase, LoginSuccess, UserSignIn
from src.infra.config.database import get_db
from src.infra.repositories.user import UserRepository
from src.infra.providers import hash_provider, token_provider
from src.routers.utils import get_logged_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserBase)
async def signup(user: UserBase, session: Session = Depends(get_db)):
    user_aux = UserRepository(session).get_by_mail(user.mail)
    
    if user_aux:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email already registered")
    
    user.password = hash_provider.generate_hash(user.password)
    created_user = UserRepository(session).create(user)
    return created_user

@router.post("/signin", response_model=LoginSuccess)
async def signin(login_data: UserSignIn, session: Session = Depends(get_db)):
    mail = login_data.mail
    password = login_data.password
    user = UserRepository(session).get_by_mail(mail)
    password_valid = hash_provider.verify_hash(password, user.password)
    
    if not user or not password_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect email or password')
    
    token = token_provider.create_access_token({ 'sub': str(user.id) })
    refresh_token = token_provider.create_access_token({ 'sub': user.id }, timedelta(days=7))
    return LoginSuccess(user=user, access_token=token, refresh_token=refresh_token)

@router.post("/login", response_model=LoginSuccess)
async def login(login_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    mail = login_data.username
    password = login_data.password
    user = UserRepository(session).get_by_mail(mail)
    password_valid = hash_provider.verify_hash(password, user.password)
    
    if not user or not password_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect email or password')
    
    token = token_provider.create_access_token({ 'sub': str(user.id) })
    return LoginSuccess(user=user, access_token=token)

@router.get("/refresh", response_model=LoginSuccess)
async def refresh_token(user: UserBase = Depends(get_logged_user)):
    token = token_provider.create_access_token({ 'sub': user.id })
    
    return LoginSuccess(user=user, access_token=token)

@router.get("/me", response_model=UserBase)
async def me(user: UserBase = Depends(get_logged_user)):
    return user

@router.put("/users/{user_id}", status_code=status.HTTP_201_CREATED, response_model=UserBase)
async def update(user_id:int, user: UserBase = Depends(get_logged_user), session: Session = Depends(get_db)):
    user_aux = UserRepository(session).get_by_id(user_id)
    
    if not user_aux:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user_aux.id != user.id or not user.isAdmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    UserRepository(session).update(user_id, user)
    return user

@router.delete("/users/{user_id}")
async def delete(user_id: int, user: UserBase = Depends(get_logged_user), session: Session = Depends(get_db)):
    user_aux = UserRepository(session).get_by_id(user_id)
    
    if not user_aux:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user_aux.id != user.id or not user.isAdmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    UserRepository(session).delete(user_id)
    return { "message": "User deleted successfully" }