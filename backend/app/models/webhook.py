from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class Webhook(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))