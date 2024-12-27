# run.py
import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable reload for development
        workers=1,    # Single worker for development
        log_level="info" if settings.DEBUG else "error"
    )