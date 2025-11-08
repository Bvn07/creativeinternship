from fastapi import APIRouter, HTTPException
from app.database import db

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_stats():
    try:
        total_users = await db["users"].count_documents({})
        total_scratch_cards = await db["scratch_cards"].count_documents({})
        unused_scratch_cards = await db["scratch_cards"].count_documents({"isUsed": False})
        total_transactions = await db["transactions"].count_documents({})

        return {
            "totalUsers": total_users,
            "totalScratchCards": total_scratch_cards,
            "unusedScratchCards": unused_scratch_cards,
            "totalTransactions": total_transactions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard stats: {str(e)}")
