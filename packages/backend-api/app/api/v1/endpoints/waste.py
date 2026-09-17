from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.core.database import get_db
from app.api.v1.endpoints.users import get_current_user_id
from app.middleware.upload_validation import validate_image_upload
from app.schemas.common import ResponseSchema
import sys
from pathlib import Path
_curr = Path(__file__).resolve()
while _curr.parent != _curr:
    if (_curr / "packages").exists() or (_curr / ".git").exists():
        if str(_curr) not in sys.path:
            sys.path.insert(0, str(_curr))
        break
    _curr = _curr.parent

from packages.ai_engine.inference.predictor import MobileNetWastePredictor

router = APIRouter()
predictor = MobileNetWastePredictor()


@router.post("/classify", response_model=ResponseSchema[dict])
async def classify_waste_image(
    file: UploadFile = File(...),
    is_rural_setting: bool = Form(False),
    user_id: str = Depends(get_current_user_id),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Upload waste image, run MobileNetV3 AI inference, record scan, update user carbon offset, and issue Eco-Coins.
    """
    # 1. Sanitize file
    image_bytes = await validate_image_upload(file)

    # 2. Execute PyTorch / MobileNetV3 Prediction
    ai_result = predictor.predict_image_bytes(image_bytes)
    label = ai_result["primary_label"]
    category = ai_result["category"]
    confidence = ai_result["confidence_score"]
    carbon_saved = ai_result["carbon_saved_kg"]
    upcycling = ai_result["upcycling_ideas"]

    # 3. Lookup disposal instructions from waste_knowledge_base
    kb_doc = await db["waste_knowledge_base"].find_one({"category_code": label})
    if not kb_doc:
        kb_doc = await db["waste_knowledge_base"].find_one({"waste_type": category})

    bin_color = kb_doc.get("bin_color", "BLUE") if kb_doc else "BLUE"
    urban_instructions = kb_doc.get("urban_instructions_en", "Dispose in dry recyclable bin.") if kb_doc else "Dispose in dry bin."
    rural_instructions = kb_doc.get("rural_instructions_en", "Handover to local Kabadiwala.") if kb_doc else "Handover to local Kabadiwala."
    reward_points = kb_doc.get("eco_coins_reward", 10) if kb_doc else 10

    # 4. Save scan record to MongoDB
    scan_doc = {
        "user_id": ObjectId(user_id),
        "image_url": f"https://s3.ap-south-1.amazonaws.com/ecosort/scans/{file.filename}",
        "ai_result": {
            "primary_label": label,
            "category": category,
            "confidence_score": confidence
        },
        "disposal_guidance": {
            "setting": "RURAL" if is_rural_setting else "URBAN",
            "bin_color": bin_color,
            "urban_instructions": urban_instructions,
            "rural_instructions": rural_instructions,
            "upcycling_ideas": upcycling
        },
        "carbon_saved_kg": carbon_saved,
        "eco_coins_earned": reward_points,
        "status": "COMPLETED",
        "created_at": datetime.now(timezone.utc)
    }
    scan_res = await db["scans"].insert_one(scan_doc)

    # 5. Update user impact metrics & unlock badges
    sustainability_service = SustainabilityService(db)
    impact = await sustainability_service.update_user_impact(user_id, carbon_saved, reward_points)

    return ResponseSchema(
        success=True,
        message="Waste classified successfully",
        data={
            "scan_id": str(scan_res.inserted_id),
            "classification": {
                "label": label,
                "category": category,
                "confidence_score": confidence
            },
            "disposal_guidance": {
                "bin_color": bin_color,
                "instructions": rural_instructions if is_rural_setting else urban_instructions,
                "upcycling_ideas": upcycling
            },
            "rewards": {
                "eco_coins_earned": reward_points,
                "carbon_saved_kg": carbon_saved,
                "new_sustainability_score": impact.get("sustainability_score"),
                "newly_unlocked_badges": impact.get("newly_unlocked_badges", [])
            }
        }
    )


@router.get("/history", response_model=ResponseSchema[dict])
async def get_user_scan_history(
    limit: int = 20,
    user_id: str = Depends(get_current_user_id),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Retrieve user's historical waste scans."""
    cursor = db["scans"].find({"user_id": ObjectId(user_id)}).sort("created_at", -1).limit(limit)
    scans = []
    async for doc in cursor:
        scans.append({
            "id": str(doc["_id"]),
            "image_url": doc.get("image_url"),
            "primary_label": doc.get("ai_result", {}).get("primary_label"),
            "category": doc.get("ai_result", {}).get("category"),
            "confidence_score": doc.get("ai_result", {}).get("confidence_score"),
            "carbon_saved_kg": doc.get("carbon_saved_kg", 0.0),
            "eco_coins_earned": doc.get("eco_coins_earned", 0),
            "created_at": doc.get("created_at").isoformat() if isinstance(doc.get("created_at"), datetime) else str(doc.get("created_at"))
        })
    return ResponseSchema(success=True, data={"total": len(scans), "scans": scans})
