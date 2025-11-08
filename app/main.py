from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.routes.scratch_routes import router as scratch_router 

app = FastAPI(title="Creative Internship API")

app.include_router(user_router)
app.include_router(scratch_router)