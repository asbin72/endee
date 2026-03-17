# Endee RAG Assistant

## How It Works (Simple Explanation)

### 📚 Step 1: Document Upload
- You upload PDF, TXT, or Markdown files through the web interface
- The system reads and extracts text from your documents

### ✂️ Step 2: Text Chunking
- Long documents are broken into smaller, overlapping chunks
- Each chunk is like a "page" that can be understood independently
- Overlapping ensures no information is lost at chunk boundaries

### 🧠 Step 3: Text Embedding
- Each text chunk is converted into numbers (vectors) using AI
- These numbers capture the meaning and context of the text
- Similar concepts get similar number patterns

### 💾 Step 4: Storage in Endee
- All vectors are stored in Endee vector database
- Endee can quickly find similar vectors when you ask questions
- Think of it like a super-smart filing system

### ❓ Step 5: Your Question
- You type a question in natural language
- Your question is also converted into a vector

### 🔍 Step 6: Similarity Search
- Endee searches for chunks with vectors most similar to your question
- It returns the top 5 most relevant chunks
- Similarity scores show how well each chunk matches

### 🤖 Step 7: Answer Generation
- The system uses your retrieved chunks as context
- AI generates an answer based only on this context
- If no relevant chunks are found, it says so honestly

### 📋 Step 8: Source Display
- You see the answer with source file names
- You can also view the exact chunks that were used
- This helps you verify the information yourself

### 🔄 Complete Flow
```
Your Documents → Text Chunks → AI Embeddings → Endee Storage
                                                    ↑
                                                    ↓
Your Question → AI Embedding → Similarity Search → Relevant Chunks → AI Answer
```

### 🎯 Why This Works Better Than Simple Search
- **Understands Meaning**: Finds related concepts, not just exact words
- **Context-Aware**: Uses surrounding text for better understanding
- **Trustworthy**: Shows sources so you can verify
- **Focused**: Only uses your uploaded documents, not internet

## Features
- Upload PDF, TXT, and Markdown files
- Chunk and embed text using Sentence Transformers
- Store embeddings in Endee
- Ask questions in natural language
- Retrieve top relevant chunks
- Generate grounded answers
- Display sources and matched chunks

## Tech Stack
- Python
- Streamlit
- Endee Vector Database
- Sentence Transformers
- PyPDF
- Optional: OpenAI API for answer generation

## System Design
1. User uploads documents
2. Text is extracted and chunked
3. Chunks are converted into embeddings
4. Embeddings are stored in Endee
5. User asks a question
6. Query is embedded
7. Endee retrieves top matching chunks
8. LLM generates an answer from retrieved context

## Project Structure
```text
endee_rag_assistant/
├── app.py
├── config.py
├── embedder.py
├── ingest.py
├── rag.py
├── requirements.txt
├── README.md
├── .env.example
└── utils.py