from fastapi import APIRouter, HTTPException, Query
from app.models.transaction import Transaction
from app.database import db
from bson import ObjectId
from datetime import datetime, timedelta

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
    transaction_data["dateOfTransaction"] = datetime.utcnow()  

    result = await db["transactions"].insert_one(transaction_data)

    await db["scratch_cards"].update_one(
        {"_id": ObjectId(transaction.scratchCardId)},
        {"$set": {"isUsed": True}}
    )

    return {
        "message": "Transaction added successfully",
        "transactionId": str(result.inserted_id),
        **transaction_data
    }



@router.get("/transactions")
async def get_transactions(
    dateOfTransaction: str | None = Query(None, description="Filter by date (YYYY-MM-DD or ISO format)"),
    userId: str | None = Query(None, description="Filter by user ID"),
    transactionAmount: float | None = Query(None, description="Filter by transaction amount")
):
    filters = {}

    if userId:
        filters["userId"] = userId
    if transactionAmount is not None:
        filters["transactionAmount"] = transactionAmount

 
    if dateOfTransaction:
        try:
            query_date = datetime.fromisoformat(dateOfTransaction)
        except ValueError:
            try:
                query_date = datetime.strptime(dateOfTransaction, "%Y-%m-%d")
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid dateOfTransaction format. Use YYYY-MM-DD or ISO date.")

        start_of_day = query_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = query_date.replace(hour=23, minute=59, second=59, microsecond=999999)

        filters["dateOfTransaction"] = {"$gte": start_of_day, "$lte": end_of_day}

    cursor = db["transactions"].find(filters)
    transactions = []
    async for txn in cursor:
        txn["_id"] = str(txn["_id"])
        transactions.append(txn)

    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found")

    return {"transactions": transactions}
