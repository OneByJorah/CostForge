# CostForge

> Self-hosted cost-observability proxy for local and free-tier LLMs that meters every request and prices it against premium-model rates so you can quantify what the free traffic would have cost.

[![License](https://img.shields.io/github/license/OneByJorah/CostForge?style=for-the-badge&color=FFB300&labelColor=0a0a09)](https://github.com/OneByJorah/CostForge)
[![Top Language](https://img.shields.io/github/languages/top/OneByJorah/CostForge?style=for-the-badge&color=FFB300&labelColor=0a0a09)](https://github.com/OneByJorah/CostForge)
[![Stars](https://img.shields.io/github/stars/OneByJorah/CostForge?style=for-the-badge&color=FFB300&labelColor=0a0a09)](https://github.com/OneByJorah/CostForge/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/OneByJorah/CostForge?style=for-the-badge&color=FFB300&labelColor=0a0a09)](https://github.com/OneByJorah/CostForge/commits)
[![CodeQL](https://img.shields.io/github/actions/workflow/status/OneByJorah/CostForge/codeql.yml?style=for-the-badge&color=FFB300&labelColor=0a0a09&label=codeql)](https://github.com/OneByJorah/CostForge/actions/workflows/codeql.yml)

![CostForge dashboard](docs/screenshots/costforge-dashboard.png)

## What This Is

CostForge sits in front of your local models (Ollama, LM Studio, vLLM) and free-tier APIs (Groq, Gemini free, Hugging Face) as a transparent HTTP reverse proxy. Every proxied request is priced against a premium-model catalog and stored alongside token counts, so you can see the volume and commercial value of the traffic your local stack absorbed. Point a client at the proxy URL and metering kicks in automatically — no SDK, no instrumentation.

## Quick Start

```bash
git clone https://github.com/OneByJorah/CostForge.git
cd CostForge
cp .env.example .env
docker compose up -d
```

Open **http://localhost:8090** for the dashboard; the backend API listens on **http://localhost:8000**.

## Features

- Zero-friction metering via `/proxy/<provider>` passthrough — no client code changes.
- Premium-equivalence costing (e.g. `llama3.1:8b` → `gpt-4o-mini`) priced from `pricing/catalog.json`.
- Live WebSocket feed broadcasting usage records to the dashboard with reconnect.
- Provider catalog covering Ollama, LM Studio, vLLM, Headroom, Groq, OpenRouter free, Gemini free, and Hugging Face.
- External ingestion adapters (Hermes, GitHub, Telegram, OpenRouter) pushing non-proxied usage into the same store via `POST /ingest`.
- Time-series analytics: per-source breakdowns, token splits, sparklines, recent-request views.
- SQLite with WAL persisted in a Docker volume — zero external dependencies.
- Non-root backend container with healthchecks.

## Architecture

```
Browser ──▶ nginx (port 8090) ──▶ FastAPI backend (port 8000)
                                     │
                            ┌────────┴────────┐
                            ▼                 ▼
                       SQLite (usage)   JSON catalogs
                            │            (providers, pricing)
                            ▼
                  WebSocket live feed (/ws)
```

The frontend is a pre-built static SPA served by nginx, which also proxies `/api/`, `/ingest`, `/proxy/`, and `/ws` to the backend.

## Stack

Python 3.12 · FastAPI · uvicorn · httpx · SQLite (WAL) · nginx · vanilla JS SPA · Docker Compose · CodeQL.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). [Open an issue](https://github.com/OneByJorah/CostForge/issues) to report a bug or request a provider adapter.

## License

MIT — see [LICENSE](LICENSE).
