import os
import requests
from config import OPENAI_API_KEY, TOP_K
from embedder import embed_query
from ingest import ensure_index

SYSTEM_PROMPT = """You are a helpful AI knowledge assistant.
Answer only from the retrieved context.
If the answer is not in the context, say:
"I could not find that in the uploaded documents."
Keep the answer clear and concise.
At the end, include a short 'Sources' section with file names.
"""

def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    index = ensure_index()
    qvec = embed_query(query)
    # Pass query text for better similarity matching in mock server
    results = index.query(vector=qvec, top_k=top_k, query_text=query)
    return results

def build_context(results: list[dict]) -> str:
    blocks = []
    for i, item in enumerate(results, start=1):
        meta = item.get("meta", {})
        source = meta.get("source", "unknown")
        text = meta.get("text", "")
        sim = item.get("similarity", 0)
        blocks.append(
            f"[Chunk {i}] Source: {source}\nSimilarity: {sim}\nText: {text}"
        )
    return "\n\n".join(blocks)

def answer_with_openai(query: str, context: str) -> str:
    if not OPENAI_API_KEY:
        return fallback_answer(query, context)

    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Question:\n{query}\n\nRetrieved Context:\n{context}"
                }
            ],
            "temperature": 0.2
        }

        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception:
        return fallback_answer(query, context)

def fallback_answer(query: str, context: str) -> str:
    if not context.strip():
        return "I could not find that in the uploaded documents."

    lines = context.split("\n")
    source_names = []
    text_parts = []

    for line in lines:
        if line.startswith("Source: "):
            source_names.append(line.replace("Source: ", "").strip())
        if line.startswith("Text: "):
            text_parts.append(line.replace("Text: ", "").strip())

    joined = " ".join(text_parts[:3]).strip()
    sources = ", ".join(sorted(set(source_names))) if source_names else "uploaded files"

    if not joined:
        return "I could not find that in the uploaded documents."

    return (
        f"Based on the retrieved document chunks, here is the most relevant information:\n\n"
        f"{joined}\n\n"
        f"Sources: {sources}"
    )

def run_rag(query: str) -> tuple[str, list[dict]]:
    results = retrieve(query)
    context = build_context(results)
    answer = answer_with_openai(query, context)
    return answer, results