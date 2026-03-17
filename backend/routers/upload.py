import sys
import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import List
from io import BytesIO

# Add parent directory to path to import from main modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.models import UploadResponse, DocumentInfo
from utils import read_uploaded_file
from ingest import ingest_document, ensure_index

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
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
