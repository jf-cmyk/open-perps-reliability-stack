# Solana Foundation Grant Application Draft

## Project Title

Open Perps Reliability Stack for Solana

## One-Line Summary

Open-source, read-only infrastructure for Solana perps reliability: protocol adapters, Pyth-aware risk tooling, normalized market-quality data, dry-run liquidation replay, and public reliability dashboards.

## Problem

Solana perps venues are growing quickly, but builders and risk teams still lack neutral public tooling for comparing venue health, oracle risk, liquidation conditions, and execution reliability. Today these views are fragmented across venue-specific dashboards, private bots, RPC logs, and ad hoc research.

The result is a public-good gap: developers can build venues, searchers can run private strategies, and users can trade, but the ecosystem has limited shared infrastructure for inspecting whether perps markets are reliable under stress.

## Proposed Solution

Blocksize will build the Open Perps Reliability Stack as open-source, read-only, dry-run infrastructure:

- A standard adapter interface for Solana perps venues.
- A first read-only Drift adapter plus fixture-backed tests.
- Pyth-aware risk primitives for confidence, staleness, divergence, and liquidation-band analysis.
- Normalized perps data schemas and public sample datasets.
- Dry-run liquidation replay and reason-code classification.
- Public dashboard/API schemas for market quality, oracle risk, liquidation health, and adapter health.

The first grant phase will not include production trading, custody, private-key handling, live liquidation submission, or capital deployment.

## Why Blocksize

Blocksize brings Solana infrastructure context, validator operations experience, Pyth data-provider experience, and prior liquidation/reliability research. The team has already built a local research corpus around liquidation economics, execution constraints, data quality, and dry-run readiness.

This grant turns that research into public, reusable infrastructure rather than a private trading system.

## Milestones

### Milestone 1: Adapter and Architecture Foundation

Deliverables:

- Architecture v0 and ADRs.
- Adapter standard.
- `DriftReadOnlyAdapter` spike.
- Core Rust type crates.

Evidence:

- Public GitHub repo.
- Compile-passing workspace.
- Docs and issue board.

### Milestone 2: Data Model and Dataset Contract

Deliverables:

- Canonical event envelope.
- Dataset manifest type.
- Data quality publish gates.
- Scrubbing policy.

Evidence:

- Public schema docs.
- Rust schema types.
- Example fixture manifest.

### Milestone 3: Risk SDK and Dry-Run Replay

Deliverables:

- Pyth-aware oracle policy primitives.
- Liquidation opportunity model.
- Replay fixture manifest.
- Dry-run output bundle and reason-code taxonomy.

Evidence:

- Tests or deterministic fixtures.
- Public dry-run examples.

### Milestone 4: Public Demo Surface

Deliverables:

- Public dashboard/API schema.
- Market-quality, oracle-risk, liquidation-health, and adapter-health views.
- Demo narrative and methodology.

Evidence:

- Running Railway proof-pack MVP and filtered GitHub Pages fallback.
- Final report.

## Budget

Recommended Solana Foundation request: $125,000.

Milestone split:

- Milestone 1, adapter and architecture foundation: $25,000.
- Milestone 2, canonical data and sample datasets: $35,000.
- Milestone 3, Pyth-aware risk SDK and dry-run replay: $40,000.
- Milestone 4, public dashboard/API contract and final report: $25,000.

Budget categories:

- Protocol adapter engineering.
- Data schemas, sample datasets, and data quality gates.
- Risk SDK and dry-run engine.
- Dashboard/API contracts.
- QA and fixtures.
- Documentation and developer relations.
- RPC/data infrastructure for reproducible reads.
- Security/license review.
- Project management.

## Open-Source Deliverables

- Adapter standard.
- First read-only adapter.
- Core type crates.
- Risk SDK primitives.
- Data schemas.
- Replay fixture format.
- Dry-run output format.
- Public sample datasets.
- Documentation and ADRs.

## Commercial Boundary

Commercial services may later include premium APIs, managed integrations, private execution analytics, and controlled execution services, but these are outside the grant scope.

Grant-funded outputs remain public, reproducible, read-only, and dry-run only.

## Risks and Mitigations

- Perps-specific decoded liquidation data is thin: start with Drift adapter scaffolding and fixture-backed shape tests.
- First live Helius proof still needs corrected local read-only RPC endpoint access; do not claim historical decode coverage until that passes.
- Live execution is high risk: explicitly out of scope.
- Public datasets may leak secrets or private strategy: enforce scrubbing policy and publish gates.
- Venue schemas may drift: adapter metadata includes schema and IDL versioning.
- License boundaries matter: keep BUSL/private Express Relay internals out of OSS modules.

## Founder Decisions Needed

- Whether validator telemetry belongs in v0.
- Public dataset depth.
- Whether the application should disclose the future commercial track explicitly or keep the proposal framed as pure public-good infrastructure.

Grant ask and milestone split are now recommended in `docs/solana-foundation-application-fields.md`; founder should confirm before submission.
