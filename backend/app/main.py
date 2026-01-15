"""
AIZA Enterprise AI Platform - Main Application
The Complete AI Solution for Modern Enterprises

Built with ❤️ by AIZA
"""

import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time

from app.core.config import settings
from app.core.database import init_db
from app.api.v1 import api_router
from app.core.logging import setup_logging
from app.core.monitoring import setup_monitoring

# Setup logging
logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("🚀 Starting AIZA Enterprise AI Platform...")
    init_db()
    setup_monitoring()
    logger.info("✅ Platform initialized successfully")
    yield
    # Shutdown
    logger.info("👋 Shutting down AIZA Enterprise AI Platform...")


# Initialize FastAPI application
app = FastAPI(
    title="AIZA Enterprise AI Platform",
    description="The Complete AI Solution for Modern Enterprises",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "AIZA Enterprise AI Platform",
        "version": "1.0.0",
        "status": "operational",
        "description": "The Complete AI Solution for Modern Enterprises",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AIZA Enterprise AI Platform",
        "version": "1.0.0",
        "timestamp": time.time()
    }


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    from app.core.monitoring import get_metrics
    return get_metrics()


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║   AIZA Enterprise AI Platform v1.0.0                      ║
    ║   Built with ❤️ by AIZA                                   ║
    ╚═══════════════════════════════════════════════════════════╝
    
    🌐 Server: http://{settings.HOST}:{settings.PORT}
    📚 API Docs: http://{settings.HOST}:{settings.PORT}/docs
    📊 Metrics: http://{settings.HOST}:{settings.PORT}/metrics
    🏥 Health: http://{settings.HOST}:{settings.PORT}/health
    
    🎯 Features Enabled:
       ✅ Voice AI
       ✅ Document Intelligence
       ✅ Multi-Agent Workflows
       ✅ Real-time Analytics
       ✅ Enterprise Security
    
    """)
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
        access_log=True
    )
