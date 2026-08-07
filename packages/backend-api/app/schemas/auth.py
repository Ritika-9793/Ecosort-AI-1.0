from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserRegisterSchema(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100, example="Rajesh Kumar")
    email: EmailStr = Field(..., example="rajesh@example.com")
    phone: Optional[str] = Field(None, example="+919876543210")
    password: str = Field(..., min_length=8, example="SecretP@ss123")
    role: str = Field(default="CITIZEN", example="CITIZEN")
    preferred_language: str = Field(default="en", example="en")


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(..., example="rajesh@example.com")
    password: str = Field(..., example="SecretP@ss123")


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
