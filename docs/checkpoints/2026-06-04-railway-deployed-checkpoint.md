# Railway Deployed MVP Checkpoint: 2026-06-04

This checkpoint is the resume point after deploying and smoke-checking the proof-pack MVP on Railway.

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Base commit before this checkpoint update: `855e952 Add Railway MVP checkpoint`
- Railway project: `refreshing-art`
- Railway environment: `production`
- Railway service: `refreshing-art`
- Railway deployment ID: inspect current value with `railway service status --service refreshing-art --json`
- Railway proof pack: `https://refreshing-art-production-86de.up.railway.app/`
- Railway dashboard: `https://refreshing-art-production-86de.up.railway.app/apps/dashboard/`
- GitHub Pages fallback:
  - `https://jf-cmyk.github.io/open-perps-reliability-stack/`
  - `https://jf-cmyk.github.io/open-perps-reliability-stack/apps/dashboard/`
- URL policy: Railway is canonical for grant reviewers; GitHub Pages remains an equivalent fallback mirror.
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

- Railway CLI authentication was confirmed for the founder account.
- Linked Railway service `refreshing-art` in project `refreshing-art`.
- Deployed the checked-in static Docker/Nginx service with `railway up --detach`.
- Re-deployed after the deployment docs/checkpoint update so the public Railway snapshot includes current project memory docs.
- Generated the public Railway domain:
  - `https://refreshing-art-production-86de.up.railway.app`
- Verified Railway service status as `SUCCESS`.
- Verified Nginx served `/` with HTTP 200 during Railway health checks.
- Verified hosted proof-pack and dashboard markers over the public Railway domain.
- Confirmed the static Railway service does not need `HELIUS_RPC_URL`.
- Hardened Railway static serving to return HTTP 404 for missing files instead of falling back to `/index.html`.
- Added `scripts/run_hosted_smoke_checks.sh` for public Railway proof-pack/dashboard marker checks, `.env` 404 checks, and public secret-marker checks.
- Added service-boundary and public-artifact-boundary docs.
- Excluded `docs/checkpoints/` from the Railway proof-pack image while keeping checkpoints in GitHub project memory.
- Created M1 GitHub issues from Railway Deployment Review Agent and Solana Expert Research Agent findings:
  - `#14` Add hosted uptime and secret-exposure monitoring.
  - `#15` Add data reconstruction envelope schema.
  - `#16` Design Helius read-only decode proof command.
  - `#17` Expand replay failure taxonomy for Solana runtime outcomes.
  - `#18` Add branded Railway domain and service naming.
- Implemented `#15` with:
  - `schemas/datasets/data-reconstruction-envelope-v0.json`
  - `examples/datasets/data_reconstruction_envelope.json`
  - `oprs-data` validation for required provenance, relative evidence refs, slot-range sanity, and scrub-policy rejection.
  - public docs and homepage links.
- Founder confirmed Railway as the canonical reviewer URL while keeping GitHub Pages equivalent as a fallback mirror.
- Founder asked Codex to research Helius decode proof targets and venue relevance. Protocol target order is now Drift first, Jupiter second, Phoenix/Rise telemetry third, then FlashTrade/Adrena/Pacifica/Zeta-Bullet diligence.
- Sent deployment-result context to the Railway Deployment Review Agent:
  - `019e93bc-dbed-7a83-8243-63294099ecd2`

## Railway Variables

For the static proof-pack service:

- Required: none.
- Railway injects `PORT` automatically.
- Current variables observed on the static service are Railway-generated metadata only.
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

Passed before deployment:

```bash
git diff --check
git check-ignore -v .env
cargo run -p oprs-replay --example validate_fixtures
cargo run -p oprs-api-types --example validate_api_examples
scripts/run_mvp_checks.sh
scripts/run_hosted_smoke_checks.sh https://refreshing-art-production-86de.up.railway.app
```

Railway deployment checks passed:

```bash
railway whoami
railway service status --service refreshing-art --json
curl -sS -L https://refreshing-art-production-86de.up.railway.app/ | rg -o "Open Perps Reliability Stack Proof Pack|Read-only|Dry-run"
curl -sS -L https://refreshing-art-production-86de.up.railway.app/apps/dashboard/ | rg -o "OpenPerp|No live execution|ExecutionDisabledDryRun|AdapterVersionMismatch"
```

GitHub Actions:

- CI passed for `855e952`.
- Pages deploy passed for `855e952`.

## Recommended Next Development Queue

No access needed:

1. Implement `#17` Solana runtime failure taxonomy expansion.
2. Continue `#16` by implementing a read-only target discovery command that prepares Drift/Jupiter/Phoenix targets without printing `HELIUS_RPC_URL`.
3. Keep adapting grant proposal language as the Railway MVP hardens.
4. Add hosted uptime or scheduled smoke monitoring from `#14`.

Access or confirmation needed:

1. Branded domain/DNS and Railway service naming decision.
2. Final grant submission approval/details.

## New Window Kickoff Prompt

Use this prompt in a fresh Codex window:

```text
Continue development for the Blocksize Open Perps Reliability Stack.

Repo: /Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack
Checkpoint: docs/checkpoints/2026-06-04-railway-deployed-checkpoint.md

Read the checkpoint first. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

The Railway MVP is live at:
https://refreshing-art-production-86de.up.railway.app/

Dashboard:
https://refreshing-art-production-86de.up.railway.app/apps/dashboard/

The static Railway service should not receive HELIUS_RPC_URL. Use Helius only for a separate read-only decode proof worker or local command.

Run `scripts/run_mvp_checks.sh` before committing. After Railway deploys, run `scripts/run_hosted_smoke_checks.sh https://refreshing-art-production-86de.up.railway.app`. Continue with service-boundary docs or Helius read-only decode proof once the target accounts/sources are confirmed.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation
```
