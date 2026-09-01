# 2026-09-01 Drift 288k And Railway IaC Checkpoint

## Repo

- Path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- Branch: `main`
- Prior pushed commit before this slice: `97c91ca Refresh Drift scan to 278k`

## Scope Boundary

- Read-only and dry-run only.
- No private keys, signing, custody, capital deployment, live liquidation submission, or production trading recommendations.
- No claims of protocol safety, liquidation absence, validator performance improvement, Blocksize readiness, partnership, endorsement, or user demand.

## What Changed

- Railway config migrated from deprecated `railway.json` to `.railway/railway.ts`.
- The generated Railway IaC file was corrected to target the existing `refreshing-art` service instead of creating a duplicate `open-perps-reliability-stack` service.
- `railway config plan` now reports the Railway configuration is already up to date.
- Repo-local Git identity is set to `Johann Focke <243385122+jf-cmyk@users.noreply.github.com>`.
- Helius-backed read-only Drift pagination advanced another 10,000 finalized transactions.
- A public `slot-regime-benchmark-v0` package now records the 400ms-to-350ms activation boundary at slot `440208000` with pre/post windows and blocked performance claims.

## Drift Scan Boundary

- Legacy Drift liquidation-history scan advanced from 278,000 to 288,000 finalized transactions.
- Current Drift scan boundary: July 22 back through slot `415592674` at `2026-04-25T15:31:16Z`.
- Latest bounded tranche covered slots `415733769` through `415592674`.
- The scan found zero logs beginning with `Program log: Instruction: Liquidate`.
- Resume before cursor `39u3VDJhyTrGpe4oa8bdE922p7uzB7V2RcDQWizh4mEaTVTXMRfcpNMP4dUpJdMdrkZMWvHhqkc1LygkMp7jsHyk`.

## Validation Completed In This Slice

- `railway config plan`
- `scripts/validate_drift_liquidation_history_probe.py target/oprs-drift-liquidation-history-probe/latest.json`
- `python3 -m json.tool target/oprs-drift-liquidation-history-probe/latest.json >/dev/null`
- `scripts/validate_public_slot_regime_benchmark.py`
- `scripts/validate_public_contract_index.py`
- DOCX regenerated with `scripts/build_solana_grant_docx.py`
- DOCX rendered to `target/docx-render/proposal-288k` with `render_docx.py --emit_pdf`
- Rendered DOCX pages visually inspected via contact sheet
- `git diff --check`
- `scripts/run_mvp_checks.sh`

## Next Work Queue

- Continue Drift legacy pagination from the new cursor and stop only when a candidate is found, RPC history is exhausted, or source semantics force a new filter.
- Strengthen the Jupiter outbound confirmation package and keep binary decode blocked until a current Jupiter-confirmed IDL/source/hashable artifact exists.
- Keep Phoenix/Rise on validator-plan gates before account-level decode or replay claims.
- Regenerate and render the local Word proposal whenever public proof-pack text changes materially.

## Access Or Confirmation Blockers

- Grant submission remains blocked by founder confirmation. Prepare materials only; do not submit.
- Jupiter canonical decode remains blocked until Jupiter supplies or publicly confirms a current IDL/source/hashable artifact. A Jupiter API key may help with read-only metadata discovery only if it maps to relevant public/canonical source surfaces; do not add it to the repo or Railway static service.
- Helius is approved for read-only scans through local `.env`; do not print or commit the key.

## Fresh-Window Kickoff Prompt

Continue the Open Perps Reliability Stack from `docs/checkpoints/2026-09-01-drift-288k-railway-iac-checkpoint.md`. Preserve read-only and dry-run scope. First run `git status --short`, check whether the current slice was pushed, then continue the no-access queue: slot-regime benchmark fixture, Drift pagination, Jupiter source-authority package, Phoenix/Rise validator-plan gates, and grant proposal alignment.
