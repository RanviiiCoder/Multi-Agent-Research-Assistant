FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt backend_reqs.txt
COPY frontend/requirements.txt frontend_reqs.txt

# Install dependencies
RUN pip install --no-cache-dir -r backend_reqs.txt -r frontend_reqs.txt

# Copy all code
COPY . .

# Make the run script executable
RUN chmod +x run.sh

# Expose the HF Spaces port
EXPOSE 7860

# Run the unified script
CMD ["./run.sh"]
