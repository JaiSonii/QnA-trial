from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from enum import Enum
from app.models.user import User 

class QuestionStatus(str, Enum):
    PENDING = "Pending"
    ESCALATED = "Escalated"
    ANSWERED = "Answered"

class Reply(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question_id: int = Field(foreign_key="question.id")
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)) 
    is_admin: bool = Field(default=False)
    
    question: "Question" = Relationship(back_populates="replies")

class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    status: QuestionStatus = Field(default=QuestionStatus.PENDING)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    answer: Optional[str] = None 
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship()

    replies: List[Reply] = Relationship(back_populates="question")