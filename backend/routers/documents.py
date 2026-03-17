import sys
import os
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

# Add parent directory to path to import from main modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ingest import ensure_index

router = APIRouter()

@router.get("/documents")
async def list_documents():
    """List all documents in the index"""
    try:
        index = ensure_index()
        # Note: This is a simplified approach. You might need to adapt based on Endee's API
        # For now, we'll return a basic response
        return {"documents": [], "message": "Document listing not fully implemented"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list documents: {str(e)}")

@router.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a specific document from the index"""
    try:
        index = ensure_index()
        # Note: This is a simplified approach. You might need to adapt based on Endee's API
        return {"message": f"Document {document_id} deletion not fully implemented"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")
