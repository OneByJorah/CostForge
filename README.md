<div align="center">

![CostForge banner](docs/assets/banner.svg)

# CostForge

Self-hosted cloud and API cost estimation dashboard

![License](https://img.shields.io/badge/license-MIT-brightgreen)
![Language](https://img.shields.io/badge/language-Python-blue)
</div>

---

<p align="center">
  <img src="docs/assets/screenshot.png" alt="CostForge dashboard preview" width="90%">
</p>

<br>

---

## What It Does

CostForge sits between your applications and your LLM/API providers as a transparent metering proxy. Point a client at `/proxy/<provider>` instead of the provider's real URL and CostForge:

1. Forwards the request untouched
2. Parses token usage from the response (OpenAI-compatible, Ollama, or generic formats)
3. Maps each local/free model to its premium-API equivalent (e.g., `llama3.1:8b` → `gpt-4o-mini`)
4. Records what the same usage *would have cost* on paid APIs to SQLite
5. Shows live totals, per-provider breakdowns, and savings-over-time charts

## Features

- **Metering Proxy** — Route traffic through `/proxy/*` endpoints; every call is metered automatically.
- **Premium Equivalence** — Compare local/free-tier usage against GPT-4o, Claude, and Gemini per-million-token rates.
- **100% Self-Hosted** — No external services or accounts required; zero secrets in git.
- **Dark Dashboard** — Single-page dark-themed dashboard served by the backend.
- **Local Storage** — SQLite (WAL mode) for usage data, JSON for provider and pricing catalogs.
- **Live Updates** — WebSocket feed (`/ws`) pushes new usage records to connected dashboards.
- **External Ingestion** — POST `/ingest` endpoint plus adapter modules for Hermes, GitHub, Telegram, OpenRouter.
- **Docker Compose** — One-command deployment behind an Nginx reverse proxy.

## Quick Start

Prerequisites: Docker Engine running (the daemon must be up before `docker compose up`).

```bash
git clone https://github.com/OneByJorah/CostForge.git
cd CostForge

cp .env.example .env  # Optional: adjust paths
docker compose up -d
```

Open **http://localhost:8090** in your browser. The backend API is also reachable directly on **http://localhost:8000** (the dashboard is served there too).

### Local Development

Requires Python 3.10+.

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Then open http://localhost:8000 — the backend serves the dashboard itself. (The `frontend/dist/index.html` SPA is what gets served; Nginx serves it directly in the Docker deployment.)

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `COSTFORGE_DB` | `<backend>/costforge.db` | SQLite database path |
| `COSTFORGE_LOG` | `<backend>/usage.jsonl` | Usage log path |
| `COSTFORGE_ENDPOINT` | `http://127.0.0.1:17890/ingest` | Ingest target used by adapter modules |
| `COSTFORGE_GITHUB_DEFAULT_MODEL` | `github/api` | Default model label for GitHub adapter events |

Provider credentials (Groq keys, Gemini `?key=`, etc.) are passed through the proxy untouched by your clients — CostForge never stores them. See `.env.example` for deployment path overrides.

## Architecture

```
Browser ──▶ Nginx (port 8090) ──▶ FastAPI Backend (port 8000)
                                        │
                        ┌───────────────┼───────────────┐
                        ▼               ▼               ▼
              /proxy/* metering    SQLite (WAL)   JSON catalogs
              to configured        usage records  providers.json
              providers            + events       pricing.json
                        │
                        ▼
             WebSocket live feed (/ws)
```

## Tech Stack

- **Backend**: FastAPI + uvicorn + httpx (Python 3.10+)
- **Database**: SQLite (WAL mode)
- **Frontend**: Vanilla JavaScript SPA (dark theme, no build step)
- **Reverse Proxy**: Nginx
- **Deployment**: Docker Compose

## Supported Providers

Configured in [`backend/providers.json`](backend/providers.json):

| Provider | Type | Proxy Prefix |
|----------|------|--------------|
| Ollama | local | `/proxy/ollama` |
| LM Studio | local | `/proxy/lmstudio` |
| vLLM | local | `/proxy/vllm` |
| Headroom | local | `/proxy/headroom` |
| Groq (free tier) | cloud-free | `/proxy/groq` |
| OpenRouter (free models) | cloud-free | `/proxy/openrouter` |
| Google Gemini (free tier) | cloud-free | `/proxy/gemini` |
| Hugging Face Inference (free tier) | cloud-free | `/proxy/hf` |

Premium baselines (GPT-4o family, Claude family, Gemini family) are priced per million tokens in [`backend/pricing.json`](backend/pricing.json). Prices change — re-verify before relying on them for real budgeting.

## Project Structure

```
CostForge/
├── backend/
│   ├── main.py              # FastAPI app: proxy, metering, API, WebSocket, DB
│   ├── providers.json       # Provider definitions (Ollama, Groq, ...)
│   ├── pricing.json         # Premium API pricing catalog
│   ├── seed_demo.py         # Demo data seeder
│   ├── Dockerfile           # Python 3.12-slim, non-root user
│   ├── requirements.txt     # fastapi, uvicorn[standard], httpx
│   └── ingest/              # Adapter modules (hermes, github, telegram, openrouter)
├── frontend/
│   └── dist/
│       └── index.html       # Single-file SPA dashboard
├── pricing/
│   └── catalog.json         # Pricing catalog (mirror of backend/pricing.json)
├── scripts/
│   ├── healthcheck.sh       # Shell health check for both services
│   └── capture-screenshots.py
├── docs/
│   └── screenshots/         # Dashboard screenshots
├── docker-compose.yml       # Backend + nginx frontend
├── nginx.conf               # Reverse proxy config
└── .env.example             # Configuration template
```

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard SPA |
| `/proxy/{provider}/{path}` | any | Metering reverse proxy to a configured provider |
| `/api/stats` | GET | Totals + per-provider aggregates |
| `/api/recent` | GET | Recent usage rows (`?limit=N`, max 500) |
| `/api/timeseries` | GET | Per-minute cost/request buckets (`?rangeMinutes=N`) |
| `/api/providers` | GET | Configured providers |
| `/api/pricing` | GET | Premium pricing catalog |
| `/api/usage` | GET | Raw usage rows (`?days=N`) |
| `/api/summary` | GET | Grouped summary (`?days=N`) |
| `/api/health`, `/healthz` | GET | Health checks |
| `/ws` | WebSocket | Live usage feed |
| `/ingest` | POST | Push a usage record from external adapters |

Interactive docs: `/docs` (Swagger UI) and `/redoc` via FastAPI.

## Contributing

Contributions are welcome. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community standards.

## Security

Found a vulnerability? Please follow our [Security Policy](SECURITY.md) and report privately to `security@jorahone.com` — do not use public issues.

## License

[MIT License](LICENSE) © Jhonattan L. Jimenez (OneByJorah)

---

<p align="center">Built with 🌴 by <a href="https://github.com/OneByJorah">OneByJorah</a> · <a href="https://jorahone.com">jorahone.com</a></p>
