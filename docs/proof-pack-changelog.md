# Proof-Pack Changelog

This public changelog records reviewer-facing proof-pack progress. It excludes internal checkpoint files, raw scan output, RPC URLs, keys, wallets, private signatures, and non-public research notes.

## 2026-09-01

- Migrated Railway service configuration from deprecated `railway.json` to `.railway/railway.ts` and applied it to the existing canonical `refreshing-art` service.
- Advanced the bounded read-only Drift legacy liquidation-history scan to 298,000 finalized transactions through slot `415423666` at `2026-04-24T20:58:39Z`, with no `Program log: Instruction: Liquidate*` match in the searched segment.
- Added the `slot-regime-benchmark-v0` public package for the Solana mainnet 400ms-to-350ms slot target activation boundary at slot `440208000`.
- Tightened Jupiter source-authority docs to clarify that `JUPITER_API_KEY` may support authenticated read-only discovery but does not unlock binary decode, verified pairing, keeper execution, or replay claims without a Jupiter-confirmed hashable artifact.
- Regenerated the local Solana Foundation proposal DOCX and refreshed validation/smoke checks for the public proof pack.

Boundary: this is source-governance and reviewer evidence progress only. It does not claim liquidation absence, Jupiter binary decode, verified Jupiter request/fulfillment pairing, Phoenix/Rise account decode, validator performance improvement, or production execution readiness.

## 2026-08-31

- Advanced the bounded read-only Drift legacy liquidation-history scan to 278,000 finalized transactions.
- Refreshed grant and proof-pack language with the Solana shorter-slot activation research boundary.
- Kept Drift reconstruction, replay readiness, and protocol-safety claims blocked until a candidate is verified against pinned source and public transaction evidence.

## 2026-07-30

- Added Phoenix/Hawkeye validator-plan evidence and public proof-pack links.
- Added a Drift source-governance checkpoint at 148,000 finalized transactions.
- Verified GitHub Pages and Railway hosted smoke checks for the public proof pack.

## 2026-06-29

- Added Jupiter position-authority confirmation docs and outbound note.
- Updated Jupiter public authority-gap package so binary decode and verified request/fulfillment pairing remain explicitly blocked pending source authority.

## 2026-06-16

- Added Phoenix/Rise public market-telemetry package.
- Kept account-level decode, trader monitoring, routing use, liquidation replay, and live execution blocked.

## 2026-06-10

- Added public package contracts for reviewer-facing datasets.
- Added guardrail and authority-gap validators with public artifact scrub checks.

## 2026-06-04

- Deployed the first Railway-hosted static proof-pack MVP.
- Added hosted smoke monitoring and public artifact boundary checks.

## 2026-06-03

- Created the first static dashboard and proof-pack skeleton.
- Established the read-only and dry-run scope boundary for Open Perps Reliability Stack.
