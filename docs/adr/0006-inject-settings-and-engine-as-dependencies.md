# 0006. Inject settings and the engine as dependencies

- **Status:** Accepted
- **Date:** 2026-11-01

## Context

Settings and the database engine were originally created at import time
(`settings = Settings()`, `engine = create_engine(...)`). Importing any module
therefore read `.env` and required a password. Tests could not swap in a different
database, and CI, which has no `.env`, could not even import the app.

## Decision

- Replace the globals with `get_settings()` and `get_engine()`, each wrapped in
  `@lru_cache` so the app still has exactly one settings object and one engine
  (and therefore one connection pool), created on first use.
- Endpoints declare what they need with FastAPI dependencies:
  `engine: Annotated[Engine, Depends(get_engine)]`.
- `build_url()` takes `Settings` as an argument instead of reading a global.
- Endpoints live in `routers/`; `main.py` only creates the app and includes routers.

## Alternatives considered

- **Module-level globals:** simple, but untestable without patching, and importing
  has side effects.
- **Patching globals in tests (`monkeypatch`):** works, but couples tests to internal
  names and is easy to leak between tests.

## Consequences

- Importing the app has no side effects; CI runs without `.env` or a database.
- Tests replace dependencies through `app.dependency_overrides`, cleared after each
  test by the `client` fixture.
- Functions that receive their inputs as arguments, like `build_url(settings)`, can
  be tested directly.
- Database sessions for future endpoints will follow the same pattern.
