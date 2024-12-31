from fastapi import APIRouter
from app.api.v1.endpoints import user, report, sections

api_router = APIRouter()

# Include routers from endpoints
api_router.include_router(user.router, prefix="/users")
api_router.include_router(report.router, prefix="/reports", tags=["report-management"])
api_router.include_router(sections.router, prefix="/sections", tags=["content-management"])
