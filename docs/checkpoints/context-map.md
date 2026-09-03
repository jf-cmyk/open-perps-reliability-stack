# Context Map

This map tells a fresh Codex window what to read for each workstream. Prefer this over loading the whole conversation history.

## Always Read First

1. [Current checkpoint](2026-09-03-worker-commercial-domain-checkpoint.md)
2. [Roadmap](../roadmap.md)
3. [ADR-0001: Read-only and dry-run first](../adr/0001-read-only-dry-run-first.md)

## Scope And Boundaries

Read when changing anything that might imply execution, custody, commercial/private services, or public claims:

- [OSS and commercial boundary](../oss-commercial-boundary.md)
- [ADR-0001: Read-only and dry-run first](../adr/0001-read-only-dry-run-first.md)
- [ADR-0003: OSS/commercial separation](../adr/0003-oss-commercial-separation.md)
- [Grant proposal](../solana-foundation-developer-tooling-proposal.md)

## Architecture

Read when changing module boundaries, service boundaries, contracts, or future services:

- [Architecture](../architecture.md)
- [Adapter standard](../adapter-standard.md)
- [Data model](../data-model.md)
- [Liquidation dry-run and replay](../liquidation-dry-run.md)
- [Live readiness path](../live-readiness-path.md)
- [Railway read-only worker service plan](../railway-readonly-worker-service-plan.md)
- [Access and operations setup](../access-ops-setup.md)
- [Read-only soak runbook](../read-only-soak-runbook.md)
- [Jupiter verified pairing validator](../jupiter-verified-pairing-validator.md)
- [Commercial diagnostics pricing](../commercial-diagnostics-pricing.md)
- [Execution pilot scope](../execution-pilot-scope.md)
- [ADR-0002: Adapter-first boundaries](../adr/0002-adapter-first-boundaries.md)
- [ADR-0004: Deterministic replay before shadow mode](../adr/0004-deterministic-replay-before-shadow-mode.md)

## Fixtures And Replay

Read when changing fixture validation, dry-run outputs, reason codes, or replay examples:

- [Liquidation dry-run and replay](../liquidation-dry-run.md)
- `crates/oprs-replay/src/lib.rs`
- `crates/oprs-replay/examples/validate_fixtures.rs`
- `datasets/sample/fixture_catalog.json`
- `datasets/sample/*/manifest.json`
- `datasets/sample/*/dry_run_output.json`

Required checks:

```bash
cargo run -p oprs-replay --example validate_fixtures
cargo test
```

## API Examples

Read when changing public API example JSON, API response types, or public schema docs:

- `crates/oprs-api-types/src/lib.rs`
- `crates/oprs-api-types/examples/validate_api_examples.rs`
- `examples/api/*.json`
- `schemas/api/public-api-v0.json`

Required checks:

```bash
cargo run -p oprs-api-types --example validate_api_examples
cargo test
```

## Dashboard And Reviewer Proof Pack

Read when changing frontend/static reviewer artifacts:

- `index.html`
- `apps/dashboard/index.html`
- [Railway deployed MVP checkpoint](2026-06-04-railway-deployed-checkpoint.md)
- [Railway deploy-ready MVP checkpoint](2026-06-04-railway-mvp-checkpoint.md)
- [Hosted MVP checkpoint](2026-06-03-hosted-mvp-checkpoint.md)
- [Dashboard design checkpoint](2026-06-03-dashboard-design-checkpoint.md)
- [Reviewer-facing grant proposal](../solana-foundation-developer-tooling-proposal.md)
- [Railway deployment](../deployment-railway.md)
- [Live readiness path](../live-readiness-path.md)
- [Railway read-only worker service plan](../railway-readonly-worker-service-plan.md)
- [Access and operations setup](../access-ops-setup.md)
- [Read-only soak runbook](../read-only-soak-runbook.md)
- [Jupiter verified pairing validator](../jupiter-verified-pairing-validator.md)
- [Commercial diagnostics pricing](../commercial-diagnostics-pricing.md)
- [Execution pilot scope](../execution-pilot-scope.md)

Required checks:

```bash
python3 -m http.server 8791 --bind 127.0.0.1
```

Then inspect:

- `http://127.0.0.1:8791/index.html`
- `http://127.0.0.1:8791/apps/dashboard/index.html`

Stop the server after QA.

## Grant Package

Read when changing the Solana Foundation materials, founder-facing language, or reviewer demo positioning:

- [Solana Foundation application fields](../solana-foundation-application-fields.md)
- [Developer Tooling proposal](../solana-foundation-developer-tooling-proposal.md)
- [Grant application draft](../grant-application-draft.md)
- [Grant package](../grant-package.md)
- `deliverables/Open Perps Reliability Stack - Solana Foundation Proposal.docx`

