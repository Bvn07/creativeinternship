from fastapi import APIRouter, HTTPException
from app.database import db
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/scratch-cards/expiring-soon")
async def get_expiring_soon_cards():
    """
    Returns all scratch cards that will expire in the next 2 days.
    """
    now = datetime.utcnow()
    two_days_later = now + timedelta(days=2)

    cards = []
    cursor = db["scratch_cards"].find({
        "expiryDate": {"$gte": now, "$lte": two_days_later},
        "isUsed": False
    })
    async for card in cursor:
        card["_id"] = str(card["_id"])
        cards.append(card)

    if not cards:
        return {"message": "No scratch cards expiring soon"}
    return {"expiringSoonCards": cards}
