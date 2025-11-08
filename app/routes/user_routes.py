from fastapi import APIRouter, HTTPException
from app.models.user import User
from app.database import db
from bson import ObjectId

router = APIRouter()


def serialize_user(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "age": user["age"]
    }


@router.post("/users")
async def create_user(user: User):
    result = await db["users"].insert_one(user.dict())
    created_user = await db["users"].find_one({"_id": result.inserted_id})
    return serialize_user(created_user)



@router.get("/users")
async def get_users():
    users = []
    cursor = db["users"].find({})
    async for document in cursor:
        users.append(serialize_user(document))
    return users


@router.get("/users/{id}")
async def get_user(id: str):
    try:
        user = await db["users"].find_one({"_id": ObjectId(id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return serialize_user(user)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID")



@router.put("/users/{id}")
async def update_user(id: str, user: User):
    try:
        result = await db["users"].update_one(
            {"_id": ObjectId(id)},
            {"$set": user.dict()}
        )

        if result.modified_count == 1:
            return {"message": "User updated successfully"}

        raise HTTPException(status_code=404, detail="User not found or no changes applied")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID")



@router.delete("/users/{id}")
async def delete_user(id: str):
    try:
        result = await db["users"].delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 1:
            return {"message": "User deleted successfully"}

        raise HTTPException(status_code=404, detail="User not found")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID")
