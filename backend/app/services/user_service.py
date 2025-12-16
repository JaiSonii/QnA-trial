from sqlmodel import Session, select
from app.models.user import User, Role
from passlib.context import CryptContext
from app.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = self.session.exec(statement)
        return result.first()

    def create_user(self, user_data: UserCreate) -> User:
        hashed_password = pwd_context.hash(user_data.password)
        
        # Create User Object
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password,
            role= Role.ADMIN if user_data.email.endswith("@admin.com") else Role.GUEST
        )
        
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user

    def authenticate(self, email: str, password: str) -> User | None:
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not pwd_context.verify(password, user.password):
            return None
        return user