# 2026-08-31 Drift 278k And Shorter Slot Research Checkpoint

## Repo

- Path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- Branch: `main`
- Prior pushed commit before this slice: `03b7c8b Refresh Solana research and Drift scan boundary`
- This checkpoint should be updated with the new commit hash after push if a fresh window starts before the final run summary is available.

## Purpose

Preserve the current project state after promoting the latest grant-safe Solana research findings into the public proof pack.

## Scope Boundary

- Read-only and dry-run only.
- No private keys, signing, custody, capital deployment, live liquidation submission, or production trading recommendations.
- No claims of protocol safety, liquidation absence, validator performance improvement, Blocksize readiness, partnership, endorsement, or user demand.

## Promoted Research

- Legacy Drift liquidation-history scan advanced from 266,000 to 278,000 finalized transactions.
- Current Drift scan boundary: July 22 back through slot `415733773` at `2026-04-26T07:00:53Z`.
- Latest bounded tranche covered slots `415878863` through `415733773`.
- The scan found zero logs beginning with `Program log: Instruction: Liquidate`.
- Resume before cursor `3jh46Jgw6UhfPnMDedAewucwmuAPfzLY5rPXWV9oeWjwVQ4UzCTBGaKFpnpRibWJEgXvrBPLRWF2GhWiKMZLWaMe`.
- Solana's 400ms-to-350ms mainnet slot-time activation is now treated as a source-governed benchmark boundary at activation slot `440208000`, mapped by public block time to `2026-08-19T05:50:49Z`.

## Claim Boundaries

- The Drift scan is bounded queue progress only. It does not prove that liquidations were absent, that every liquidation variant emits the searched log shape, that public RPC history is complete, or that replay is ready.
- The 350ms slot-time feature account is benchmark context only. It does not prove achieved slot duration, faster confirmations, lower latency, better landing, lower skip rates, tighter spreads, improved validator performance, Blocksize readiness, or activation of any other feature gate.
- Pyth Core post-cutover, Kamino Scope v0.40.0, and Circle/DefiLlama reconciliation findings remain research backlog items until a separate proof-pack artifact promotes them with explicit source and claim boundaries.

## Updated Public Artifacts

- `docs/drift-liquidation-scan-boundary.md`
- `docs/grant-application-draft.md`
- `docs/solana-foundation-developer-tooling-proposal.md`
- `docs/solana-foundation-application-fields.md`
- `scripts/build_solana_grant_docx.py`
- `scripts/run_mvp_checks.sh`
- `scripts/run_hosted_smoke_checks.sh`

## Validation

- `python3 -m json.tool research/solana-ecosystem/state.json >/dev/null`
- `python3` NDJSON parse for `research/solana-ecosystem/evidence.ndjson`
- DOCX regenerated with `scripts/build_solana_grant_docx.py`
- DOCX rendered to `target/docx-render/proposal-278k` with `render_docx.py --emit_pdf`
- Rendered DOCX pages visually inspected via contact sheet
- `git diff --check`
- `scripts/run_mvp_checks.sh`

## Next Work Queue

- Continue Drift legacy pagination from the new cursor and stop only when a candidate is found, RPC history is exhausted, or source semantics force a new filter.
- Build a slot-regime benchmark fixture that labels pre/post activation windows without asserting performance improvement.
- Keep Jupiter canonical decode blocked until a current Jupiter-confirmed IDL/source or hashable artifact is obtained.
- Keep Phoenix/Rise on validator-plan gates before account-level decode or replay claims.
- Update the grant proposal while the MVP advances, keeping reviewer-facing wording aligned with validated artifacts.

## Access Or Confirmation Blockers

- GitHub push/Actions/Pages require the existing authenticated GitHub CLI/session.
- Railway deployment requires the existing linked Railway project and active login.
- Grant submission remains blocked by founder confirmation. Prepare materials only; do not submit.
- Jupiter canonical decode remains blocked until Jupiter supplies or publicly confirms a current IDL/source/hashable artifact.
- Any use of Pyth Hermes after its Core cutover requiring API-key access remains out of the public grant MVP unless explicitly authorized and kept local-only.

## Fresh-Window Kickoff Prompt

Continue the Open Perps Reliability Stack from `docs/checkpoints/2026-08-31-drift-278k-shorter-slot-research-checkpoint.md`. Preserve read-only and dry-run scope. First run `git status --short`, check whether the current slice was pushed, then continue the no-access queue: Drift pagination, slot-regime benchmark fixtures, Jupiter source-authority blockers, Phoenix/Rise validator-plan gates, and grant proposal alignment.
