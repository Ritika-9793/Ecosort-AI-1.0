from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserResponseSchema(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str
    preferred_language: str
    rewards_balance: int
    is_active: bool
    created_at: datetime


class UserUpdateSchema(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    preferred_language: Optional[str] = None
