# Solana Foundation Application Fields

Source form: https://share.hsforms.com/1GE1hYdApQGaDiCgaiWMXHA5lohw

## Recommended Form Choices

| Field | Response |
| --- | --- |
| Company name | Blocksize |
| Website URL | https://blocksize.info/ |
| Country | Germany |
| First Name | Johann |
| Last Name | Focke |
| Email Address | jf@blocksize-capital.com |
| Solana On-Chain Accounts | N/A - the grant scope is read-only and dry-run only. No on-chain program, token, fee payer wallet, custody wallet, or production execution account is part of this proposal. |
| Which funding category are you applying for? | Developer Tooling |
| Funding amount | 125000 |
| Is / will this project be open sourced? | Yes |

## Your Project / Idea

Open Perps Reliability Stack is open-source developer tooling for Solana onchain perps reliability. It gives builders, researchers, risk teams, and venue operators a neutral way to inspect market quality, oracle risk, liquidation health, adapter health, and dry-run liquidation outcomes without depending on private venue dashboards or proprietary bot infrastructure.

The grant-funded scope is public, read-only, and dry-run only. It includes protocol adapter standards, a fixture-backed Drift read-only adapter, Pyth-aware risk primitives, canonical event/data schemas, reproducible sample datasets, deterministic dry-run/replay outputs, and public dashboard/API schema definitions. It explicitly excludes private keys, custody, capital deployment, production liquidation execution, live transaction submission, and trading-profit promises.

Developer Tooling proposal link: [replace with shared Google Doc URL copied from docs/solana-foundation-developer-tooling-proposal.md].

Public repo: https://github.com/jf-cmyk/open-perps-reliability-stack

If referred by a Solana Foundation partner or contact, add the referral name here before submission.

## Why You?

Blocksize is well positioned to build this because the team combines Solana infrastructure operations, validator/reliability context, Pyth data-provider experience, and prior liquidation/reliability research. The project is not a speculative new perp venue; it is a public-good reliability layer around the venues and oracle systems Solana perps already depend on.

The current repo already demonstrates execution discipline: OSS hygiene, architecture ADRs, read-only/dry-run scope boundaries, Rust workspace scaffolding, core type crates, a fixture-backed Drift read-only adapter, Pyth-aware risk policy tests, canonical data envelope types, data reconstruction provenance schema, replay fixture manifests, dry-run output contracts, hosted smoke monitoring, and a running reviewer-facing static proof-pack MVP on Railway with a filtered GitHub Pages fallback. Public package contracts now index Drift guardrail evidence, Jupiter authority-gap blockers, and Phoenix/Rise market telemetry readiness with explicit claim boundaries. Jupiter remains source-authority blocked for binary account decode and verified request/fulfillment pairing. Phoenix/Rise is source-pinned for production program and Hawkeye view planning, but account-level decode, trader monitoring, oracle-input identity, liquidation replay, and historical reconstruction are not claimed. That gives the Foundation a concrete base to evaluate rather than a purely narrative application.

Blocksize also has a clear commercial boundary: grant-funded deliverables remain public, reproducible, and no-signing. Future premium APIs, managed integrations, private analytics, or controlled execution services would be outside the grant scope and cannot privatize the public artifacts funded here.

Adjacent ecosystem note for BD conversations: Solana Foundation's June 2026 WSOP, MoneyGram/SDP, and bare-metal validator-readiness announcements show Solana being positioned for high-visibility real-money payment, settlement, institutional infrastructure, and high-throughput validator operations. That supports the broader importance of neutral reliability tooling, but it is not an MVP claim; this grant remains scoped to read-only open perps developer tooling.

## Budget And Milestone Summary

Total request: $125,000.

Milestone 1 - Adapter and architecture foundation: $25,000.

- Public architecture v0, ADRs, adapter standard, capability matrix, and first fixture-backed Drift read-only adapter.
- Evidence: public repo, compile-passing Rust workspace, adapter metadata, read-only/simulate/execute-disabled tests.

Milestone 2 - Canonical data and sample datasets: $35,000.

- Canonical event envelope, dataset manifest, lineage fields, data quality publish gates, scrub policy, and golden fixture samples.
- Evidence: schema docs, Rust types, JSON examples, checksum-bearing fixture manifest.

Milestone 3 - Pyth-aware risk SDK and dry-run replay: $40,000.

- Oracle staleness/confidence/divergence primitives, liquidation state inputs, reason-code taxonomy, dry-run output bundles, and deterministic replay examples.
- Evidence: unit tests, sample dry-run output, documented no-signing transaction-plan guardrails.

Milestone 4 - Public dashboard/API contract and final report: $25,000.

- Public API schema, dashboard view contract, demo narrative, methodology, limitations, and final grant report.
- Evidence: API/dashboard schema files, sample responses, reproducible demo path, adoption-readiness docs.

## Backup Fields If The Category Is Changed Away From Developer Tooling

### Budget Proposal

Requesting $125,000 across four measurable public-good milestones: $25,000 for adapter/architecture foundation, $35,000 for data schemas and public sample datasets, $40,000 for Pyth-aware risk SDK and dry-run replay, and $25,000 for public dashboard/API contracts plus final reporting. Each milestone ships public OSS artifacts and evidence in the repository.

### Relevant Metrics

Current status: public GitHub repo live; Railway reviewer-facing static proof-pack MVP live; GitHub Pages fallback live; OSS governance files, architecture docs, ADRs, Rust workspace, core crates, Drift read-only adapter spike, Pyth-aware risk primitives, canonical data contracts, public package index, Drift guardrail package, Jupiter authority-gap package, Phoenix/Rise market telemetry readiness package, Phoenix/Rise source-authority note and MVP validator, invalid package corpus, replay tx-plan guardrail negatives, data reconstruction envelope schema, dry-run/replay contracts, hosted smoke monitoring, and unit tests are already pushed. Drift legacy liquidation-history diligence has scanned 145,000 finalized program transactions from July 22 back through slot 418197785 on May 7 without a matching `Liquidate*` log; this is bounded queue progress only, not evidence that liquidations were absent. Jupiter program/custody/oracle metadata and lifecycle candidates are readable/sampleable, but canonical current IDL/source authority, binary decode, and verified request/fulfillment pairing remain blocked. Phoenix/Rise production program and Hawkeye view constants are pinned from Ellipsis Labs Rise source, while account-level decode, trader monitoring, oracle-input identity, liquidation replay, and live execution remain blocked. This is pre-adoption developer tooling; success metrics will be GitHub usage, adapter integrations, reproducible fixture runs, public dataset downloads, dashboard/API consumers, and downstream references by Solana perps builders/researchers.

### Funding Status

Planning to raise funds in the next year for commercial services outside the grant scope. The grant-funded deliverables remain public-good OSS and are not dependent on a private financing round.

### Competition

Existing venue dashboards, private searcher/liquidator infrastructure, proprietary data vendors, and protocol-specific analytics partially cover pieces of this problem. They do not provide a neutral open adapter standard, reproducible perps reliability datasets, Pyth-aware public risk primitives, and fixture-backed deterministic dry-run replay under one OSS stack.

### Public Good

The project is a public good because it turns private reliability knowledge into reusable Solana developer tooling: open adapters, open schemas, sample datasets, public methodology, public dashboard/API contracts, and deterministic replay artifacts. It helps developers inspect perps venue health and oracle/liquidation risk without needing private bot infrastructure or proprietary data.
