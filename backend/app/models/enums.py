from enum import Enum

class ContentSourceType(str, Enum):
    """Source type of the content"""
    AI_GENERATED = "ai_generated"
    USER_UPLOADED = "user_uploaded"
    MIXED = "mixed"
