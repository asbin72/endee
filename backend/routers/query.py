import sys
import os
from fastapi import APIRouter, HTTPException

# Add parent directory to path to import from main modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.models import QueryRequest, QueryResponse
from rag import run_rag

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query the RAG system with a question"""
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        answer, results = run_rag(request.query, top_k=request.top_k)
        
        return QueryResponse(
            answer=answer,
            results=results,
            query=request.query
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
