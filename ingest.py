import requests
from endee import Endee, Precision
from requests.exceptions import RequestException
from config import INDEX_NAME, ENDEE_AUTH_TOKEN, CHUNK_SIZE, CHUNK_OVERLAP, ENDEE_URL
from embedder import get_dimension, embed_texts
from utils import chunk_text, safe_id

def check_endee_server():
    """Check if Endee server is running and accessible"""
    try:
        response = requests.get(f"{ENDEE_URL}/api/v1/health", timeout=3)
        response.raise_for_status()
        return True
    except RequestException as e:
        return False

def get_client():
    """Get Endee client with proper connection checking"""
    if not check_endee_server():
        raise RuntimeError(
            " Endee server is not running!\n\n"
            " Start it first with Docker:\n"
            "docker run --ulimit nofile=100000:100000 -p 8080:8080 "
            "-v ./endee-data:/data --name endee-server --restart unless-stopped "
            "endeeio/endee-server:latest\n\n"
            " Then verify:\n"
            " Open http://localhost:8080 in browser\n"
            " Or run: curl http://localhost:8080/api/v1/health\n\n"
            " If port 8080 is busy, use different port:\n"
            "docker run --ulimit nofile=100000:100000 -p 8081:8080 "
            "-v ./endee-data:/data --name endee-server --restart unless-stopped "
            "endeeio/endee-server:latest\n"
            "Then update ENDEE_URL to 'http://127.0.0.1:8081' in config.py"
        )
    
    # Use mock client for testing
    try:
        return EndeeClient(base_url=ENDEE_URL, auth_token=ENDEE_AUTH_TOKEN)
    except:
        # Fallback to original Endee client
        if ENDEE_AUTH_TOKEN:
            return Endee(ENDEE_AUTH_TOKEN)
        return Endee()

class EndeeClient:
    """Mock Endee client that works with our mock server"""
    def __init__(self, base_url, auth_token=None):
        self.base_url = base_url
        self.auth_token = auth_token
        self.session = requests.Session()
        if auth_token:
            self.session.headers.update({"Authorization": f"Bearer {auth_token}"})
    
    def list_indexes(self):
        """List all indexes"""
        response = self.session.get(f"{self.base_url}/api/v1/indexes")
        response.raise_for_status()
        return response.json()
    
    def create_index(self, name, dimension, space_type="cosine", precision="INT8"):
        """Create a new index"""
        data = {
            "name": name,
            "dimension": dimension,
            "space_type": space_type,
            "precision": precision
        }
        response = self.session.post(f"{self.base_url}/api/v1/index/create", json=data)
        response.raise_for_status()
        return response.json()
    
    def get_index(self, name):
        """Get an index object"""
        response = self.session.get(f"{self.base_url}/api/v1/index/{name}")
        response.raise_for_status()
        return IndexWrapper(self.base_url, name, self.session, self.auth_token)
    
class IndexWrapper:
    """Wrapper for index operations"""
    def __init__(self, base_url, name, session, auth_token):
        self.base_url = base_url
        self.name = name
        self.session = session
        self.auth_token = auth_token
    
    def upsert(self, vectors):
        """Upsert vectors to index"""
        response = self.session.post(f"{self.base_url}/api/v1/index/{self.name}/vectors", json=vectors)
        response.raise_for_status()
        return response.json()
    
    def query(self, vector, top_k=5, query_text=None):
        """Query index for similar vectors"""
        data = {
            "vector": vector,
            "top_k": top_k
        }
        # Add query text if available for better similarity matching
        if query_text:
            data["query_text"] = query_text
        
        response = self.session.post(f"{self.base_url}/api/v1/index/{self.name}/query", json=data)
        response.raise_for_status()
        result = response.json()
        return result.get("results", [])

def ensure_index():
    client = get_client()
    index_names = []

    try:
        indexes = client.list_indexes()
        for item in indexes:
            if isinstance(item, dict) and "name" in item:
                index_names.append(item["name"])
            else:
                index_names.append(str(item))
    except Exception:
        indexes = []

    if INDEX_NAME not in index_names:
        client.create_index(
            name=INDEX_NAME,
            dimension=get_dimension(),
            space_type="cosine",
            precision=Precision.INT8
        )

    return client.get_index(name=INDEX_NAME)

def ingest_document(file_name: str, text: str, category: str = "general") -> dict:
    index = ensure_index()
    chunks = chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)

    if not chunks:
        return {"inserted": 0, "chunks": []}

    vectors = embed_texts(chunks)
    payload = []

    for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
        payload.append({
            "id": safe_id(file_name, i),
            "vector": vector,
            "meta": {
                "source": file_name,
                "chunk_id": i,
                "text": chunk
            },
            "filter": {
                "category": category,
                "source": file_name
            }
        })

    index.upsert(payload)

    return {
        "inserted": len(payload),
        "chunks": chunks
    }