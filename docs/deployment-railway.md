# Railway Deployment

This deployment serves the proof-pack MVP as a static, read-only site on Railway.

## Scope

- Static proof pack and dashboard only.
- Read-only and dry-run only.
- No wallet, signer, custody, private-key, live transaction, or capital-deployment surface.
- Do not expose local `.env` values in the public container.

## Architecture

Railway builds the repository with the checked-in `Dockerfile`. The container uses `nginx:1.27-alpine` and listens on Railway's injected `PORT` variable via `deploy/railway/nginx.conf.template`.

The public container includes only reviewer-facing static assets:

- `index.html`
- `apps/`
- `datasets/`
- `docs/`
- `examples/`
- `schemas/`
- `deliverables/`
- `README.md`
- `LICENSE`

The `.dockerignore` file excludes `.env`, `.git`, build outputs, and Word temp lock files.

## Railway Variables

Required variables:

- None. Railway injects `PORT` automatically.

Do not add these to the static proof-pack service:

- `HELIUS_RPC_URL`
- wallet keys
- seed phrases
- bearer tokens
- private RPC credentials
- signer/custody/capital settings

Optional future variable for a separate server-side read-only decode worker:

- `HELIUS_RPC_URL`: read-only HTTPS RPC URL for local or server-side decode proof. Add it only to a non-public worker/service that needs it, never to the static site.

## Setup

1. In Railway, create a new project from the GitHub repository.
2. Select `jf-cmyk/open-perps-reliability-stack`.
3. Let Railway detect and build the checked-in `Dockerfile`.
4. Do not add secrets to the static site service.
5. Generate a public Railway domain for the service.
6. Smoke-check:

```bash
curl -sS -L "$RAILWAY_PUBLIC_URL/" | rg -o "Open Perps Reliability Stack Proof Pack|Read-only|Dry-run"
curl -sS -L "$RAILWAY_PUBLIC_URL/apps/dashboard/" | rg -o "OpenPerp|No live execution|ExecutionDisabledDryRun|AdapterVersionMismatch"
```

## QA Checklist

- `/` returns the proof-pack index.
- `/apps/dashboard/` returns the OpenPerp dashboard.
- The site includes `Read-only`, `Dry-run`, and `No live execution` markers.
- The dashboard includes `ExecutionDisabledDryRun` and `AdapterVersionMismatch`.
- No `.env` content is served.
- No `HELIUS_RPC_URL` value appears in hosted HTML.
