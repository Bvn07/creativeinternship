from fastapi import APIRouter, HTTPException
from app.models.transaction import Transaction
from app.database import db
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/transactions")
async def add_transaction(transaction: Transaction):
   
    user = await db["users"].find_one({"_id": ObjectId(transaction.userId)})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid userId")

    
    card = await db["scratch_cards"].find_one({"_id": ObjectId(transaction.scratchCardId)})
    if not card:
        raise HTTPException(status_code=400, detail="Invalid scratchCardId")

    if card.get("isUsed", False):
        raise HTTPException(status_code=400, detail="Scratch card already used")

    
    expiry = card.get("expiryDate")
    if expiry and datetime.fromisoformat(str(expiry).replace("Z", "")) < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Scratch card expired")

 
    transaction_data = transaction.model_dump()

    result = await db["transactions"].insert_one(transaction_data)

    
    await db["scratch_cards"].update_one(
        {"_id": ObjectId(transaction.scratchCardId)},
        {"$set": {"isUsed": True}}
    )

    
    return {
        "message": "Transaction added successfully",
        "transactionId": str(result.inserted_id),
        "userId": str(transaction.userId),
        "scratchCardId": str(transaction.scratchCardId),
        "transactionAmount": transaction.transactionAmount,
        "dateOfTransaction": str(transaction.dateOfTransaction)
    }
