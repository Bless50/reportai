from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title="ReportAI API",
    description="API for generating internship reports",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "authentication",
            "description": "User authentication operations (register, login, logout)"
        },
        {
            "name": "profile",
            "description": "User profile operations (view, update, delete)"
        },
        {
            "name": "report-management",
            "description": "Report and chapter management operations"
        },
        {
            "name": "content-management",
            "description": "Section content operations (type, upload, generate AI content, files)"
        }
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")