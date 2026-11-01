# 0003. Use SQL Server for the app and SQLite only in tests

- **Status:** Accepted
- **Date:** 2026-10-22

## Context

Production will run on Azure SQL, which is SQL Server. The target team uses SQL
Server in production and SQLite for some local development.

SQL Server and SQLite differ in ways that matter: SQL dialect (pagination, string
and date functions), type strictness, schema-change support, and the driver setup
(Python reaches SQL Server through pyodbc and Microsoft's ODBC driver).

## Decision

- Run the app locally against **SQL Server 2025 in Docker**, matching production.
- Use **SQLite only in tests**, swapped in through FastAPI dependency overrides, so
  tests need no server, `.env`, or network.

## Alternatives considered

- **SQLite for local development:** zero setup, but bugs that only appear on SQL
  Server would surface late, in staging or production.
- **SQL Server in tests too:** the most rigorous option, but it requires a database
  service in CI. Revisit when tests start exercising real queries.

## Consequences

- Local behavior matches production, including the ODBC driver path.
- Local setup needs Docker and the ODBC driver (documented in the README).
- Current tests only check connectivity, where SQLite and SQL Server behave the same.
  Tests of real queries may need SQL Server in CI to stay trustworthy.
- A SQLite option for everyday development may still be added to match the team's
  workflow; it would be a configuration change, not a code change.
