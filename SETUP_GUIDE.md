# 🤖 Endee RAG Assistant Setup Guide

## 🚀 Quick Start

### Prerequisites
- **Docker Desktop** (required for Endee server on Windows)
- **Python 3.8+** with pip

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start Endee Server
```bash
# Method 1: Automated setup (recommended)
python setup_endee.py

# Method 2: Manual Docker command
docker run --ulimit nofile=100000:100000 -p 8080:8080 -v ./endee-data:/data --name endee-server --restart unless-stopped endeeio/endee-server:latest
```

### Step 3: Verify Endee Server
```bash
# Check if server is running
curl http://localhost:8080/api/v1/health

# Or open in browser: http://localhost:8080
```

### Step 4: Run the Application

**Streamlit Frontend:**
```bash
streamlit run app.py
# Open: http://localhost:8501
```

**FastAPI Backend:**
```bash
python backend_simple.py
# API docs: http://localhost:8000/docs
```

## 🔧 Configuration

Create a `.env` file from `.env.example`:
```bash
cp .env.example .env
```

Environment variables:
```env
# Required
ENDEE_URL=http://127.0.0.1:8080
ENDEE_AUTH_TOKEN=                    # Optional auth token

# Optional
OPENAI_API_KEY=your_openai_key_here  # For better responses
INDEX_NAME=rag_documents
EMBED_MODEL=all-MiniLM-L6-v2
CHUNK_SIZE=700
CHUNK_OVERLAP=120
TOP_K=5
```

## 🐛 Troubleshooting

### "Endee server is not running" Error
**Cause:** Endee Docker container is not running

**Solution:**
1. Install Docker Desktop
2. Run the setup script:
   ```bash
   python setup_endee.py
   ```
3. Or start manually:
   ```bash
   docker run --ulimit nofile=100000:100000 -p 8080:8080 -v ./endee-data:/data --name endee-server --restart unless-stopped endeeio/endee-server:latest
   ```

### Port 8080 Already in Use
**Check what's using port 8080:**
```bash
netstat -ano | findstr :8080
```

**Solutions:**
1. Stop the service using port 8080
2. Use different port (8081):
   ```bash
   docker run --ulimit nofile=100000:100000 -p 8081:8080 -v ./endee-data:/data --name endee-server --restart unless-stopped endeeio/endee-server:latest
   ```
3. Update `ENDEE_URL` in `.env` to `http://127.0.0.1:8081`

### Docker Issues
**Docker not found:**
- Install Docker Desktop from https://www.docker.com/products/docker-desktop/
- Start Docker Desktop application
- Wait for it to fully initialize

**Permission denied:**
- Make sure Docker Desktop is running
- Try running PowerShell/CMD as Administrator

### Connection Timeout
**Server taking too long to start:**
- Wait 30-60 seconds after starting Docker container
- Check with: `curl http://localhost:8080/api/v1/health`
- If still failing, restart Docker Desktop

## 📋 Verification Commands

```bash
# Check Docker containers
docker ps

# Check Endee health
curl http://localhost:8080/api/v1/health

# Check port availability
netstat -ano | findstr :8080

# Test Python connection
python -c "from ingest import check_endee_server; print('Endee connected:', check_endee_server())"
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   FastAPI        │    │   Endee Server  │
│   Frontend      │◄──►│   Backend        │◄──►│   (Docker)      │
│   :8501         │    │   :8000          │    │   :8080         │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📚 API Endpoints

### Backend API (http://localhost:8000)
- `GET /` - API information
- `GET /health` - Health check
- `POST /upload` - Upload documents
- `POST /query` - RAG queries
- `GET /docs` - Swagger documentation

### Endee API (http://localhost:8080)
- `GET /api/v1/health` - Server health
- `GET /api/v1/indexes` - List indexes
- Document and vector operations

## 🎯 Features

✅ **Document Upload**: PDF, TXT, MD files  
✅ **Text Chunking**: Intelligent splitting with overlap  
✅ **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)  
✅ **Vector Storage**: Endee with cosine similarity  
✅ **Semantic Search**: Find similar documents  
✅ **RAG**: Retrieval-augmented generation  
✅ **Fallback Mode**: Works without OpenAI API  
✅ **REST API**: Clean FastAPI endpoints  
✅ **Web UI**: Beautiful Streamlit interface  

## 🚀 Production Tips

1. **Security**: Set `ENDEE_AUTH_TOKEN` in production
2. **Scaling**: Use Docker Compose for multiple services
3. **Monitoring**: Add health checks and logging
4. **Performance**: Adjust `CHUNK_SIZE` and `TOP_K` as needed
5. **Backup**: Backup the `./endee-data` directory regularly

## 📞 Support

If you encounter issues:
1. Run `python setup_endee.py` for automated diagnosis
2. Check Docker Desktop is running
3. Verify port 8080 is available
4. Check the troubleshooting section above

---

**🎉 Your Endee RAG Assistant is ready to use!**
