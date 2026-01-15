"""
API v1 Router
"""

from fastapi import APIRouter

api_router = APIRouter()

# Import and include routers
# from app.api.v1.endpoints import voice, document, agent, analytics

@api_router.get("/status")
async def status():
    """API status endpoint"""
    return {
        "status": "operational",
        "version": "1.0.0",
        "features": {
            "voice_ai": True,
            "document_intelligence": True,
            "multi_agent": True,
            "analytics": True
        }
    }
