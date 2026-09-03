# Checkpoint: Worker Boundary, Commercial Pricing, And Domain Path

Date: 2026-09-03

## Current State

- Railway remains canonical for the public proof pack.
- GitHub Pages remains the public fallback mirror.
- Static service: `refreshing-art`.
- Read-only worker boundary: `oprs-readonly-worker`.
- The worker service exists as an empty Railway service with no source, no public URL, no deployment, and no secret variables.
- Non-secret guardrail variables are set on `oprs-readonly-worker`: `OPRS_WORKER_MODE`, `OPRS_OUTPUT_MODE`, `OPRS_TARGET_PROTOCOLS`, and `OPRS_RUN_LIMIT`.
- `HELIUS_RPC_URL` was not moved to Railway because secret transfer needs a separate explicit approval.
- Local Railway service link was returned to `refreshing-art` after creating the worker boundary.

## Scope Lock

Current implementation remains read-only and dry-run only:

- No signing.
- No wallet loading.
- No custody.
- No capital deployment.
- No live transaction submission.
- No autonomous liquidation execution.

## Completed In This Slice

- Created empty Railway service `oprs-readonly-worker`.
- Confirmed no secrets were passed during service creation.
- Set non-secret worker guardrail variables on `oprs-readonly-worker` with `--skip-deploys`.
- Documented safe Railway variable setup using stdin for secret-like values.
- Documented alert destination constraints and payload boundary.
- Documented custom domain setup path for Railway.
- Added current-source commercial diagnostics pricing ranges for public API and private dashboard lanes.
- Added execution pilot scope definition and gates.

## Next Queue

1. Add `HELIUS_RPC_URL` to `oprs-readonly-worker` using stdin and explicit `--service` only after explicit approval to store the secret in Railway.
2. Select alert destination type and create the webhook outside the repo.
3. Select the custom domain and run Railway domain setup.
4. Pick the first worker command and retention policy before deploying source to `oprs-readonly-worker`.
5. Keep adapting the grant proposal as live read-only evidence improves.

## Fresh-Window Kickoff Prompt

Read this checkpoint, then read `docs/access-ops-setup.md`, `docs/railway-readonly-worker-service-plan.md`, `docs/commercial-diagnostics-pricing.md`, and `docs/execution-pilot-scope.md`.

Continue with read-only worker operationalization only. Keep `refreshing-art` as the canonical public static service and use `oprs-readonly-worker` only for read-only backend work. Do not add private keys, wallet files, signing, transaction submission, custody, or capital deployment.
