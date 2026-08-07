from fastapi import APIRouter, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import get_db
from app.schemas.auth import UserRegisterSchema, UserLoginSchema
from app.schemas.common import ResponseSchema
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=ResponseSchema[dict])
async def register(payload: UserRegisterSchema, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Register a new user account (Citizen, BWG, Vendor, Municipality)."""
    service = AuthService(db)
    result = await service.register_user(payload)
    return ResponseSchema(
        success=True,
        message="User registered successfully",
        data=result
    )


@router.post("/login", status_code=status.HTTP_200_OK, response_model=ResponseSchema[dict])
async def login(payload: UserLoginSchema, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Authenticate user credentials and receive JWT access/refresh tokens."""
    service = AuthService(db)
    result = await service.authenticate_user(payload)
    return ResponseSchema(
        success=True,
        message="Authentication successful",
        data=result
    )
