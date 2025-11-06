from fastapi import APIRouter
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
    result = await db.users.insert_one(user.dict())
    return {"id": str(result.inserted_id), **user.dict()}

@router.get("/users")
async def get_users():
    users = await db.users.find().to_list(100)
    return [serialize_user(user) for user in users]

@router.get("/users/{id}")
async def get_user(id: str):
    user = await db.users.find_one({"_id": ObjectId(id)})
    return serialize_user(user)

@router.put("/users/{id}")
async def update_user(id: str, user: User):
    await db.users.update_one({"_id": ObjectId(id)}, {"$set": user.dict()})
    return {"message": "User updated"}

@router.delete("/users/{id}")
async def delete_user(id: str):
    await db.users.delete_one({"_id": ObjectId(id)})
    return {"message": "User deleted"}


@router.get("/users")
async def get_users():
    users = []
    cursor = db["users"].find({})
    async for document in cursor:
        document["id"] = str(document["_id"])  
        del document["_id"]                     
        users.append(document)
    return users
