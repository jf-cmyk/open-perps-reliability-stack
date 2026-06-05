# Grant Package v0

## Title

Open Perps Reliability Stack for Solana

## Public-Good Claim

Open-source, read-only infrastructure that helps Solana perps builders, risk teams, market makers, and researchers inspect market quality, oracle risk, liquidation health, and execution reliability without relying on private venue tooling or proprietary datasets.

This is not a new perp venue. It is the missing reliability substrate around Solana perps: open adapters, Pyth-aware risk tooling, normalized datasets, dry-run liquidation analysis, and public reliability dashboards.

## Milestones

1. Adapter standard: define `PerpsVenueAdapter` for markets, positions, funding, fills, oracle state, margin, and liquidation eligibility.
2. First read-only adapter: ship one supported venue adapter with fixtures, decode-health reporting, and reproducible backfill docs.
3. Pyth-aware risk SDK: open-source stale-price, confidence, divergence, liquidation-price, and stress-scenario helpers.
4. Market-quality data layer: publish normalized sample datasets for open interest, funding, fills, liquidations, oracle divergence, and adapter health.
5. Dry-run liquidation replay: detect and classify historical opportunities as safe, unsafe, stale-oracle, thin-liquidity, unprofitable, or execution-failed. No signing.
6. Public dashboard/API: read-only views for market quality, oracle risk, liquidation health, and execution reliability methodology.
7. Docs and grant report: integration guide, data schema, methodology, limitations, and final milestone evidence.

## Budget Categories

- Protocol adapter engineering.
- Data indexing and backfill.
- Pyth/risk SDK.
- Dashboard/API.
- Replay/simulation tooling.
- QA and test fixtures.
- Documentation and developer relations.
- RPC/data infrastructure.
- Security/license review.
- Project management.

## OSS Deliverables

- Adapter interface.
- First read-only adapter.
- Risk SDK.
- Normalized schema.
- Replay harness.
- Dashboard/API schemas.
- Public sample datasets.
- Methodology docs.
- Integration guide.
- Milestone reports.

## Commercial Boundary

Grant-funded work stays read-only, public, reproducible, and no-signing. Commercial work stays outside grant scope:

- Premium low-latency APIs.
- Managed protocol integrations.
- Private analytics.
- Execution routing.
- Live liquidation operations.
- Signer management.
- Capital deployment.
- SLA-backed services.

## Diligence Risks

- Perps-specific decoded datasets are still thin.
- Drift is the likely first adapter, but decoded perps liquidation fixtures still need to be built.
- Validator/RPC telemetry access may vary.
- Public data must be scrubbed for secrets.
- License boundaries between Apache and BUSL/private components require care.
- Execution-phase security and compliance are explicitly out of scope for this grant.

## Demo Narrative

Here is the current Open Perps Reliability Stack proof pack running as a public, read-only MVP. Railway is the canonical reviewer URL, with an equivalent GitHub Pages fallback. The dashboard shows market quality, oracle confidence/staleness, liquidation-risk bands, adapter health, and dry-run guardrails. The replay fixtures explain why opportunities are accepted or rejected without keys, custody, capital, signing, or transaction submission.

The MVP proof checklist maps claims to URLs, schemas, fixtures, and validation commands: [MVP proof checklist](mvp-proof-checklist.md).

## Founder Decisions Needed

- Drift binary decode proof, Jupiter Perps canonical IDL/source provenance, and Jupiter request/fulfillment proof.
- Grant ask size.
- Preferred OSS license.
- Public dataset depth.
- Whether validator telemetry belongs in v0.
- Commercial carveout language.
- Whether to position this as pure public-good grant or public-good grant with future commercial track disclosed.
