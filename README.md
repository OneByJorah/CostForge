# CostForge — Cloud Cost Dashboard

**Version:** v1.0  
**Status:** Active Development  
**Repository:** https://github.com/OneByJorah/CostForge

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Features](#features)
- [Getting Started](#getting-started)
- [Service Management](#service-management)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Overview

CostForge is a cloud cost estimation and pricing dashboard spun out of the J1 NOC Platform UI. It aggregates pricing catalogs, ingests usage data, and presents cost breakdowns through a dark-themed frontend.

Built for operators who need quick visibility into cloud spend without leaving their internal tooling.

---

## Architecture

Client → FastAPI backend (`backend/main.py`) → ingest adapters (Hermes, OpenRouter, Telegram) → pricing catalog (`pricing/catalog.json`) → frontend (`frontend/dist/index.html`).

Data flow:
- Ingest adapters normalize external cost signals into a common format.
- `backend/seed_demo.py` populates sample data for development.
- Dashboard renders as a static single-page app from the built frontend.

---

## Technology Stack

| Layer | Stack |
|---|---|
| Runtime | Linux (Ubuntu 22.04+) |
| Backend | Python / FastAPI |
| Frontend | Static HTML5 Dashboard |
| Integrations | Hermes adapter, OpenRouter adapter, Telegram adapter |
| Data | JSON catalog + seeded demo data |
| VCS | Git + GitHub (`github.com/OneByJorah/CostForge`) |

---

## Features

- **Pricing catalog**: JSON-backed service pricing (`pricing/catalog.json`).
- **Ingest adapters**:
  - Hermes adapter
  - OpenRouter adapter
  - Telegram adapter
- **Demo seeding**: `backend/seed_demo.py` for quick local previews.
- **Static frontend build**: production-ready HTML output in `frontend/dist/`.

---

## Getting Started

```bash
# 1. Clone
git clone https://github.com/OneByJorah/CostForge.git
cd CostForge

# 2. Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # or install fastapi uvicorn as needed

# 3. Seed demo data (optional)
python seed_demo.py

# 4. Run backend
uvicorn main:app --host 0.0.0.0 --port 8000

# 5. Serve frontend (in another terminal)
cd frontend/dist
python -m http.server 8080
```

Visit `http://localhost:8080`.

---

## Service Management

```bash
# Quick start backend
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# Quick start frontend
cd frontend/dist && python -m http.server 8080
```

---

## Project Structure

```
CostForge/
├── backend/
│   ├── main.py
│   ├── seed_demo.py
│   └── ingest/
│       ├── hermes_adapter.py
│       ├── openrouter_adapter.py
│       └── telegram_adapter.py
├── frontend/
│   └── dist/
│       └── index.html
├── pricing/
│   └── catalog.json
└── docs/screenshots/
    └── costforge-dashboard.png
```

---

## Screenshots

### CostForge Dashboard
![CostForge Dashboard](docs/screenshots/costforge-dashboard.png)

---

## Contributing

1. Create a feature branch off `main`.
2. Keep pricing catalog changes backward-compatible.
3. Submit a PR with description and screenshots for UI changes.

---

## License

MIT

---

## Author

Built by **Jhonattan L. Jimenez**.
