FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py seed_demo.py ./
COPY ingest/ ./ingest/
COPY pricing/ ./pricing/

# Create non-root user
RUN useradd -m -u 1000 costforge \
    && chown -R costforge:costforge /app

USER costforge

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]