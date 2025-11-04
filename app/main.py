from fastapi import FastAPI
from app.routes.user_routes import router as user_router

app = FastAPI(title="Creative Internship API")

app.include_router(user_router)
