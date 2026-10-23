# MTG Tracker

A Magic: The Gathering collection tracker built on a modern Python and TypeScript stack:
FastAPI, SQL Server, and Aurelia 2, deployed to Azure.

> **Status:** early development. The backend API and database connection are working.
> See the [roadmap](#roadmap) for what's next.

## Stack

| Layer      | Technology                                          |
|------------|-----------------------------------------------------|
| API        | Python 3.13, FastAPI, SQLAlchemy, pyodbc            |
| Database   | SQL Server 2025 (Docker locally, Azure SQL in cloud)|
| Frontend   | Aurelia 2, TypeScript *(planned)*                   |
| Tooling    | uv, Ruff, pytest, Docker                            |
| Cloud      | Azure, defined as infrastructure as code *(planned)*|

## Prerequisites

Tested on Ubuntu 22.04 (x86_64).

- **Docker**, with your user in the `docker` group
- **[uv](https://docs.astral.sh/uv/)** for Python versions and dependencies
- **Microsoft ODBC Driver 18 for SQL Server** (`msodbcsql18`)
- A SQL client: the VS Code **SQL Server (mssql)** extension works well

## Getting started

### 1. Clone the repository

```bash
git clone git@github.com:Escobarj6/mtg-tracker.git
cd mtg-tracker
```

### 2. Start SQL Server

Set a strong `sa` password without saving it to shell history:

```bash
read -rs MSSQL_SA_PASSWORD && export MSSQL_SA_PASSWORD
```

Start the container, bound to localhost only, with a named volume so data survives container removal:

```bash
docker run -d --name mtg-sql \
  -e ACCEPT_EULA=Y -e MSSQL_SA_PASSWORD \
  -p 127.0.0.1:1433:1433 \
  -v mtg-sql-data:/var/opt/mssql \
  mcr.microsoft.com/mssql/server:2025-latest
```

Wait about 20 seconds for startup, then connect with your SQL client
(server `127.0.0.1`, port `1433`, user `sa`, trust server certificate) and run:

```sql
CREATE DATABASE mtg;
```

### 3. Configure the backend

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` and set `MTG_DB_PASSWORD` to your `sa` password.
`.env` is gitignored and must never be committed.

### 4. Run the API

```bash
cd backend
uv sync
uv run fastapi dev src/mtg_api/main.py
```

- Health check: <http://127.0.0.1:8000/health> returns `{"status": "ok", "database": "ok"}`
- Interactive API docs: <http://127.0.0.1:8000/docs>

## Configuration

Settings load from environment variables, with `backend/.env` as a local fallback.
Real environment variables take priority.

| Variable                          | Default     | Notes                                   |
|-----------------------------------|-------------|-----------------------------------------|
| `MTG_DB_PASSWORD`                 | *(required)*| App refuses to start without it         |
| `MTG_DB_HOST`                     | `127.0.0.1` | IPv4 on purpose (see troubleshooting)   |
| `MTG_DB_PORT`                     | `1433`      |                                         |
| `MTG_DB_NAME`                     | `mtg`       |                                         |
| `MTG_DB_USER`                     | `sa`        | Local development only                  |
| `MTG_DB_TRUST_SERVER_CERTIFICATE` | `false`     | Set `true` locally for the self-signed container cert. Never in production. |

## Development workflow

- Work on a branch (`feat/...`, `fix/...`, `docs/...`), never directly on `main`.
- Before committing, from `backend/`:
```bash
  uv run ruff format .
  uv run ruff check .
```
- Open a pull request with what changed, why, and how it was tested, then squash-merge.

## Project layout

```
mtg-tracker/
├── backend/
│   ├── src/mtg_api/
│   │   ├── config.py     # settings loaded from environment
│   │   ├── db.py         # SQLAlchemy engine and connection URL
│   │   └── main.py       # FastAPI app and routes
│   ├── .env.example      # template for local configuration
│   ├── pyproject.toml    # project metadata and dependencies
│   └── uv.lock           # exact, reproducible dependency versions
└── README.md
```

## Troubleshooting

**`/health` returns 503 with `Login timeout expired (HYT00)` in the server log**

The driver can't reach SQL Server. Check the container is running (`docker ps`).
If it is, make sure `MTG_DB_HOST` is `127.0.0.1` and not `localhost`: `localhost` can
resolve to IPv6 `::1`, where the container isn't listening.

**`permission denied` connecting to the Docker socket**

Add your user to the `docker` group (`sudo usermod -aG docker $USER`), then log out
and back in. A new terminal isn't enough; group membership is set at login.

## Roadmap

- [x] FastAPI backend with SQL Server connectivity and health check
- [ ] Database schema and migrations (Alembic)
- [ ] Card data from the Scryfall API
- [ ] Collection and deck endpoints
- [ ] Aurelia 2 frontend
- [ ] Tests and CI with GitHub Actions
- [ ] Docker Compose and dev container
- [ ] Azure deployment with infrastructure as code
- [ ] Architecture decision records