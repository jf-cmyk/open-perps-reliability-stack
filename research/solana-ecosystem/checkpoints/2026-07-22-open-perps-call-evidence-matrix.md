# Open Perps Call Evidence Matrix

Date: 2026-07-22

Primary source: https://solana.com/news/build-onchain-perps (Solana Foundation, June 1, 2026)

## Positioning Decision

OPRS should apply as complementary infrastructure around fully onchain perps, not as a venue. Its value is neutral, open, reproducible evidence about market quality, oracle risk, liquidation health, adapter integrity, and execution reliability. It does not submit orders, match trades, cancel orders, settle positions, sign transactions, hold custody, or deploy capital.

## Requirement Matrix

| Foundation priority | Current OPRS proof | Status | Remaining evidence |
| --- | --- | --- | --- |
| Fully onchain execution | OPRS observes and explains onchain state through read-only adapters, account/transaction discovery, simulation plans, and proof packages. | Complementary only | Do not claim venue execution. Add verified historical transaction-to-state reconstruction when source authority permits. |
| Competitive two-sided price discovery | Market-quality API/dashboard contracts cover spreads, depth, funding, fills, and reliability. Phoenix/Rise telemetry surfaces are publicly packaged. | Partial | Continuous live telemetry and comparative venue measurements are not yet public proof. |
| Solana-first design | Solana account/program adapters, Pyth-aware oracle policy, runtime failure reason codes, Helius-backed read-only discovery, Drift/Jupiter/Phoenix diligence. | Strong | Keep protocol versions and source authority pinned; add network-regime tests for Alpenglow/VAT changes. |
| Revenue routed back to Solana | The grant-funded OPRS core has no required revenue surface. A separately scoped commercial API can use Solana-native stablecoin settlement and the canonical Subscriptions program with observable lifecycle events. | Boundary defined | Keep free outputs meaningful; do not claim current revenue, customers, or settlement. Use the convertible-grant path if the commercial component becomes material. |
| Innovation | Deterministic dry-run classification, explicit reason codes, unsigned plans, source-governed public packages, and negative-evidence fixtures. | Strong design proof | Historical liquidation reconstruction remains unproved; benchmark external builder usefulness. |
| Experienced team | Grant draft cites Blocksize validator operations, Solana infrastructure, Pyth publishing, and liquidation research. | Evidence gap | Add public biographies, prior shipped infrastructure, validator history, Pyth evidence, repositories, and named delivery owners. |
| Open source | Rust workspace, adapter/risk/replay/API contracts, schemas, fixtures, validators, public dashboard, GitHub Pages/Railway proof pack. | Strong local/public artifact proof | Confirm final repository license, contributor setup, tagged release, and reviewer-stable public links. |
| Complementary products | OPRS directly supplies adapters, public datasets, risk/replay methodology, API contracts, dashboard views, and reliability proof packs. | Direct fit | Show adoption path: one builder integration, one reproducible incident/replay case, or one protocol feedback loop. |

## Current Public Proof

- Architecture: `docs/architecture.md`
- Adapter contract and Drift spike: `crates/oprs-adapter/`, `adapters/drift-readonly/`
- Risk and deterministic replay: `crates/oprs-risk/`, `crates/oprs-replay/`, `datasets/sample/`
- Public API and dashboard contracts: `schemas/api/public-api-v0.json`, `schemas/dashboard/public-dashboard-v0.json`, `apps/dashboard/`
- Public claim boundaries: `examples/public/contract-index.json`, Drift guardrail package, Jupiter authority-gap package, and Phoenix telemetry package
- Reviewer proof map: `docs/mvp-proof-checklist.md`

## Grant-Safe Narrative

Open Perps Reliability Stack is open-source complementary infrastructure for teams building fully onchain perps on Solana. It gives builders and reviewers common adapters, market-quality and oracle-risk contracts, deterministic dry-run explanations, source-governed public datasets, and a read-only proof surface. It helps make onchain derivatives inspectable without introducing custody, signing, private execution, or capital deployment.

The public-good core remains freely usable. If Blocksize later packages commercial reliability subscriptions, grant materials should describe that extension separately and show Solana-native settlement at the protocol or payment-rail level, without claiming current revenue or making the commercial layer a condition for access to grant-funded outputs.

## Priority Gaps

1. Jupiter canonical source/IDL authority and verified request/fulfillment pairing.
2. Source-backed Drift market-economics decode and one historical liquidation reconstruction.
3. Continuous Phoenix/Rise market telemetry rather than static readiness evidence.
4. Public team credibility and delivery-owner evidence.
5. One external builder/protocol validation of the public contracts or proof-pack workflow.
