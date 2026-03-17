from sentence_transformers import SentenceTransformer
from config import EMBED_MODEL

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model

def get_dimension() -> int:
    model = get_model()
    return model.get_sentence_embedding_dimension()

def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_model()
    vectors = model.encode(texts, normalize_embeddings=True)
    return [v.tolist() for v in vectors]

def embed_query(text: str) -> list[float]:
    model = get_model()
    vector = model.encode([text], normalize_embeddings=True)[0]
    return vector.tolist()