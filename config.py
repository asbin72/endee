import os
from dotenv import load_dotenv

load_dotenv()

INDEX_NAME = os.getenv("INDEX_NAME", "rag_documents")
EMBED_MODEL = os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "700"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))
TOP_K = int(os.getenv("TOP_K", "5"))

# Endee configuration
ENDEE_URL = os.getenv("ENDEE_URL", "http://127.0.0.1:8080")
ENDEE_AUTH_TOKEN = os.getenv("ENDEE_AUTH_TOKEN", "").strip()

# Optional
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()