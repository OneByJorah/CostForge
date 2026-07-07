<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white">
  <img src="https://img.shields.io/badge/license-MIT-blue?style=for-the-badge">
</div>

<br>

<div align="center">
  <h1>💰 CostForge</h1>
  <p><strong>Self-Hosted Cloud &amp; API Cost Estimation Dashboard</strong></p>
  <p>Track, compare, and estimate cloud/LLM API usage costs with zero external dependencies</p>
  <p>
    <a href="#-features">Features</a> •
    <a href="#-quick-start">Quick Start</a> •
    <a href="#-architecture">Architecture</a> •
    <a href="#-pricing">Pricing</a>
  </p>
</div>

---

## 📸 Screenshot

This is a CLI/backend-only tool. No screenshots available.

## ✨ Features

- **Multi-Provider Cost Aggregation** — Compare pricing across cloud and LLM providers
- **Self-Hosted** — Zero external dependencies, zero secrets in git
- **Usage Ingestion** — Adapters normalize incoming cost/usage signals
- **Dark Dashboard** — Production-ready dark-themed single-page dashboard
- **Local Storage** — SQLite for usage data, JSON for pricing catalogs
- **Cost Comparison** — Compare self-hosted vs premium API pricing
- **REST API** — Programmatic access to cost data
- **Docker Deploy** — One-command deployment

## 🚀 Quick Start

```bash
git clone https://github.com/OneByJorah/CostForge.git
cd CostForge
docker compose up -d
```

Open **http://localhost:8080** in your browser.

## 🏗️ Architecture

```
┌──────────────────────────────────────────────┐
│                 CostForge                     │
│                                               │
│  Browser ──▶ Nginx ──▶ FastAPI Backend        │
│                            │                   │
│                    ┌───────┴───────┐           │
│                    ▼               ▼           │
│              ┌──────────┐   ┌──────────┐     │
│              │  SQLite  │   │   JSON   │     │
│              │  Usage   │   │ Pricing  │     │
│              │  Data    │   │ Catalog  │     │
│              └──────────┘   └──────────┘     │
└──────────────────────────────────────────────┘
```

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard UI |
| `/api/costs` | GET | Usage cost data |
| `/api/pricing` | GET | Provider pricing catalog |
| `/api/compare` | GET | Cost comparison data |
| `/api/ingest` | POST | Ingest usage data |

## 📁 Project Structure

```
CostForge/
├── backend/              # FastAPI backend server
├── frontend/             # SPA frontend
├── pricing/              # Pricing catalog data
├── scripts/              # Utility scripts
├── docs/                 # Documentation
├── docker-compose.yml    # Docker deployment
├── nginx.conf            # Reverse proxy config
└── stack_manifest.json   # Stack metadata
```

## 📄 License

MIT © Jhonattan L. Jimenez

---

<div align="center">
  <p>📊 Know your cloud costs — self-hosted</p>
  <p><a href="https://github.com/OneByJorah">@OneByJorah</a></p>
</div>
