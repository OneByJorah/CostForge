# CostForge — API / Platform Usage Dashboard

Self-hosted dashboard for tracking API usage and cost comparison across free and premium services.

## Verify locally
1. `cd backend`
2. `python3 -m venv .venv && source .venv/bin/activate`
3. `pip install fastapi uvicorn sqlalchemy aiosqlite httpx orjson pydantic-settings`
4. `uvicorn main:app --host 0.0.0.0 --port 9070`
5. Health: http://localhost:9070/healthz
6. Dashboard: http://localhost:9070/

## API
- `POST /ingest`
- `GET /api/summary?days=30`
- `GET /api/usage?days=30`

## Screenshots
- `docs/screenshots/costforge-dashboard.html`
