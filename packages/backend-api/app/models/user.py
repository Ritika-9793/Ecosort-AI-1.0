from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr


class GeoLocation(BaseModel):
    type: str = "Point"
    coordinates: List[float] = [77.2090, 28.6139]  # [lng, lat]


class UserModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    hashed_password: str
    role: str = "CITIZEN"  # CITIZEN, BWG, VENDOR, MUNICIPALITY, ADMIN
    preferred_language: str = "en"
    rewards_balance: int = 0
    location: Optional[GeoLocation] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
