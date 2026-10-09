# Changelog

## [1.1.0] - 2026-10-09
### Fixed
- **The dashboard fabricated a phantom metered request on every page load.** The
  WebSocket greeting sent a message typed `usage` with a stub `{ts}` payload, which the
  client counted as a real request — showing "1 requests metered" with
  `source: undefined` against an empty database. The greeting now uses its own message
  type. Verified: the UI, `/api/stats` and the SQLite table now agree.
- **The dashboard returned HTTP 500 on a clean clone.** `frontend/` was missing from the
  repository although `backend/main.py` reads `frontend/dist/index.html` and
  `Dockerfile.frontend` copies it. The prebuilt SPA is restored and explicitly
  un-ignored so it ships.
- **`/` and the container healthchecks could never pass.** The compose frontend
  healthcheck probed an internal port nothing listened on; the frontend image ran as
  root. Both corrected — nginx now serves on 8080 as an unprivileged user.
- Backend image could not build (`libssl3t64` conflict); apt removed entirely since every
  dependency ships a wheel.

### Added
- Backend test suite (8 tests) covering the API surface, the ingest path and the
  usage-parsing helpers, with the database isolated per test session.
- Real dashboard screenshots in `docs/media/` captured from the running stack.

### Changed
- Deprecated `datetime.utcnow()` replaced (format-preserving, so stored timestamps and
  range queries are unaffected).
- `gen.py` (portal) now honours the documented `GITHUB_TOKEN`.

## [1.0.0] - 2026-07-07
### Added
- Initial release
- Dockerfile improvements (backend, frontend)
- docker-compose.yml with healthchecks
- .env.example with placeholder values
