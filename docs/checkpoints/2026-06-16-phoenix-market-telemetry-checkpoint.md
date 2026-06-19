# Development Checkpoint: 2026-06-16

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Base commit before this slice: `bfc058c`
- Local residue to ignore unless explicitly refreshed: `deliverables/Open Perps Reliability Stack - Solana Foundation Proposal.docx`

## Scope Lock

- Read-only: yes.
- Dry-run/replay: yes.
- No signing/custody/submission/capital: yes.
- OSS/commercial boundary changes: none.

## What Changed Since Previous Checkpoint

- Added `phoenix-market-telemetry-v0` as the third public package family.
- Added a bounded JSON Schema for Phoenix/Rise public market telemetry readiness.
- Added a specialized Phoenix public-package validator.
- Registered the package in `examples/public/contract-index.json`.
- Expanded invalid public-package fixtures from 16 to 20 cases with Phoenix execution/instruction/source/schema negatives.
- Wired Phoenix package validation into local MVP checks and hosted smoke checks.
- Updated grant-safe docs to distinguish current synthetic dry-run evidence from deferred historical reconstruction.
- Added `scripts/discover_phoenix_market_telemetry.py` as a local-only public HTTP probe that writes capped scrubbed summaries under `target/`.
- Added `schemas/datasets/phoenix-market-telemetry-probe-v0.json` and `scripts/validate_phoenix_market_telemetry_probe.py` for non-served local probe outputs.
- Added `docs/solana-real-money-rails-bd-brief.md` from Solana Expert research, using the official June 10, 2026 Solana WSOP announcement as adjacent BD context only.
- Added `scripts/validate_drift_readonly_state.py` to validate local Drift public-field target outputs before any additional field expansion.

## Claim Boundary

Allowed:

- Phoenix/Rise public HTTP and WebSocket market-data surfaces are mapped from official docs.
- Market-quality telemetry candidates are source-backed for exchange snapshots, market configuration, L2 orderbook snapshots, market-statistics history, funding-rate history, and live L2 streams.
- Public package checksums and DQ gates can validate the static package.

Blocked:

- Live Phoenix API response capture is not committed.
- Trader-state decode or monitoring is not claimed.
- Instruction builders, order operations, authenticated routes, signing, transaction submission, custody, capital deployment, continuous WebSocket monitoring, and historical replay are not claimed.

## Validation To Run

```bash
scripts/validate_public_phoenix_market_telemetry.py
scripts/validate_public_contract_index.py
scripts/validate_invalid_public_package_fixtures.py
scripts/run_mvp_checks.sh
scripts/discover_phoenix_market_telemetry.py --out target/oprs-phoenix-market-telemetry/latest.json
scripts/validate_phoenix_market_telemetry_probe.py target/oprs-phoenix-market-telemetry/latest.json
scripts/discover_drift_readonly_state.py --include-public-fields --out target/oprs-drift-readonly-state/latest-public-fields.json
scripts/validate_drift_readonly_state.py target/oprs-drift-readonly-state/latest-public-fields.json
cargo fmt --check
git diff --check
```

After deploy:

```bash
scripts/run_hosted_smoke_checks.sh https://refreshing-art-production-86de.up.railway.app
scripts/run_hosted_smoke_checks.sh https://jf-cmyk.github.io/open-perps-reliability-stack
```

## Agent Guidance Used

- Phoenix explorer: prefer a Phoenix/Rise market-data readiness package before any Rust liquidation adapter. Exclude auth, transaction builders, instruction builders, signing, and order submission.
- Grant explorer: refresh grant-safe wording around hosted MVP, public package index, invalid fixture corpus, tx-plan guardrails, and still-blocked Jupiter canonical source/verified pairing claims.

## Next Queue

Can continue without access:

1. Run full validation, commit, push, deploy Railway, and smoke-check Railway plus GitHub Pages.
2. Continue Drift field expansion only after the local validator passes against current public-field target output and new offsets are source-reviewed.
3. Continue adding BD/grant positioning notes from Solana Expert research only where they are source-backed and do not create MVP product claims.

Needs access or founder confirmation:

1. Jupiter canonical `PositionRequest` source/authority confirmation or direct Jupiter review.
2. Refresh the local Word proposal if the current modified document can be safely regenerated or reconciled.
3. Grant submission timing and final ask confirmation.

## Fresh-Window Kickoff Prompt

```text
Continue development for the Blocksize Open Perps Reliability Stack.

Repo: /Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack
Checkpoint: docs/checkpoints/2026-06-16-phoenix-market-telemetry-checkpoint.md

Read the checkpoint first, then read docs/checkpoints/context-map.md only for the workstream being touched. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation
```
