#!/bin/bash

# Start the FastAPI backend in the background
echo "Starting backend..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Start the Streamlit frontend in the foreground
echo "Starting frontend..."
streamlit run frontend/app.py --server.port 7860 --server.address 0.0.0.0
