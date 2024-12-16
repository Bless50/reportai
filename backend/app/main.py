# Import FastAPI and CORS middleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Import our user router
from app.api.v1.endpoints.user import router as user_router

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create FastAPI app instance
app = FastAPI(
    title="ReportAI API",
    description="API for generating internship reports",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include our routers
app.include_router(
    user_router,
    prefix="/api/v1/users",  # All user routes start with /api/v1/users
    tags=["users"]  # For API documentation
)

# Root endpoint
@app.get("/")
def read_root():
    """
    Root endpoint - can be used to check if API is running
    """
    return {
        "message": "Welcome to ReportAI API",
        "version": "1.0.0",
        "status": "active"
    }