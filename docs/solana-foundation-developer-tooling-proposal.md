# Open Perps Reliability Stack For Solana

## Summary

Open Perps Reliability Stack is open-source developer tooling for Solana onchain perps reliability. It provides read-only protocol adapters, Pyth-aware risk primitives, normalized market-quality data, deterministic dry-run liquidation replay, and public dashboard/API schemas.

The grant-funded scope is intentionally read-only and dry-run only. It does not include signing, custody, capital deployment, live liquidation execution, live transaction submission, private-key handling, or trading-profit promises.

## Problem

Solana perps venues are becoming more important, but reliability tooling is fragmented. Builders and risk teams need to understand market quality, oracle health, liquidation conditions, adapter/decode quality, and execution reliability under stress. Today these views are often venue-specific, private, or embedded inside searcher infrastructure.

That creates a public-good gap. Developers can build venues, users can trade, and searchers can run private strategies, but the ecosystem has limited shared infrastructure for answering basic reliability questions:

- Which oracle feeds are stale, wide, missing, or diverging from venue marks?
- Which markets show weak depth, high funding stress, or poor liquidation health?
- Which account/event decoders are failing after program or IDL changes?
- Which liquidation windows are detectable from public state, and why would a dry-run accept or reject them?
- Which data can be published safely without leaking private strategy, RPC secrets, or signer/custody details?

## Proposed Solution

Blocksize will build an open-source reliability stack around Solana perps:

- Adapter standard for read-only Solana perps venue integrations.
- First fixture-backed Drift read-only adapter.
- Pyth-aware risk SDK for staleness, confidence, divergence, and liquidation-risk inputs.
- Canonical event envelope, lineage model, dataset manifests, and data quality publish gates.
- Deterministic replay fixtures and dry-run output bundles with explicit reason codes.
- Public dashboard/API schemas for market quality, oracle risk, liquidation health, adapter health, and methodology.

This is not a new perp venue. It is neutral tooling that helps existing and future Solana perps systems become more inspectable, testable, and reliable.

## Why Solana

The problem is Solana-specific because perps reliability depends on Solana execution mechanics and account state:

- Pyth confidence, exponent, publish time, and freshness.
- Slot timing, blockhash expiry, priority fees, compute budget, and account locks.
- Venue-specific program accounts and event layouts.
- High-throughput historical state, replay, and public dataset needs.
- Onchain liquidation and margin semantics that differ by Solana venue.

## Grant Scope

### In Scope

- Public OSS repo and issue board.
- Architecture docs and ADRs.
- Rust crates for canonical types, adapter traits, risk primitives, data contracts, replay contracts, dry-run contracts, and API types.
- Fixture-backed Drift read-only adapter spike.
- Sample JSON fixtures and public dataset examples.
- Public API/dashboard schema stubs.
- Methodology, limitations, and final grant report.

### Out Of Scope

- Production liquidation execution.
- Live transaction submission.
- Signers, private keys, custody, wallet inventory, or capital controls.
- Autonomous trading or profitability promises.
- Private searcher routing, private validator telemetry, premium APIs, or managed integrations.
- Any use of restricted-license/private Blocksize infrastructure inside grant-funded OSS modules without an explicit license decision.

## Milestones And Budget

Total request: $125,000.

### Milestone 1: Adapter And Architecture Foundation - $25,000

Deliverables:

- Architecture v0 and ADRs.
- Adapter standard and capability matrix.
- Core Rust workspace and type crates.
- Fixture-backed `DriftReadOnlyAdapter` with read-only/simulate/execute-disabled capabilities.

Evidence:

- Public GitHub repo.
- Compile-passing workspace.
- Adapter metadata/provenance fields.
- Unit tests proving execute-disabled safety posture.

### Milestone 2: Canonical Data And Sample Datasets - $35,000

Deliverables:

- Canonical event envelope with lineage/provenance fields.
- Dataset manifest contract.
- Data quality check and publish gate contract.
- Scrub policy for safe public data release.
- Golden fixture examples for synthetic Drift margin/liquidation replay.

Evidence:

- Rust schema types.
- JSON examples with manifest/checksum fields.
- Public docs describing table layout, DQ checks, and scrub rules.

### Milestone 3: Pyth-Aware Risk SDK And Dry-Run Replay - $40,000

Deliverables:

- Oracle staleness, confidence, allowed-source, and divergence policy primitives.
- Liquidation state input/output types.
- Dry-run opportunity, unsigned transaction-plan, simulation, gate, and output-bundle contracts.
- Reason-code taxonomy and deterministic replay methodology.

Evidence:

- Unit tests for stale oracle, wide confidence, fail-open visibility, divergence rejection, and execute-disabled adapter behavior.
- Dry-run sample outputs.
- No-signing guardrails in contracts and docs.

### Milestone 4: Public Dashboard/API Contract And Final Report - $25,000

Deliverables:

- Public API schema for market quality, oracle risk, liquidation health, adapter health, fixtures, and dry-run outputs.
- Dashboard view contract for public read-only surfaces.
- Demo narrative and reproducible walkthrough.
- Final methodology and limitations report.

Evidence:

- Schema files in repo.
- Sample responses.
- Final grant report with delivered artifacts and next-step recommendations.

## Product And Adoption Metrics

Initial developer-tooling metrics:

- GitHub stars/forks/issues from Solana builders and researchers.
- Adapter standard reuse or comments by perps/infrastructure teams.
- Number of public fixture runs and replay examples.
- Number of supported markets/venues in read-only mode.
- Public dataset downloads or downstream notebooks.
- Dashboard/API schema consumers.
- External references in docs, forums, or partner diligence.

Technical quality metrics:

