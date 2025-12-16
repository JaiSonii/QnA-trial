from sqlmodel import Session, select
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import get_password_hash, verify_password

class AuthService:
    def __init__(self, session: Session):
        self.session = session

    def register_user(self, user_data: UserCreate):
        hashed_pw = get_password_hash(user_data.password)
        role = "admin" if "admin" in user_data.email else "guest"
        user = User(username=user_data.username, email=user_data.email, password=hashed_pw, role=role) #type: ignore
        self.session.add(user)
        self.session.commit()
        return user

    def authenticate_user(self, email: str, password: str):
        statement = select(User).where(User.email == email)
        user = self.session.exec(statement).first()
        if not user or not verify_password(password, user.password):
            return None
        return user