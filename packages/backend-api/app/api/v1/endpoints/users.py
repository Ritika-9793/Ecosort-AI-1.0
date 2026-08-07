from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import get_db
from app.core.security import oauth2_scheme, decode_token
from app.schemas.user import UserResponseSchema, UserUpdateSchema
from app.schemas.common import ResponseSchema
from app.services.user_service import UserService

router = APIRouter()


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """Dependency injecting current authenticated user's ID from JWT token."""
    payload = decode_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    return str(user_id)


@router.get("/me", response_model=ResponseSchema[dict])
async def get_current_user_profile(
    user_id: str = Depends(get_current_user_id),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Retrieve profile details of currently logged-in user."""
    service = UserService(db)
    profile = await service.get_user_profile(user_id)
    return ResponseSchema(success=True, data=profile)


@router.patch("/me", response_model=ResponseSchema[dict])
async def update_current_user_profile(
    payload: UserUpdateSchema,
    user_id: str = Depends(get_current_user_id),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Update profile details of currently logged-in user."""
    service = UserService(db)
    updated_profile = await service.update_user_profile(user_id, payload)
    return ResponseSchema(
        success=True,
        message="Profile updated successfully",
        data=updated_profile
    )
