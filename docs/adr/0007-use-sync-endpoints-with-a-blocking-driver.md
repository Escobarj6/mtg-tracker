# 0007. Use sync endpoints with a blocking database driver

- **Status:** Accepted
- **Date:** 2026-10-22

## Context

FastAPI supports both `async def` and plain `def` endpoints. `async def` endpoints
run on a single event loop that serves many requests at once, but only if code
inside never blocks. pyodbc, the SQL Server driver, is blocking: it waits on the
database and holds the thread while it does.

## Decision

Write endpoints that touch the database as plain `def`. FastAPI runs them in a
worker thread pool, so a slow query blocks only its own thread.

## Alternatives considered

- **`async def` with pyodbc:** one slow query would freeze every other request.
- **An async SQL Server driver:** options are less mature than pyodbc, and the
  target team's stack uses synchronous SQLModel.

## Consequences

- Blocking calls are safe; concurrency comes from the thread pool.
- The thread pool (about 40 threads by default) is larger than SQLAlchemy's default
  connection pool (5, plus 10 overflow). Under heavy load, requests wait for a free
  connection and fail after 30 seconds. Pool sizes become settings if load requires it.
- Rule of thumb: blocking libraries go in `def`; only fully async code goes in `async def`.
