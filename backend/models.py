from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class QueryResponse(BaseModel):
    answer: str
    results: List[Dict[str, Any]]
    query: str

class DocumentInfo(BaseModel):
    filename: str
    category: str
    chunks_inserted: int

class UploadResponse(BaseModel):
    success: bool
    message: str
    documents: List[DocumentInfo]

class HealthResponse(BaseModel):
    status: str
    index_name: str
    endee_connected: bool

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
