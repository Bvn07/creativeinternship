from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.routes.scratch_routes import router as scratch_router 
from app.routes.transaction_routes import router as transaction_router
from app.routes.analytics_routes import router as analytics_router
from app.routes.dashboard_routes import router as dashboard_router


app = FastAPI(title="Creative Internship API")

app.include_router(user_router)
app.include_router(scratch_router)
app.include_router(transaction_router)
app.include_router(analytics_router)
app.include_router(dashboard_router) 