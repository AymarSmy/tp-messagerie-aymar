from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    sender_id: int
    receiver_id: int
    subject: str
    body: str


class MessageRead(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    sender_name: str
    receiver_name: str
    subject: str
    body: str
    is_read: bool
    sent_at: datetime
