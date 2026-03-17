# Endee RAG Assistant Backend

A FastAPI backend for document ingestion and RAG (Retrieval-Augmented Generation) queries using Endee vector database.

## Features

- **Document Upload**: Upload PDF, TXT, and MD files
- **Document Ingestion**: Automatic text chunking and embedding
- **RAG Queries**: Ask questions about uploaded documents
- **Health Check**: Monitor backend and Endee connection status
- **RESTful API**: Clean, documented API endpoints

## API Endpoints

### Base URL: `http://localhost:8000/api/v1`

### Health Check
```
GET /health
```
Returns the health status of the backend and Endee connection.

### Upload Documents
```
POST /upload
Content-Type: multipart/form-data

Parameters:
- files: List of files (PDF, TXT, MD)
- category: Category label (default: "general")
```

### Query Documents
```
POST /query
Content-Type: application/json

Body:
{
  "query": "Your question here",
  "top_k": 5
}
```

### API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start Backend**
   ```bash
   python start_backend.py
   ```

## Testing

Run the test client:
```bash
python test_backend.py
```

## Configuration

Environment variables (`.env` file):

```env
OPENAI_API_KEY=your_openai_api_key_here
INDEX_NAME=rag_documents
EMBED_MODEL=all-MiniLM-L6-v2
CHUNK_SIZE=700
CHUNK_OVERLAP=120
TOP_K=5
ENDEE_AUTH_TOKEN=your_endee_auth_token_here
```

## Project Structure

```
backend/
├── app.py              # Main FastAPI application
├── models.py           # Pydantic models
└── routers/
    ├── health.py       # Health check endpoint
    ├── upload.py       # Document upload endpoint
    ├── query.py        # RAG query endpoint
    └── documents.py    # Document management endpoints

start_backend.py        # Startup script
test_backend.py         # Test client
backend_simple.py       # Simplified backend (all-in-one)
```

## Usage Examples

### Upload Documents

```python
import requests

files = {'files': open('document.pdf', 'rb')}
data = {'category': 'research'}

response = requests.post(
    'http://localhost:8000/api/v1/upload',
    files=files,
    data=data
)
```

### Query Documents

```python
import requests

query_data = {
    "query": "What are the main findings?",
    "top_k": 3
}

response = requests.post(
    'http://localhost:8000/api/v1/query',
    json=query_data
)
```

## Development

The backend is built with:
- **FastAPI**: Modern, fast web framework
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server
- **Endee**: Vector database for embeddings
- **Sentence Transformers**: Text embeddings
- **OpenAI**: Optional LLM for responses

## Error Handling

The API returns proper HTTP status codes and error messages:
- `400`: Bad request (missing files, empty query)
- `500`: Internal server error (Endee connection issues, processing errors)

## CORS

The backend is configured to allow cross-origin requests from any origin. In production, you should restrict this to your frontend domain.
