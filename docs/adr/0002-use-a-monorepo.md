# 0002. Use a monorepo with `backend/` and `frontend/`

- **Status:** Accepted
- **Date:** 2026-10-22

## Context

The project has a FastAPI backend and a planned Aurelia 2 frontend. They change
together: a new feature usually touches the API and the page that uses it.

## Decision

Keep both in one repository, in `backend/` and `frontend/` folders, with shared
files (CI workflows, docs, README) at the root.

## Alternatives considered

- **Separate repositories:** better when separate teams own each piece and release
  independently. For one developer, it means two PRs for one feature and keeping
  versions in sync by hand.

## Consequences

- One PR can change the API and the frontend together, reviewed as one unit.
- CI and docs live in one place.
- Commands must run from the right folder: uv and Ruff from `backend/`, Git from
  the repository root.
- CI needs per-folder jobs (`working-directory: backend`) as each part gets its own tooling.
