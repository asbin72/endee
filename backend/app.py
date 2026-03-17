from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager
import sys
import os

# Add parent directory to path to import from main modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import ErrorResponse
from backend.routers import upload, query, health, documents

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Endee RAG Assistant API...")
    yield
    # Shutdown
    logger.info("Shutting down Endee RAG Assistant API...")

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title="Endee RAG Assistant API",
        description="Backend API for document ingestion and RAG queries",
        version="1.0.0",
        lifespan=lifespan
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify actual origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health.router, prefix="/api/v1", tags=["health"])
    app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
    app.include_router(query.router, prefix="/api/v1", tags=["query"])
    app.include_router(documents.router, prefix="/api/v1", tags=["documents"])

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        return ErrorResponse(
            error=exc.detail,
            detail=str(exc.status_code)
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        logger.error(f"Unexpected error: {exc}")
        return ErrorResponse(
            error="Internal server error",
            detail=str(exc)
        )

    @app.get("/")
    async def root():
        """Root endpoint with API info"""
        return {
            "message": "Endee RAG Assistant API",
            "version": "1.0.0",
            "docs": "/docs",
            "redoc": "/redoc",
            "endpoints": {
                "health": "/api/v1/health",
                "upload": "/api/v1/upload",
                "query": "/api/v1/query",
                "documents": "/api/v1/documents"
            }
        }

    return app

# Create the app instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
