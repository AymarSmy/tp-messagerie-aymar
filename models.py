from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    sender_id: int = Field(foreign_key="user.id")
    receiver_id: int = Field(foreign_key="user.id")

    subject: str
    body: str

    is_read: bool = Field(default=False)
    sent_at: datetime = Field(default_factory=datetime.utcnow)
