# Checkpoint: Drift 328k And Worker Promotion Gates

Date: 2026-09-04

## Current State

- Railway remains the canonical public proof pack.
- GitHub Pages remains the equivalent fallback mirror.
- Static service: `refreshing-art`.
- Read-only worker boundary service: `oprs-readonly-worker`.
- Worker source is not deployed to the worker service yet.
- Product scope remains read-only and dry-run only.

## Completed In This Slice

- Added a public-safe read-only worker candidate schema, example, builder, and validator.
- Added a public package manifest/DQ promotion template for future read-only worker candidates.
- Updated the dashboard, reviewer index, local MVP checks, and hosted smoke checks to cover the worker candidate and promotion template.
- Refreshed the Solana Foundation Word proposal with worker envelope, candidate, and promotion-gate proof points.
- Advanced the Drift legacy liquidation-history scan by 10,000 finalized transactions.
- New cumulative Drift scan boundary: 328,000 finalized transactions from July 22 back through slot `414754843` at `2026-04-21T19:23:41Z`.
- Latest bounded Drift segment found zero logs beginning with `Program log: Instruction: Liquidate`.
- Updated the public scrubbed Drift liquidation-history example and reviewer-facing docs to the new boundary.

## Scope Lock

The Drift scan remains source-governance progress only. It does not prove liquidation absence, decode account roles, prove market economics, verify keeper behavior, establish replay readiness, or authorize execution.

The worker candidate and promotion template do not publish generated worker payload bodies. Public package promotion remains blocked until founder review, final scrub, checksum binding, zero blocking DQ failures, and contract-index review.

## Next Queue

1. Continue Drift legacy pagination from cursor `51hCUKQToXRfTsFQq12voRR1LrQh4dvmoUWjVUogNi7x83mcfoV7rxEDSarpquJ4EqUbPnQVz4HG294SE43Uu5Ye`.
2. Create the private Slack webhook and set `OPRS_ALERT_WEBHOOK_URL` with stdin, then test only the checked-in Slack sample payload through Railway-injected worker variables.
3. Pick the first hosted worker command, schedule, and retention policy before deploying source to `oprs-readonly-worker`.
4. Select the custom domain, then use `docs/access-ops-setup.md` for safe Railway setup.
5. Continue Jupiter verified-pairing design only with before/after lifecycle evidence and source-review gates.
6. Keep adapting grant materials when proof-pack evidence materially changes.

## Fresh-Window Kickoff Prompt

Read this checkpoint, then read `docs/checkpoints/context-map.md`, `docs/drift-liquidation-scan-boundary.md`, `docs/read-only-decode-worker.md`, `docs/railway-readonly-worker-service-plan.md`, and `docs/mvp-proof-checklist.md`.

Continue only read-only and dry-run development. Do not add private keys, wallet files, signing, transaction submission, custody, or capital deployment. Use the Solana research ledger as context, but only promote source-backed, validated, scrubbed claims into reviewer-facing artifacts.

