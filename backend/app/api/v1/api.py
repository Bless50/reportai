from fastapi import APIRouter
from app.api.v1.endpoints import user, report

api_router = APIRouter()

# Include routers from endpoints
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(report.router, prefix="/reports", tags=["reports"])
