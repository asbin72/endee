import sys
import os
from fastapi import APIRouter

# Add parent directory to path to import from main modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.models import HealthResponse
from ingest import get_client
from config import INDEX_NAME

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check if the backend is healthy and Endee is accessible"""
    try:
        client = get_client()
        indexes = client.list_indexes()
        endee_connected = True
    except Exception as e:
        endee_connected = False
    
    return HealthResponse(
        status="healthy",
        index_name=INDEX_NAME,
        endee_connected=endee_connected
    )
