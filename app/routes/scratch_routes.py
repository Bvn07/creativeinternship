from fastapi import APIRouter, HTTPException
from app.models.scratch_card import ScratchCard
from app.database import db
from datetime import datetime, timedelta
import random

router = APIRouter()

@router.post("/scratch-cards/generate")
async def generate_scratch_cards(numberOfScratchCards: int):
    """
    Generate N new scratch cards.
    If unused cards >= N, no new cards are created.
    Each new card expires in 5 days and has a random discount between 0-1000.
    """

    active_cards_count = await db["scratch_cards"].count_documents({"isUsed": False})

    if active_cards_count >= numberOfScratchCards:
        return {
            "message": f"{active_cards_count} number of active scratch cards still exist in the DB. Did not create any new scratch cards."
        }

    new_cards = []

    for _ in range(numberOfScratchCards):
        card = ScratchCard(
            discountAmount=round(random.uniform(0, 1000), 2),
            expiryDate=datetime.utcnow() + timedelta(days=5),
            isUsed=False
        )

        result = await db["scratch_cards"].insert_one(card.model_dump())
        new_cards.append({**card.model_dump(), "id": str(result.inserted_id)})

    return {
        "message": f"{numberOfScratchCards} scratch cards created successfully",
        "scratchCards": new_cards
    }



@router.get("/scratch-cards/unused")
async def get_unused_scratch_cards():
    """Fetch all unused and unexpired scratch cards."""
    now = datetime.utcnow()
    cursor = db["scratch_cards"].find({"isUsed": False, "expiryDate": {"$gt": now}})
    unused_cards = []

    async for card in cursor:
        card["_id"] = str(card["_id"]) 
        unused_cards.append(card)

    if not unused_cards:
        raise HTTPException(status_code=404, detail="No unused scratch cards found")

    return {"unusedScratchCards": unused_cards}
