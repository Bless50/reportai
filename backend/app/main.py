from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import user, report
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
            "name": "reports",
            "description": "Report management operations"
        }
    ]
)

# Add CORS middleware with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Can be restricted to ["GET", "POST", "PUT", "DELETE"]
    allow_headers=["*"],  # Can be restricted to specific headers
    max_age=600  # Cache preflight requests for 10 minutes
)

# Include routers with base prefix
app.include_router(user.router, prefix="/api/v1/users")
app.include_router(report.router, prefix="/api/v1/reports")