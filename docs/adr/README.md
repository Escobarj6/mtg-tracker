# Architecture Decision Records

Each file records one decision: the situation, what was chosen, the alternatives,
and the consequences. They explain *why* the project is built the way it is.

## Rules

- Numbered in order and never rewritten. If a decision changes, write a new ADR
  that supersedes the old one, and mark the old one `Superseded by NNNN`.
- Start new records from [0000-template.md](0000-template.md).

## Index

| #    | Decision |
|------|----------|
| [0001](0001-store-color-identity-as-a-bitmask.md) | Store color identity as a bitmask |
| [0002](0002-use-a-monorepo.md) | Use a monorepo with `backend/` and `frontend/` |
| [0003](0003-use-sql-server-and-sqlite-only-in-tests.md) | Use SQL Server for the app and SQLite only in tests |
| [0004](0004-use-uv-for-python-tooling.md) | Use uv for Python versions and dependencies |
| [0005](0005-configure-through-environment-variables.md) | Configure through environment variables |
| [0006](0006-inject-settings-and-engine-as-dependencies.md) | Inject settings and the engine as dependencies |
| [0007](0007-use-sync-endpoints-with-a-blocking-driver.md) | Use sync endpoints with a blocking database driver |
| [0008](0008-use-surrogate-keys.md) | Use surrogate keys, with Scryfall IDs as unique columns |
| [0009](0009-store-finishes-as-booleans.md) | Store finishes as booleans |
| [0010](0010-name-constraints-with-a-naming-convention.md) | Name constraints with a naming convention |
| [0011](0011-manage-schema-changes-with-alembic.md) | Manage schema changes with Alembic |
