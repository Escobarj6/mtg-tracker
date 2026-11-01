# Security Setup

How this repository is secured, and why. Every setting can be reapplied with
the `gh` commands below (replace `OWNER/REPO`).

## Branch protection: ruleset "Protect main"

All changes to `main` go through a pull request, and CI must pass first.
Nobody can bypass it, including the repository owner.

| Rule | Purpose |
|---|---|
| Pull request required | No direct pushes to `main` |
| Required check `Backend lint and tests` | CI must pass before merging |
| Check pinned to GitHub Actions (`integration_id: 15368`) | Another app or token can't fake a passing check |
| Branch must be up to date (`strict`) | Tests ran against the latest `main` |
| Squash merges only, linear history | One clean commit per PR |
| Force pushes and deletion blocked | History on `main` can't be rewritten or removed |
| No bypass actors | Rules apply to admins too; limits damage from a compromised account or token |

Verified by attempting a direct push to `main`, which GitHub rejected.

## GitHub Actions

- **Default workflow token is read-only**, and workflows can't approve pull requests.
- **The CI workflow declares `permissions: contents: read`** and checks out without persisting credentials.
- **Actions are pinned to full commit SHAs**, not tags. A tag can be moved to malicious
  code; a commit SHA can't. (In 2025, `tj-actions/changed-files` was compromised this way.)
- **Workflows from first-time and external contributors require approval** before running.

```bash
gh api -X PUT repos/OWNER/REPO/actions/permissions/workflow \
  -f default_workflow_permissions=read \
  -F can_approve_pull_request_reviews=false
```

## Secret protection

- **Secret scanning** and **push protection**: pushes containing known credential
  formats are rejected before they reach the repository.
- **`.env` is gitignored**; `.env.example` documents variable names with placeholders.
- History audited with [gitleaks](https://github.com/gitleaks/gitleaks) before the
  repository went public: no secrets found.

```bash
gh api -X PATCH repos/OWNER/REPO --input - <<'JSON'
{"security_and_analysis": {
  "secret_scanning": {"status": "enabled"},
  "secret_scanning_push_protection": {"status": "enabled"}
}}
JSON
```

## Dependencies

- **Dependabot alerts and security updates**: vulnerable packages are flagged, and fix PRs
  are opened automatically, which CI then tests.
- **`uv.lock`** pins exact versions; CI installs with `uv sync --locked` and fails if the
  lockfile is out of date.

```bash
gh api -X PUT repos/OWNER/REPO/vulnerability-alerts
gh api -X PUT repos/OWNER/REPO/automated-security-fixes
```

## Vulnerability reporting

Private vulnerability reporting is enabled. See [SECURITY.md](../SECURITY.md).

```bash
gh api -X PUT repos/OWNER/REPO/private-vulnerability-reporting
```

## Account security

The repository is only as secure as the owner's GitHub account, which can change
any of the settings above.

- Two-factor authentication, preferably a passkey or hardware security key
- SSH key with a passphrase; unused keys removed
- Authorized apps and personal access tokens reviewed periodically

## Application security

- Configuration from environment variables; the database password is required and
  wrapped in `SecretStr` so it never appears in logs or output.
- Database errors are logged server-side; clients only see a generic message.
- The local SQL Server container is bound to `127.0.0.1` only. Docker's port publishing
  bypasses `ufw`, so binding to all interfaces would expose it to the network.

### Known gaps (planned)

- The app connects as `sa`; it will move to a least-privilege database login.
- Azure deployment will use managed identity instead of a database password.
