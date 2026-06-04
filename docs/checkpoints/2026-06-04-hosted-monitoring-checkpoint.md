# Hosted Monitoring Checkpoint: 2026-06-04

This checkpoint is the resume point after adding scheduled hosted smoke monitoring for the public proof-pack MVP.

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Base commit before this checkpoint update: `68793d7 Add read-only target discovery command`
- Railway project: `refreshing-art`
- Railway environment: `production`
- Railway service: `refreshing-art`
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

- Added `.github/workflows/hosted-smoke.yml`.
- The hosted smoke workflow runs hourly and on manual dispatch.
- The workflow checks both public reviewer surfaces:
  - Railway canonical: `https://refreshing-art-production-86de.up.railway.app`
  - GitHub Pages fallback: `https://jf-cmyk.github.io/open-perps-reliability-stack`
- The workflow uses no secrets and no Railway variables.
- Hardened `scripts/run_hosted_smoke_checks.sh` so it can run with either `rg` or POSIX `grep`.
- Added `scripts/build_public_artifact.sh` so GitHub Pages deploys the same filtered reviewer artifact boundary as Railway.
- Tightened hosted smoke checks for specific checkpoint files, `.env.example`, deployment config paths, Railway `nosniff`, and public JSON secret markers.
- Documented the hosted monitoring contract in `docs/deployment-railway.md` and README.
- Added `docs/mvp-proof-checklist.md` and updated grant materials so the application reflects the running Railway MVP and the Helius access caveat.
- Updated project memory so protocol priority is Drift first, Jupiter second, Phoenix/Rise third, then FlashTrade/Adrena/Pacifica diligence.
- Sent monitoring review context to Railway Deployment Review Agent:
  - `019e93bc-dbed-7a83-8243-63294099ecd2`
- Sent read-only Drift/Jupiter proof context to Solana Expert Research Agent:
  - `019e8f41-3d20-7f00-b3d2-15f0e8b3fc89`

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

Passed locally:

```bash
git diff --check
scripts/run_mvp_checks.sh
scripts/run_hosted_smoke_checks.sh https://refreshing-art-production-86de.up.railway.app
scripts/run_hosted_smoke_checks.sh https://jf-cmyk.github.io/open-perps-reliability-stack
```

The GitHub Pages smoke command required an outside-sandbox network run because the sandbox could not resolve `jf-cmyk.github.io`.

Expected post-push checks:

- CI should run on `main`.
- Deploy proof pack should run on `main`.
- Hosted smoke can be run manually from GitHub Actions immediately and will run hourly after the workflow is active.

## Recommended Next Development Queue

Can continue without access:

1. Adapt grant proposal language to reflect the running Railway MVP, hosted monitoring, data reconstruction envelope, runtime failure taxonomy, and read-only discovery command.
2. Add a founder-facing MVP proof checklist that maps reviewer claims to hosted URLs, schemas, fixtures, and validation commands.
3. Continue dry-run proof polish and dashboard copy while preserving read-only/dry-run language.

Needs access or founder confirmation:

1. Correct local Helius RPC endpoint/key so `scripts/discover_readonly_targets.py --out target/oprs-readonly-target-discovery/latest.json` no longer returns `Unauthorized`.
2. Branded domain/DNS and Railway service naming decision.
3. Final grant submission approval/details.

## Helius Fix Instructions For Founder

Background: the local command reached Helius but Helius returned `Unauthorized`. That usually means the `.env` value is not the full active RPC endpoint, the API key is not active, or the endpoint was copied for the wrong network/product.

Do this from your side without pasting the key into chat:

1. Open the Helius dashboard.
2. Select the project/API key intended for Solana mainnet RPC.
3. Copy the full HTTPS RPC endpoint, including the API key query parameter. Do not copy only the raw key.
4. In the repo root, update `.env` so it contains exactly one `HELIUS_RPC_URL` line shaped like:

```bash
HELIUS_RPC_URL="https://mainnet.helius-rpc.com/?api-key=YOUR_KEY_HERE"
```

5. Run:

```bash
scripts/discover_readonly_targets.py --out target/oprs-readonly-target-discovery/latest.json
```

Expected success: the command writes a scrubbed JSON report to `target/oprs-readonly-target-discovery/latest.json` and does not print the secret URL.

## New Window Kickoff Prompt

Use this prompt in a fresh Codex window:

```text
Continue development for the Blocksize Open Perps Reliability Stack.

Repo: /Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack
Checkpoint: docs/checkpoints/2026-06-04-hosted-monitoring-checkpoint.md

Read the checkpoint first. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

Railway is the canonical reviewer URL:
https://refreshing-art-production-86de.up.railway.app/

GitHub Pages is the equivalent fallback:
https://jf-cmyk.github.io/open-perps-reliability-stack/

The static Railway service should not receive HELIUS_RPC_URL. Helius is local or future worker-only, and the latest run returned Unauthorized until the endpoint/key is corrected.

Run `scripts/run_mvp_checks.sh` before committing. For hosted checks, run both:
scripts/run_hosted_smoke_checks.sh https://refreshing-art-production-86de.up.railway.app
scripts/run_hosted_smoke_checks.sh https://jf-cmyk.github.io/open-perps-reliability-stack

Continue with grant proposal adaptation and MVP proof checklist unless Helius access is fixed first.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation
```
