from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from datetime import timedelta

from app.core.database import db
from app.core.security import create_access_token 
from app.schemas.user import UserCreate, Token
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_user_service(session: Session = Depends(db.get_session)):
    return UserService(session)

@router.post("/register", response_model=dict)
def register(user_data: UserCreate, service: UserService = Depends(get_user_service)):
    existing_user = service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    service.create_user(user_data)
    return {"message": "User registered successfully"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), service: UserService = Depends(get_user_service)):
    user = service.authenticate(email=form_data.username, password=form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}