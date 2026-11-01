# 0004. Use uv for Python versions and dependencies

- **Status:** Accepted
- **Date:** 2026-10-22

## Context

The project needs a specific Python version, an isolated environment, and
reproducible installs across a laptop, CI, and eventually a container.
Traditionally that takes several tools: pyenv for Python versions, venv for
environments, and pip with a requirements file for packages.

## Decision

Use **uv** for all of it: `uv init`, `uv add`, `uv sync`, and `uv run`.
The Python version is pinned in `.python-version`, dependencies are declared in
`pyproject.toml`, and exact versions are locked in `uv.lock`.

## Alternatives considered

- **pip + venv + pyenv:** standard and widely known, but three tools, slower installs,
  and no lockfile without extra tooling.
- **Poetry:** a mature all-in-one tool, but slower, and it doesn't manage Python
  versions itself.

## Consequences

- One fast tool; uv downloads the right Python version itself.
- `uv.lock` makes installs reproducible. CI runs `uv sync --locked`, which fails if
  the lockfile is out of date with `pyproject.toml`.
- The system Python is never touched.
- After switching branches with different dependencies, run `uv sync` so `.venv`
  matches; `uv run` syncs automatically, but editors like Pylance read `.venv` directly.
