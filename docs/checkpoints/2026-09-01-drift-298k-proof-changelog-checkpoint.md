# 2026-09-01 Drift 298k And Proof Changelog Checkpoint

## Repo

- Path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- Branch: `main`
- Prior pushed commit before this slice: `3ede72e Add Railway IaC and slot benchmark proof`

## Scope Boundary

- Read-only and dry-run only.
- No private keys, signing, custody, capital deployment, live liquidation submission, order building, order routing, or production trading recommendations.
- No claims of liquidation absence, protocol safety, Jupiter binary decode, verified Jupiter request/fulfillment pairing, Phoenix/Rise account decode, validator performance improvement, Blocksize readiness, partnership, endorsement, current revenue, or customer demand.

## What Changed

- Helius-backed read-only Drift pagination advanced another 10,000 finalized transactions.
- Public Drift boundary text advanced from 288,000 to 298,000 finalized legacy-program transactions.
- Added public reviewer-facing `docs/proof-pack-changelog.md`.
- Added protocol gate status to the proof-pack front page and dashboard:
  - Drift: partial proof, reconstruction still candidate-gated.
  - Jupiter: authority blocked, decode and verified pairing not claimed.
  - Phoenix/Rise: source pinned, account decode and replay not claimed.
  - Runtime: benchmark ready, performance improvement not claimed.
- Regenerated and render-checked the Solana Foundation proposal DOCX.

## Drift Scan Boundary

- Legacy Drift liquidation-history scan advanced from 288,000 to 298,000 finalized transactions.
- Current Drift scan boundary: July 22 back through slot `415423666` at `2026-04-24T20:58:39Z`.
- Latest bounded tranche covered slots `415592670` through `415423666`.
- The scan found zero logs beginning with `Program log: Instruction: Liquidate`.
- Resume before cursor `2vXjFAqSK23ykcvg36GBo2skhHjnxzZ8C2ZW2Csovf3A8Sgqdt4pB5NeczNmGFn1PbHYr62ZayoANvARH8fzrtd1`.

## Validation Completed In This Slice

- `scripts/validate_drift_liquidation_history_probe.py target/oprs-drift-liquidation-history-probe/latest.json`
- `python3 -m json.tool target/oprs-drift-liquidation-history-probe/latest.json >/dev/null`
- Research state JSON parse
- Research evidence NDJSON parse
- DOCX regenerated with `scripts/build_solana_grant_docx.py`
- DOCX rendered to `target/docx-render/proposal-298k` with `render_docx.py --emit_pdf`
- Rendered DOCX pages visually inspected via contact sheet
- DOCX text check confirmed `298,000` and `415423666`
- `git diff --check`
- `scripts/run_mvp_checks.sh`

## Validation Still Required After Commit

- Commit and push.
- GitHub CI and Pages verification.
- Railway deploy and hosted smoke check.

## Next Work Queue

- Continue Drift legacy pagination from the new cursor and stop only when a candidate is found, RPC history is exhausted, or source semantics force a new filter.
- Keep Jupiter pairing unverified until the Jupiter position-authority confirmation evidence lands from canonical source or direct Jupiter confirmation.
- If a Jupiter API key is used, keep it local in `.env` as `JUPITER_API_KEY` and restrict it to authenticated read-only schema/source discovery only.
- Add local-only Jupiter API discovery tooling only after confirming there is a read-only metadata/schema endpoint worth probing.
- Keep Phoenix/Rise on validator-plan gates before account-level decode or replay claims.
- Keep Railway and GitHub Pages mirrors equivalent.

## Access Or Confirmation Blockers

- Grant submission remains blocked by founder confirmation.
- Jupiter canonical decode remains blocked until Jupiter supplies or publicly confirms a current IDL/source/hashable artifact. The API key does not unlock decode unless it leads to such an artifact.
- Any production execution scope remains blocked by design.

## Fresh-Window Kickoff Prompt

Continue the Open Perps Reliability Stack from `docs/checkpoints/2026-09-01-drift-298k-proof-changelog-checkpoint.md`. Preserve read-only and dry-run scope. First run `git status --short`, check whether the current slice was pushed, then continue the no-access queue: Drift pagination from cursor `2vXjFAqSK23ykcvg36GBo2skhHjnxzZ8C2ZW2Csovf3A8Sgqdt4pB5NeczNmGFn1PbHYr62ZayoANvARH8fzrtd1`, Jupiter source-authority confirmation package, public proof-pack changelog upkeep, Phoenix/Rise validator-plan gates, and grant proposal alignment.
