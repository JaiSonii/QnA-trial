from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    GUEST = "guest"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str = Field(unique=True, index=True)
    password: str
    role: Role = Field(default=Role.GUEST)