Wording guardrails:

- Say `read-only`, `dry-run`, `replay`, and `developer tooling`.
- Do not say or imply production trading, live liquidation submission, custody, or capital deployment.
- Keep Drift/Jupiter live proof language bounded to validated read-only public fields and unverified candidate evidence.

## Protocol And Drift Adapter

Read when changing Drift adapter shape, protocol priority, or venue metadata:

- [Source authority and guardrails checkpoint](2026-06-09-source-authority-and-guardrails-checkpoint.md)
- [Drift guardrail labels checkpoint](2026-06-09-drift-guardrail-labels-checkpoint.md)
- [Contract index and Jupiter gap checkpoint](2026-06-09-contract-index-and-jupiter-gap-checkpoint.md)
- [Jupiter onchain decode checkpoint](2026-09-01-jupiter-onchain-decode-checkpoint.md)
- [Split guardrails and oracle identity checkpoint](2026-06-09-split-guardrails-and-oracle-identity-checkpoint.md)
- [Worker and guardrail package checkpoint](2026-06-09-worker-and-guardrail-package-checkpoint.md)
- [Stronger Jupiter candidates and spot pool checkpoint](2026-06-09-stronger-jupiter-candidates-and-spot-pool-checkpoint.md)
- [Spot metadata and shared account probes checkpoint](2026-06-08-spot-metadata-and-shared-account-probes-checkpoint.md)
- [Public fields and candidate pairs checkpoint](2026-06-05-public-fields-and-candidate-pairs-checkpoint.md)
- [Jupiter transaction history checkpoint](2026-06-05-jupiter-transaction-history-checkpoint.md)
- [Drift shape snapshot checkpoint](2026-06-05-drift-shape-snapshot-checkpoint.md)
- [Protocol targets](../protocol-targets.md)
- [Jupiter position authority confirmation](../jupiter-position-authority-confirmation.md)
- [Adapter standard](../adapter-standard.md)
- `adapters/drift-readonly/src/lib.rs`
- `crates/oprs-adapter/src/lib.rs`
- `crates/oprs-core/src/lib.rs`

Current protocol priority:

1. Drift read-only adapter
2. Jupiter Perps read-only contrast adapter
3. Phoenix/Rise orderbook market-quality telemetry companion
4. FlashTrade and Adrena follow-on pool-perps/oracle/keeper comparison
5. Pacifica API-centric diligence later

## Agent Threads

Use background agent threads for bounded questions, not as the only source of truth:

- Coordinator / PM: `019e8a3b-5f29-7172-8138-bf5ff637a867`
- Architecture: `019e8a3b-7710-7212-b6f7-ca48d90f3217`
- Protocol: `019e8a3b-8eb0-7a11-969f-624b03d8d903`
- Data: `019e8a3b-a177-7220-993b-0448c092497b`
- Liquidator/SDK: `019e8a3b-b77c-7812-85b6-ba503200239d`
- Grant Positioning: `019e8a3b-cc8c-79a2-b231-5114cf5e56bd`

When agent guidance affects implementation order, summarize it in the next checkpoint.

## Current No-Access Queue

1. Continue Drift legacy pagination from cursor `2fhTXQqs9qnyX4mBrcKAuTLipxnWyfLG7kj7YRn3EpRNBQoRLignDCCVxCRx1ckfntdhYsSuC6deefgTLS9ghYKm`.
2. Keep Jupiter pairing unverified until the [Jupiter position authority confirmation](../jupiter-position-authority-confirmation.md) lifecycle evidence lands from canonical source or direct Jupiter confirmation.
3. Decode additional Drift fields only after `scripts/validate_drift_readonly_state.py` passes on current local public-field target output and new offsets pass [Drift public field source review checklist](../drift-public-field-source-review-checklist.md).
4. Keep `docs/proof-pack-changelog.md` current for reviewer-facing shipped evidence.
5. Add source-backed BD/grant positioning notes from the Solana Expert thread without creating MVP claims.
6. Jupiter account-layout decode is source-authorized through the live onchain Anchor IDL, and a local role-map probe now binds sampled public transaction accounts to onchain-IDL roles; keep verified lifecycle pairing and replay blocked until before/after state evidence and source-review gates land.
7. Refresh the local Word proposal after public proof-pack text changes materially.
8. Keep Railway and GitHub Pages mirrors equivalent.
9. Configure the existing empty `oprs-readonly-worker` service only after selecting the exact worker command, schedule, and retention policy.
10. Add a local-only worker command wrapper and a synthetic Jupiter pairing-validator fixture before deploying source to the hosted worker service.
11. Select the alert destination and custom domain, then use `docs/access-ops-setup.md` for safe Railway setup.
