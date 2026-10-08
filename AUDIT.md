# CostForge — Audit (2026-10-08, Stage 1-2)

Baseline recorded before any change. Every claim below was produced by a command run
locally against a clean clone; nothing here is inferred from reading alone.

## Baseline

| Check | Result |
|---|---|
| Clone | clean, `main`, working tree clean at start |
| Stack | FastAPI 0.115.0 + uvicorn 0.32.0 + httpx 0.28.1, SQLite (WAL), single `backend/main.py` (597 lines) |
| Dependency count | 3 runtime (genuinely zero-dependency beyond FastAPI stack) |
| Import | `import main` → OK, `app` is a FastAPI instance, **17 routes** |
| Runtime | `uvicorn main:app --host 127.0.0.1 --port 8099` → started |
| `GET /healthz` | **200** `{"ok":true,...}` |
| `GET /api/health` | **200**, reports provider count 8 |
| `GET /api/stats`, `/api/summary`, `/api/recent`, `/api/timeseries` | **200**, correct shapes |
| `GET /` (dashboard) | **500** ← defect, see A1 |
| Tests in repo | **none** (no `tests/`, no pytest config) |
| `gitleaks detect` | clean — 35 commits scanned, no leaks |

## Findings

### A1 — Documented dashboard 500s on a clean clone (fixed)
`backend/main.py:533-535` serves the SPA by reading
`APP_DIR.parent / "frontend" / "dist" / "index.html"`, which raises `FileNotFoundError`
when `frontend/` is absent → HTTP 500 on `/`.

`frontend/` **does not exist in the repository at all**. The same commit that wrote the
README claims (`7532072 "docs: trending README, real screenshots…"`) deleted
`frontend/dist/index.html`; it was tracked at `9717a4c` and earlier.

Two shipped files depend on a path that is not in the repo:
- `Dockerfile.frontend` → `COPY ./frontend/dist /usr/share/nginx/html`
- `docker-compose.yml` → `costforge-frontend` service

So both the documented local quick start (`docker compose up -d`) and the plain
`uvicorn` route were broken from a fresh clone.

**Fix:** restored `frontend/dist/index.html` from `9717a4c` (self-contained single-file
SPA, 12,625 bytes, no external assets). Verified `GET /` → **200**, correct `<title>`,
and the page's fetch calls target only endpoints that exist
(`/api/pricing`, `/api/providers`, `/api/recent`, `/api/stats`, `/api/timeseries`).

### A2 — `.gitignore` silently dropped the restored file (fixed)
`.gitignore` line 18 ignored `dist/`. A restored frontend would therefore never be
committed, re-breaking A1 on the next clone. Added an explicit
`!frontend/dist/` + `!frontend/dist/**` exception, keeping `dist/` ignored for any
genuine build output.

### A3 — Runtime database artifacts unignored (fixed)
`backend/costforge.db`, `-shm`, `-wal` are created at runtime and were untracked and
unignored — easy to commit by accident. Added to `.gitignore`.

### A4 — No tests (delegated)
Zero automated tests existed. Delegated a real pytest suite for the API surface and the
usage-parsing helpers to OpenCode (free model). Status recorded in the daily note.

## Not verified (honest gaps)
- **No Docker on this host** → `Dockerfile.frontend`, `docker-compose.yml` and the
  container install path were **not** exercised. Only the direct `uvicorn` path was.
- **No real proxied traffic** → the metering path (`/proxy/{provider}/{path}`) and
  WebSocket feed were not exercised end-to-end; `/api/*` reads were verified against an
  empty store.
- Screenshots of the CostForge dashboard have **not** been captured yet (the existing
  `docs/screenshots/*.png` are pre-existing and were not re-verified in this run).
