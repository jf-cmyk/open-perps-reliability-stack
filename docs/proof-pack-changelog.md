# Proof-Pack Changelog

This public changelog records reviewer-facing proof-pack progress. It excludes internal checkpoint files, raw scan output, RPC URLs, keys, wallets, private signatures, and non-public research notes.

## 2026-09-01

- Migrated Railway service configuration from deprecated `railway.json` to `.railway/railway.ts` and applied it to the existing canonical `refreshing-art` service.
- Advanced the bounded read-only Drift legacy liquidation-history scan to 328,000 finalized transactions through slot `414754843` at `2026-04-21T19:23:41Z`, with no `Program log: Instruction: Liquidate*` match in the searched segment.
- Added the `slot-regime-benchmark-v0` public package for the Solana mainnet 400ms-to-350ms slot target activation boundary at slot `440208000`.
- Added the `jupiter-onchain-decode-v0` public package, resolving Jupiter `Position` / `PositionRequest` account-layout decode through the live onchain Anchor IDL and normalized IDL hash.
- Added a local-only Jupiter lifecycle role-map probe contract that binds sampled public transaction accounts to onchain-IDL instruction roles while keeping verified pairing, keeper behavior, and replay claims blocked.
- Added the live read-only worker service plan, 7-day soak runbook, and commercial diagnostics brief to define the post-MVP path before any execution scope exists.
- Added a machine-checkable read-only soak summary schema/example and Jupiter verified-pairing validator contract so post-MVP promotion gates can be tested before any hosted worker or execution scope exists.
- Added Slack alerting docs, a scrubbed Slack incoming-webhook payload schema/example, and a validator for future read-only worker alerts.
- Added a Slack sample sender that validates the checked-in payload before dry-run or delivery and supports Railway-injected worker variables without printing webhook secrets.
- Added a local one-shot read-only worker wrapper that plans allowlisted Drift, Jupiter, Phoenix, and Slack-sample jobs before hosted worker deployment.
- Validated bounded local Drift, Jupiter, and Phoenix worker smokes with outputs kept under ignored `target/` paths and no public-output promotion.
- Added a Jupiter verified-pairing fixture contract with rejected role-map-only and synthetic positive cases so lifecycle gate behavior is testable while mainnet pairing remains unclaimed.
- Added a private read-only worker run-envelope contract with builder and validator so local/hosted worker outputs can be summarized by checksum and promotion policy without copying payload bodies into public artifacts.
- Added a public package promotion template for future read-only worker candidates, keeping manifest/DQ creation blocked until founder review and final scrub gates pass.
- Added a public-safe worker candidate summary contract with builder and validator; generated candidates default to blocked pending founder review and package DQ gates.
- Tightened Jupiter source-authority docs to clarify that `JUPITER_API_KEY` may support authenticated read-only discovery but does not unlock verified pairing, keeper execution, or replay claims without a Jupiter-confirmed lifecycle artifact.
- Regenerated the local Solana Foundation proposal DOCX and refreshed validation/smoke checks for the public proof pack.

Boundary: this is source-governance and reviewer evidence progress only. It does not claim liquidation absence, verified Jupiter request/fulfillment pairing, Phoenix/Rise account decode, validator performance improvement, or production execution readiness.

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
