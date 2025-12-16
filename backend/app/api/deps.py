from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session
from typing import Optional

from app.core.config import settings
from app.core.database import db
from app.models.user import User
from app.services.user_service import UserService
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.requests import Request

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_session():
    with Session(db.engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]

def get_current_user(session: SessionDep, token: TokenDep) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user_service = UserService(session)
    user = user_service.get_user_by_email(email)
    
    if user is None:
        raise credentials_exception
        
    return user

def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency that ensures the user is specifically an Admin.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="The user doesn't have enough privileges"
        )
    return current_user

async def get_current_user_optional(session: SessionDep, request: Request) -> Optional[User]:
    authorization = request.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)
    
    if scheme.lower() != "bearer" or not param:
        return None
    
    try:
        payload = jwt.decode(param, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
    except (JWTError, Exception):
        return None
    
    user_service = UserService(session)
    return user_service.get_user_by_email(email)