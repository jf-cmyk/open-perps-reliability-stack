# Railway MVP Checkpoint: 2026-06-04

Superseded by [Railway Deployed MVP Checkpoint: 2026-06-04](2026-06-04-railway-deployed-checkpoint.md). This file records the deploy-ready state before Railway authentication and public-domain smoke checks were completed.

This checkpoint is the resume point after making the hosted MVP deploy-ready for Railway and adding the local MVP runner.

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Latest implementation commit at checkpoint time: `ba5ca47 Add local MVP check runner`
- Railway deployment commit: `e7c4e2b Add Railway static deployment config`
- Hosted GitHub Pages proof pack remains live:
  - `https://jf-cmyk.github.io/open-perps-reliability-stack/`
  - `https://jf-cmyk.github.io/open-perps-reliability-stack/apps/dashboard/`
- Local untracked item to ignore: `deliverables/~$en Perps Reliability Stack - Solana Foundation Proposal.docx`

## Scope Lock

Current execution scope remains strict:

- Read-only only.
- Dry-run/replay only.
- No production trading.
- No custody.
- No private-key handling.
- No live transaction submission.
- No capital deployment.
- No signer, wallet, keypair, block-engine submission, or execution-router surface in OSS v0.

## What Changed Since Previous Checkpoint

- Founder added Helius RPC URL to local `.env`.
- Verified `.env` exists locally without printing its contents.
- Verified `.env` is gitignored.
- Added Railway static deployment config:
  - `Dockerfile`
  - `.dockerignore`
  - `railway.json`
  - `deploy/railway/nginx.conf.template`
  - `docs/deployment-railway.md`
- Added local MVP runner:
  - `scripts/run_mvp_checks.sh`
- Railway CLI is installed but not authenticated:
  - `railway whoami` returned `Unauthorized. Please run railway login again.`
- Railway deployment review agent created and pinned:
  - `019e93bc-dbed-7a83-8243-63294099ecd2`
  - title: `Railway Deployment Review Agent`

## Railway Variables

For the static proof-pack service:

- Required: none.
- Railway injects `PORT` automatically.
- Do not add `HELIUS_RPC_URL` to the static public service.

Optional future variable for a separate server-side read-only decode worker:

- `HELIUS_RPC_URL`: add only to the worker/service that performs read-only decode proof.

Never add:

- private keys
- seed phrases
- wallet files
- bearer tokens
- signer/custody/capital settings
- live transaction submission endpoints

## Validation Commands And Results

Passed:

```bash
git diff --check
git check-ignore -v .env
cargo run -p oprs-replay --example validate_fixtures
cargo run -p oprs-api-types --example validate_api_examples
scripts/run_mvp_checks.sh
```

`scripts/run_mvp_checks.sh` also passed:

- fixture replay validation
- API example validation
- full Rust tests
- static proof-pack markers
- dashboard markers
- Railway config JSON validation
- local `HELIUS_RPC_URL` presence check without printing the value

GitHub Actions:

- CI passed for `e7c4e2b`.
- Pages deploy passed for `e7c4e2b`.
- CI passed for `ba5ca47`.
- Pages deploy passed for `ba5ca47`.

## Railway Setup Steps

1. Run `railway login` locally, or connect the GitHub repo in the Railway dashboard.
2. Create a Railway project from `jf-cmyk/open-perps-reliability-stack`.
3. Let Railway use the root `Dockerfile`.
4. Do not add variables to the static service.
5. Generate a Railway public domain.
6. Smoke-check:

```bash
curl -sS -L "$RAILWAY_PUBLIC_URL/" | rg -o "Open Perps Reliability Stack Proof Pack|Read-only|Dry-run"
curl -sS -L "$RAILWAY_PUBLIC_URL/apps/dashboard/" | rg -o "OpenPerp|No live execution|ExecutionDisabledDryRun|AdapterVersionMismatch"
```

## Recommended Next Development Queue

No access needed:

1. Expand future service-boundary docs.
2. Keep adapting grant proposal language as MVP hardens.
3. Review Solana Expert and Railway Deployment Review Agent outputs and turn findings into development QA tickets.
4. Add optional read-only Helius decode proof command once exact account/source targets are selected.

Access or confirmation needed:

1. Railway login or dashboard access to complete Railway deployment.
2. Railway public URL after deployment for hosted smoke checks.
3. Founder confirmation on whether Railway static service is the canonical MVP URL.
4. Drift account/source targets for Helius read-only decode proof.
5. Final grant submission approval/details.

## New Window Kickoff Prompt

Use this prompt in a fresh Codex window:

```text
Continue development for the Blocksize Open Perps Reliability Stack.

Repo: /Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack
Checkpoint: docs/checkpoints/2026-06-04-railway-mvp-checkpoint.md

Read the checkpoint first. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

The repo is Railway-deploy-ready with Dockerfile, railway.json, and docs/deployment-railway.md. Railway CLI exists but needs `railway login`. The static service should not receive HELIUS_RPC_URL.

Run `scripts/run_mvp_checks.sh` before committing. Continue with service-boundary docs or Helius read-only decode proof once the target accounts/sources are confirmed.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation
```
