# CostForge — API Usage & Premium-vs-Free Cost Dashboard

Enterprise command-center for tracking AI / cloud API spend across self-hosted
and free-tier cloud services, with real-time cost comparisons against premium
paid tiers.

## What it does
- Ingest usage from JSONL usage log
- Aggregate hourly / daily / monthly
- Compare actual cost (free / self-hosted) vs premium equivalent
- Live HTML dashboard

## Repo layout
- `backend/` — FastAPI app (`main.py`, SQLite store, usage models)
- `backend/ingest/` — importers for Telegram, OpenAI, OpenRouter, Hermes
- `frontend/dist/` — all-in-one dashboard SPA
- `pricing/` — free + premium rate cards

## Quick start
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn sqlalchemy aiosqlite
uvicorn main:app --host 0.0.0.0 --port 8080
```
Then open the dashboard URL shown in logs.

## Headroom / Aphrodite integration
CostForge can meter traffic flowing through the local Headroom proxy defined in StackDeploy (`vendor/headroom`):
- StackDeploy container: `http://127.0.0.1:8787`
- Add provider `headroom` in `providers.json`
- Direct requests through `http://127.0.0.1:<costforge-port>/proxy/headroom/...`
- Usage, including premium-only-equivalent costs, lands in the same SQLite/usage view
