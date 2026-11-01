# 0005. Configure through environment variables

- **Status:** Accepted
- **Date:** 2026-10-22

## Context

The app needs a database host, name, user, and password. Values differ between a
laptop, CI, staging, and production, and the password is a secret. A secret
committed to Git stays in history forever, and public repositories are scanned by
bots within minutes.

## Decision

Load configuration from environment variables with **pydantic-settings**, following
the Twelve-Factor App approach:

- Every variable uses the `MTG_` prefix, so names can't collide with other programs.
- `backend/.env` is a local fallback; it is gitignored. `.env.example` documents the
  variable names with placeholder values.
- Real environment variables take priority over `.env`.
- The database password has no default, so the app refuses to start without it.
- The password is a `SecretStr`, which prints as `**********` in logs and output.
- Insecure options default to secure values (`MTG_DB_TRUST_SERVER_CERTIFICATE`
  defaults to `false`); only local `.env` files relax them.

## Alternatives considered

- **Hard-coded values:** leaks secrets and requires code changes per environment.
- **A committed config file per environment:** still puts secrets in the repository
  unless they are stored separately anyway.

## Consequences

- No secrets in code or history; each environment supplies its own values.
- Misconfiguration fails fast at startup with a clear validation error.
- Type hints validate values, for example `MTG_DB_PORT` must be a number.
- In Azure, these become app settings, and the password can later be replaced by
  managed identity.
