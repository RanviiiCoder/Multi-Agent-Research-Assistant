---
title: Multi Agent Research Assistant
emoji: 🕵️
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---
# Multi-Agent Research Assistant

🚀 **[Try the Live Application on Hugging Face Spaces!](https://huggingface.co/spaces/RanviiiCoder/Multi-Agent-Research-Assistant)**

An autonomous AI research assistant powered by LangGraph, Google Gemini, and DuckDuckGo. 

## Overview
You provide a research topic, and a team of AI agents collaboratively:
1. **Search**: Gather relevant information from the web.
2. **Summarize**: Distill the found information into key points.
3. **Write**: Compile a structured, comprehensive markdown report.
4. **Review**: Critique the report for gaps and quality, optionally requesting a rewrite.

## Technology Stack
- **Backend**: FastAPI, LangGraph, `langchain-google-genai`, FAISS
- **Frontend**: Streamlit
- **Search**: DuckDuckGo API
- **Infrastructure**: Docker & Docker Compose

## Setup Instructions

### 1. Environment Variables
Copy `.env.example` to `.env` and fill in your Gemini API key.
```bash
cp .env.example .env
```

### 2. Running Locally (Without Docker)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### 3. Running with Docker Compose
```bash
docker-compose up --build
```
The backend will be available at `http://localhost:8000` and the frontend at `http://localhost:8501`.
