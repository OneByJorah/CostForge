# =============================================================================
# CostForge Backend — FastAPI + Uvicorn
# Tag convention: jorahone/costforge-backend:latest
# =============================================================================
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Production stage ────────────────────────────────────────────────────────
FROM python:3.12-slim

WORKDIR /app

# Runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY backend/main.py ./
COPY backend/seed_demo.py ./
COPY backend/ingest/ ./ingest/
COPY backend/providers.json ./
COPY pricing/catalog.json ./pricing.json

# Create non-root user
RUN addgroup --system --gid 1001 costforge && \
    adduser --system --uid 1001 --ingroup costforge --no-create-home costforge && \
    mkdir -p /app/data && \
    chown -R costforge:costforge /app

USER costforge

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=5 --start-period=15s \
    CMD curl -sf http://localhost:8000/healthz || exit 1

LABEL org.opencontainers.image.title="CostForge Backend" \
      org.opencontainers.image.description="FastAPI backend for CostForge API cost tracking" \
      org.opencontainers.image.vendor="JorahOne" \
      org.opencontainers.image.version="1.0.0"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
