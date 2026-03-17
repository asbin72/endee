import os
import re
from io import BytesIO
from pypdf import PdfReader

def read_uploaded_file(uploaded_file) -> str:
    name = uploaded_file.name.lower()

    if name.endswith(".pdf"):
        pdf = PdfReader(BytesIO(uploaded_file.read()))
        pages = []
        for page in pdf.pages:
            text = page.extract_text() or ""
            pages.append(text)
        return "\n".join(pages)

    if name.endswith(".txt") or name.endswith(".md"):
        return uploaded_file.read().decode("utf-8", errors="ignore")

    raise ValueError("Unsupported file type. Upload PDF, TXT, or MD.")

def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text

def chunk_text(text: str, chunk_size: int = 700, overlap: int = 120) -> list[str]:
    text = clean_text(text)
    if not text:
        return []

    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk = text[start:end].strip()

        # try not to cut in the middle of a sentence
        if end < text_len:
            last_period = chunk.rfind(". ")
            last_newline = chunk.rfind("\n")
            cut = max(last_period, last_newline)
            if cut > int(chunk_size * 0.6):
                chunk = chunk[:cut + 1].strip()
                end = start + len(chunk)

        if chunk:
            chunks.append(chunk)

        if end >= text_len:
            break

        start = max(end - overlap, start + 1)

    return chunks

def safe_id(file_name: str, idx: int) -> str:
    base = os.path.splitext(os.path.basename(file_name))[0]
    base = re.sub(r"[^a-zA-Z0-9_-]+", "_", base)
    return f"{base}_{idx}"