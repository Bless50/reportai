from fastapi import APIRouter
from app.api.v1.endpoints import user, report, sections, references

api_router = APIRouter()

# Include routers from endpoints
api_router.include_router(user.router, prefix="/users")
api_router.include_router(report.router, prefix="/reports")
api_router.include_router(sections.router)  # Prefix already set in router
api_router.include_router(references.router, prefix="/references")
