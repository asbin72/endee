from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import tempfile
import shutil
from io import BytesIO
import uuid

from utils import read_uploaded_file, chunk_text
from ingest import ingest_document, ensure_index, get_client
from rag import run_rag
from config import INDEX_NAME

app = FastAPI(
    title="Endee RAG Assistant API",
    description="Backend API for document ingestion and RAG queries",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/health", response_model=HealthResponse)
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

@app.post("/upload", response_model=UploadResponse)
async def upload_documents(
    files: List[UploadFile] = File(...),
    category: str = Form(default="general")
):
    """Upload and ingest multiple documents"""
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    total_inserted = 0
    document_infos = []
    errors = []
    
    # Ensure index exists
    try:
        ensure_index()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ensure index: {str(e)}")
    
    for file in files:
        try:
            # Validate file type
            if not file.filename.lower().endswith(('.pdf', '.txt', '.md')):
                errors.append(f"{file.filename}: Unsupported file type")
                continue
            
            # Read file content
            content = await file.read()
            temp_file = BytesIO(content)
            temp_file.name = file.filename
            
            # Process the file
            text = read_uploaded_file(temp_file)
            result = ingest_document(file.filename, text, category=category)
            
            chunks_inserted = result["inserted"]
            total_inserted += chunks_inserted
            
            document_infos.append(DocumentInfo(
                filename=file.filename,
                category=category,
                chunks_inserted=chunks_inserted
            ))
            
        except Exception as e:
            errors.append(f"{file.filename}: {str(e)}")
    
    success = len(document_infos) > 0
    message = f"Successfully processed {len(document_infos)} files"
    
    if errors:
        message += f". Errors: {'; '.join(errors)}"
    
    return UploadResponse(
        success=success,
        message=message,
        documents=document_infos
    )

@app.post("/query", response_model=QueryResponse)
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

@app.get("/documents")
async def list_documents():
    """List all documents in the index"""
    try:
        index = ensure_index()
        # Note: This is a simplified approach. You might need to adapt based on Endee's API
        # For now, we'll return a basic response
        return {"documents": [], "message": "Document listing not fully implemented"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list documents: {str(e)}")

@app.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a specific document from the index"""
    try:
        index = ensure_index()
        # Note: This is a simplified approach. You might need to adapt based on Endee's API
        return {"message": f"Document {document_id} deletion not fully implemented"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "message": "Endee RAG Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "upload": "/upload",
            "query": "/query",
            "documents": "/documents",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
