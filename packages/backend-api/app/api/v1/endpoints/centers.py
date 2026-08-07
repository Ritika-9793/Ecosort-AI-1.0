from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import get_db
from app.api.v1.endpoints.users import get_current_user_id
from app.schemas.common import ResponseSchema

router = APIRouter()

# Seed baseline recycling centers if collection empty
INITIAL_CENTERS = [
    {
        "name": "Green India Scrap Recycling Hub",
        "type": "KABADIWALA_PARTNER",
        "contact_phone": "+911123456789",
        "address": "Sector 18, Industrial Area, Noida",
        "city": "Noida",
        "location": {"type": "Point", "coordinates": [77.3260, 28.5700]},
        "accepted_categories": ["DRY_RECYCLABLE", "E_WASTE"],
        "qr_code_data": "ECOSORT_CENTER_NOIDA_101",
        "is_verified": True
    },
    {
        "name": "Delhi E-Waste Collection Kiosk",
        "type": "E_WASTE_KIOSK",
        "contact_phone": "+911198765432",
        "address": "Connaught Place, New Delhi",
        "city": "New Delhi",
        "location": {"type": "Point", "coordinates": [77.2167, 28.6328]},
        "accepted_categories": ["HAZARDOUS", "E_WASTE"],
        "qr_code_data": "ECOSORT_CENTER_DELHI_202",
        "is_verified": True
    }
]


@router.get("/nearby", response_model=ResponseSchema[dict])
async def get_nearby_recycling_centers(
    lat: float = Query(28.6139, example=28.6139),
    lng: float = Query(77.2090, example=77.2090),
    radius_km: float = Query(10.0, example=10.0),
    user_id: str = Depends(get_current_user_id),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Locate nearby recycling centers using MongoDB 2dsphere spatial index.
    """
    collection = db["recycling_centers"]
    
    # Auto-seed if empty
    if await collection.count_documents({}) == 0:
        await collection.insert_many(INITIAL_CENTERS)

    # Perform 2dsphere spatial query
    max_distance_meters = radius_km * 1000.0
    query = {
        "location": {
            "$near": {
                "$geometry": {"type": "Point", "coordinates": [lng, lat]},
                "$maxDistance": max_distance_meters
            }
        }
    }

    cursor = collection.find(query)
    centers = []
    async for doc in cursor:
        centers.append({
            "id": str(doc["_id"]),
            "name": doc.get("name"),
            "type": doc.get("type"),
            "contact_phone": doc.get("contact_phone"),
            "address": doc.get("address"),
            "city": doc.get("city"),
            "coordinates": {
                "lat": doc["location"]["coordinates"][1],
                "lng": doc["location"]["coordinates"][0]
            },
            "accepted_categories": doc.get("accepted_categories", []),
            "qr_code_data": doc.get("qr_code_data"),
            "is_verified": doc.get("is_verified", True)
        })

    return ResponseSchema(success=True, data={"total": len(centers), "centers": centers})


@router.get("/{center_id}/qr", response_model=ResponseSchema[dict])
async def get_center_qr_code(
    center_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Generate QR Code data payload for recycling center drop-off verification."""
    from bson import ObjectId
    if not ObjectId.is_valid(center_id):
        raise HTTPException(status_code=400, detail="Invalid center ID")
    
    center = await db["recycling_centers"].find_one({"_id": ObjectId(center_id)})
    if not center:
        raise HTTPException(status_code=404, detail="Recycling center not found")

    return ResponseSchema(
        success=True,
        data={
            "center_id": center_id,
            "center_name": center.get("name"),
            "qr_payload": center.get("qr_code_data", f"ECOSORT_CENTER_{center_id}")
        }
    )
