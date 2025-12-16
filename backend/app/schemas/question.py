from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional, List

class ReplyCreate(SQLModel):
    content: str

class ReplyResponse(SQLModel):
    id: int
    content: str
    created_at: datetime
    is_admin: bool

class QuestionCreate(SQLModel):
    content: str

class QuestionResponse(SQLModel):
    id: int
    content: str
    status: str
    created_at: datetime
    
    # RESTORED: Include AI Answer in response
    answer: Optional[str] = None 
    
    replies: List[ReplyResponse] = []