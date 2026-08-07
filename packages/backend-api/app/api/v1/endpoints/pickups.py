from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.core.database import get_db
from app.api.v1.endpoints.users import get_current_user_id
from app.schemas.common import ResponseSchema

router = APIRouter()


class SchedulePickupSchema(BaseModel):
    vendor_id: Optional[str] = None
    waste_categories: List[str]
    estimated_weight_kg: float
    pickup_date: str
    pickup_address: str


@router.post("/schedule", status_code=status.HTTP_201_CREATED, response_model=ResponseSchema[dict])
async def schedule_doorstep_pickup(
    payload: SchedulePickupSchema,
    user_id: str = Depends(get_current_user_id),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Schedule a doorstep scrap pickup with local Kabadiwala/recycling partner."""
    doc = {
        "citizen_id": ObjectId(user_id),
        "vendor_id": ObjectId(payload.vendor_id) if payload.vendor_id and ObjectId.is_valid(payload.vendor_id) else None,
        "waste_categories": payload.waste_categories,
        "estimated_weight_kg": payload.estimated_weight_kg,
        "pickup_date": payload.pickup_date,
        "pickup_address": payload.pickup_address,
        "status": "SCHEDULED",
        "created_at": datetime.now(timezone.utc)
    }

    res = await db["doorstep_pickups"].insert_one(doc)
    return ResponseSchema(
        success=True,
        message="Doorstep pickup scheduled successfully",
        data={"pickup_id": str(res.inserted_id), "status": "SCHEDULED"}
    )


@router.get("/my-pickups", response_model=ResponseSchema[dict])
async def get_my_pickups(
    user_id: str = Depends(get_current_user_id),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get citizen scheduled pickup requests."""
    cursor = db["doorstep_pickups"].find({"citizen_id": ObjectId(user_id)}).sort("created_at", -1)
    pickups = []
    async for doc in cursor:
        pickups.append({
            "id": str(doc["_id"]),
            "waste_categories": doc.get("waste_categories", []),
            "estimated_weight_kg": doc.get("estimated_weight_kg"),
            "pickup_date": doc.get("pickup_date"),
            "pickup_address": doc.get("pickup_address"),
            "status": doc.get("status"),
            "created_at": doc.get("created_at").isoformat() if isinstance(doc.get("created_at"), datetime) else str(doc.get("created_at"))
        })
    return ResponseSchema(success=True, data={"pickups": pickups})