- Adapter decode success rate.
- Missing account/schema mismatch rate.
- Oracle stale/wide/divergent feed counts.
- Dry-run reason-code distribution.
- Fixture replay pass/fail status.
- Dataset publish gate pass/warn/block status.

## Public-Good Value

The project makes a significant open-source contribution to Solana by publishing the reliability substrate that many teams currently have to rebuild privately:

- Open adapter standards.
- Open risk primitives.
- Open data schemas.
- Open replay and dry-run contracts.
- Public sample datasets.
- Public dashboard/API methodology.
- Clear limitations and safety boundaries.

The result is better shared observability for Solana perps without requiring a team to run a private liquidator or proprietary data stack.

## Commercial Boundary

Blocksize may later build commercial services around managed integrations, premium APIs, private analytics, and controlled execution tooling. Those are outside this grant.

Grant-funded work remains public, reproducible, read-only, and no-signing. Commercial work cannot privatize the OSS artifacts funded by the grant.

## Current Proof Of Work

The public repo already includes:

- OSS hygiene files and GitHub workflow.
- Architecture docs, roadmap, work packages, and ADRs.
- Rust workspace with core crates.
- Fixture-backed Drift read-only adapter.
- Adapter metadata and capability model.
- Canonical event and dataset manifest types.
- Data quality publish gate and scrub policy types.
- Pyth-aware risk primitives with unit tests.
- Replay fixture and dry-run output contracts.
- Expanded Solana runtime failure reason codes for account mismatches, invalid account sets, compute budget exhaustion, blockhash expiry, account-lock contention, priority-fee underbids, and unknown dropped transactions.
- Data reconstruction envelope schema with provider, commitment, slot range, query config, evidence refs, source limitations, known gaps, and scrub-policy validation.
- Read-only target discovery and source-authority commands for Helius-backed proof setup. The commands are local-only or public HTTPS only, write scrubbed output under `target/`, confirm credentials are not printed, and have successfully read Drift public program/state/selected market/selected oracle metadata plus Jupiter Perps public program/custody/oracle metadata. Drift now emits selected public identity, spot metadata, and guardrail fields. Jupiter now emits stronger unverified lifecycle candidates when shared Jupiter-owned non-executable accounts are observed, while its source-authority audit keeps binary decode blocked until a canonical IDL/source is confirmed.
- Hosted smoke monitoring for Railway canonical and GitHub Pages fallback URLs.
- Filtered public proof-pack artifact generation so internal checkpoints, `.env.example`, deployment configs, and Word lock files are not served publicly.
- Grant package and application draft.
- Hosted proof-pack MVP path for reviewers:
  - https://refreshing-art-production-86de.up.railway.app/
  - https://refreshing-art-production-86de.up.railway.app/apps/dashboard/
- GitHub Pages fallback:
  - https://jf-cmyk.github.io/open-perps-reliability-stack/
  - https://jf-cmyk.github.io/open-perps-reliability-stack/apps/dashboard/

Repo: https://github.com/jf-cmyk/open-perps-reliability-stack

MVP proof checklist: `docs/mvp-proof-checklist.md`

## Running MVP Before Submission

Before grant submission, Blocksize will keep the MVP runnable as a reviewer-facing proof pack rather than a proposal-only artifact.

The MVP target is:

- Hosted static proof-pack index.
- Hosted public dashboard.
- Local validator commands for fixture replay and API examples.
- Hourly hosted smoke checks for the Railway canonical URL and GitHub Pages fallback.
- Filtered public artifact generation for the Pages fallback.
- Optional Helius-backed read-only decode proof loaded from local `.env`.
- No signing, no private-key handling, no custody, no capital deployment, and no live transaction submission.

The Helius integration is limited to read-only RPC account fetches for decode/provenance proof. RPC URLs and API keys remain local-only and are never committed to the repo or included in public datasets. Drift program/state/selected market/selected oracle metadata discovery now succeeds, selected Drift public guardrail fields are decoded with pinned offsets, and Jupiter Perps program/custody/oracle metadata discovery plus unverified stronger lifecycle candidate labeling now succeed. Jupiter canonical IDL/source confirmation and verified request/fulfillment reconstruction remain next implementation steps.

## Why Blocksize

Blocksize brings Solana infrastructure experience, validator/reliability context, Pyth data-provider experience, and prior liquidation/reliability research. The team understands the difference between public-good methodology and private execution alpha, which is important for keeping this grant clean.

The project also benefits from a disciplined scope boundary: no signing, no custody, no production execution, and no capital deployment in the grant phase. That makes the first phase useful to the ecosystem while avoiding the security, market-conduct, and compliance risks of live liquidation operations.

## Risks And Mitigations

Risk: perps-specific historical liquidation data is thin.

Mitigation: start with fixture-backed Drift adapter shape tests, synthetic golden fixtures, and explicit data-quality caveats before claiming replay coverage.

Risk: venue schemas drift.

Mitigation: adapter metadata includes program IDs, schema versions, supported account schema versions, IDL hash, source update timestamps, and caveats.

Risk: public datasets leak private information.

Mitigation: publish gates and scrub policy remove RPC URLs, API keys, internal paths, route labels, private strategy thresholds, capital controls, and signer/custody metadata.

Risk: project scope creeps into execution.

Mitigation: dry-run transaction plans require `requires_signer=false` and `submission_disabled=true`; production execution remains out of scope.

Risk: commercial track could confuse grant reviewers.

Mitigation: grant-funded outputs are explicitly public-good OSS. Commercial services are disclosed as future/out-of-scope and cannot privatize grant-funded modules.

## Submission Notes

Recommended funding category: Developer Tooling.

Recommended form amount: 125000.

Recommended on-chain accounts field: `N/A - read-only and dry-run only`.

Recommended project/idea field: include a short paragraph plus a link to a shared Google Doc version of this proposal and the public GitHub repo.
