from sqlmodel import SQLModel

class Token(SQLModel):
    access_token: str
    token_type: str

class UserCreate(SQLModel):
    username: str
    email: str
    password: str