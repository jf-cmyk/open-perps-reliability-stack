# 2026-09-01 Drift 308k And Jupiter Resolution Checkpoint

## Repo

- Path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- Branch: `main`
- Prior pushed commit before this slice: `6f5fba5 Finalize Drift 298k checkpoint validation`

## Scope Boundary

- Read-only and dry-run only.
- No private keys, signing, custody, capital deployment, live liquidation submission, order building, order routing, or production trading recommendations.
- No claims of liquidation absence, protocol safety, Jupiter binary decode, verified Jupiter request/fulfillment pairing, Phoenix/Rise account decode, validator performance improvement, Blocksize readiness, partnership, endorsement, current revenue, or customer demand.
- User confirmed that any move beyond read-only/dry-run remains blocked by design.

## What Changed

- Added `docs/jupiter-source-authority-resolution.md`, an operator-facing checklist explaining exactly what Johann must obtain from Jupiter to resolve the canonical source-authority blocker.
- Linked the Jupiter resolution doc from the root README, docs index, and Jupiter position authority confirmation doc.
- Clarified that `JUPITER_API_KEY` may help only with authenticated read-only discovery, not source authority by itself.
- Helius-backed read-only Drift pagination advanced another 10,000 finalized transactions.
- Public Drift boundary text advanced from 298,000 to 308,000 finalized legacy-program transactions.
- Research hot state, evidence ledger, roadmap, public proof-pack changelog, grant docs, and DOCX builder text were updated to the new boundary.
- Regenerated and render-checked the Solana Foundation proposal DOCX.

## Drift Scan Boundary

- Legacy Drift liquidation-history scan advanced from 298,000 to 308,000 finalized transactions.
- Current Drift scan boundary: July 22 back through slot `415272972` at `2026-04-24T04:25:58Z`.
- Latest bounded tranche covered slots `415423666` through `415272972`.
- The scan found zero logs beginning with `Program log: Instruction: Liquidate`.
- Resume before cursor `297aqf8WJXieG1rMtb7LcpDak8i6f5WWcGogvSYsrQcnHA5RFjV2c4JyadMjPfi8BQWaDaPVZTdgeW2PBWQSE14h`.
- This is bounded pagination progress only, not evidence that liquidations were absent.

## Jupiter Resolution Instructions

Johann needs a Jupiter-controlled or Jupiter-confirmed artifact for live program `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu`.

Acceptable evidence includes:

- canonical IDL/source URL plus commit, release, package version, checksum, or hash;
- onchain/program-IDL address plus a hashable extraction path;
- written confirmation from an official Jupiter route that a named source/IDL candidate is canonical;
- API-key-gated read-only endpoint that returns canonical schema/source/IDL metadata with stable versioning;
- public mainnet request/fulfillment fixture signatures confirmed by Jupiter.

Do not paste API keys, private RPC URLs, wallet keys, raw private channel logs, or confidential Jupiter replies into chat or public docs.

## Validation Completed In This Slice

- `scripts/validate_drift_liquidation_history_probe.py target/oprs-drift-liquidation-history-probe/latest.json`
- Safe scan summary extraction from `target/oprs-drift-liquidation-history-probe/latest.json`
- Research state JSON parse
- Research evidence NDJSON parse
- `scripts/run_mvp_checks.sh`
- DOCX regenerated with `scripts/build_solana_grant_docx.py`
- DOCX rendered to `target/docx-render-solana-proposal` with `render_docx.py --emit_pdf`
- Rendered DOCX pages visually inspected via contact sheet
- DOCX text check confirmed `308,000` and `415272972`, and confirmed stale `298,000` / `415423666` grant text is absent

## Next Work Queue

Can continue without access:

1. Run final validation after this checkpoint is committed: `git diff --check`, `scripts/run_mvp_checks.sh`, local public artifact build, hosted smoke after deploy.
2. Commit and push the Jupiter resolution plus Drift 308k boundary update.
3. Deploy canonical Railway proof pack and verify hosted smoke.
4. Continue Drift legacy pagination from cursor `297aqf8WJXieG1rMtb7LcpDak8i6f5WWcGogvSYsrQcnHA5RFjV2c4JyadMjPfi8BQWaDaPVZTdgeW2PBWQSE14h`.
5. Add Phoenix/Hawkeye local account-decode gate checklist before any account-level claim.

Needs access or founder confirmation:

1. Jupiter source authority: Johann must send the outbound note or provide a Jupiter-controlled canonical artifact/confirmation.
2. Grant submission remains blocked until founder confirms final submission.
3. Any production execution, signing, custody, keeper, order-routing, or capital-deployment scope remains blocked by design.

## Fresh-Window Kickoff Prompt

```text
Continue the Open Perps Reliability Stack from `docs/checkpoints/2026-09-01-drift-308k-jupiter-resolution-checkpoint.md`. Preserve read-only and dry-run scope. First run `git status --short`, check whether the current slice was pushed/deployed, then continue the no-access queue: final validation, Railway/GitHub Pages smoke, Drift pagination from cursor `297aqf8WJXieG1rMtb7LcpDak8i6f5WWcGogvSYsrQcnHA5RFjV2c4JyadMjPfi8BQWaDaPVZTdgeW2PBWQSE14h`, Phoenix/Hawkeye local decode gates, and grant proposal alignment. For Jupiter, use `docs/jupiter-source-authority-resolution.md` and keep binary decode/pairing blocked until Jupiter source authority lands.
```
