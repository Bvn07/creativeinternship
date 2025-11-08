from fastapi import APIRouter
from app.models.scratch_card import ScratchCard
from app.database import db
from datetime import datetime, timedelta
import random

router = APIRouter()

@router.post("/scratch-cards/generate")
async def generate_scratch_cards(numberOfScratchCards: int):

    active_cards_count = await db["scratch_cards"].count_documents({"isUsed": False})

    if active_cards_count >= numberOfScratchCards:
        return {
            "message": f"{active_cards_count} number of active scratch cards still exists in the DB. Did not create any new scratch cards"
        }

    new_cards = []

    for _ in range(numberOfScratchCards):
        card = ScratchCard(
            discountAmount=random.uniform(0, 1000),
            expiryDate=datetime.utcnow() + timedelta(days=5),
            isUsed=False
        )

        result = await db["scratch_cards"].insert_one(card.dict())
        new_cards.append({**card.dict(), "id": str(result.inserted_id)})

    return {
        "message": f"{numberOfScratchCards} scratch cards created successfully",
        "scratchCards": new_cards
    }
