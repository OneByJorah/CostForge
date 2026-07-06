<!-- j1-brand:v2 -->
<div align="center">

# CostForge

A self-hosted dashboard for estimating and tracking cloud and LLM API usage costs — multi-provider aggregation, cost comparison, and ingestion adapters, all with zero external dependencies.

[![GitHub](https://img.shields.io/badge/github-OneByJorah%2FCostForge-FFB300?style=for-the-badge&labelColor=0d0d0c)](https://github.com/OneByJorah/CostForge)
[![License](https://img.shields.io/badge/license-MIT-FFB300?style=for-the-badge&labelColor=0d0d0c)](LICENSE)
[![Language](https://img.shields.io/badge/Python-FFB300?style=for-the-badge&labelColor=0d0d0c)](https://python.org)
[![Built by](https://img.shields.io/badge/built%20by-JorahOne%20LLC-FFB300?style=for-the-badge&labelColor=0d0d0c)](https://github.com/OneByJorah)

</div>

---

## Why This Exists

API costs from LLMs, cloud services, and third-party APIs can spiral before you notice. CostForge gives you a self-hosted dashboard to track usage across providers, compare pricing models, and ingest cost data through normalized adapters — no external analytics service required.

## Key Features

| Feature | Why It Matters |
|---|---|
| Multi-provider aggregation | Track costs from LLMs, cloud APIs, and SaaS tools in one place |
| Cost comparison | Side-by-side pricing views for different providers and models |
| Normalized ingestion adapters | Standardized format for any provider's usage data |
| SQLite storage | Zero-config database — no PostgreSQL or external DB to manage |
| Dark-themed UI | Easy on the eyes for your ops dashboard |

## Quick Start

```bash
git clone https://github.com/OneByJorah/CostForge.git
cd CostForge
docker compose up -d
```

## Architecture

```
┌──────────┐     ┌──────────────┐     ┌──────────┐
│  Browser  │────▶│  FastAPI      │────▶│  SQLite   │
│  (UI)     │     │  Backend      │     │  (Data)   │
└──────────┘     └──────┬───────┘     └──────────┘
                         │
                  ┌──────▼───────┐
                  │  JSON        │
                  │  Pricing     │
                  │  Catalog     │
                  └──────────────┘
```

## Documentation

| Doc | Description |
|---|---|
| [Setup Guide](docs/setup.md) | Deployment and configuration |
| [API Reference](docs/api.md) | Usage ingestion and query endpoints |

---

## License

MIT © JorahOne, LLC — see [LICENSE](LICENSE)

<sub>Part of the JorahOne infrastructure ecosystem.</sub>
