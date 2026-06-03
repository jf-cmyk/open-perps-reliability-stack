# Context Map

This map tells a fresh Codex window what to read for each workstream. Prefer this over loading the whole conversation history.

## Always Read First

1. [Current checkpoint](2026-06-03-dashboard-design-checkpoint.md)
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
- [Dashboard design checkpoint](2026-06-03-dashboard-design-checkpoint.md)
- [Reviewer-facing grant proposal](../solana-foundation-developer-tooling-proposal.md)

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
- Label current Drift data as synthetic fixture-backed validation until real read-only decode proof lands.

## Protocol And Drift Adapter

Read when changing Drift adapter shape, protocol priority, or venue metadata:

- [Protocol targets](../protocol-targets.md)
- [Adapter standard](../adapter-standard.md)
- `adapters/drift-readonly/src/lib.rs`
- `crates/oprs-adapter/src/lib.rs`
- `crates/oprs-core/src/lib.rs`

Current protocol priority:

1. Drift read-only adapter
2. Phoenix/orderbook market-quality companion
3. Jupiter Perps read-only contrast adapter

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

1. Dataset/scrub-policy failure fixtures and scrub checks.
2. Expanded dry-run reason-code fixture coverage.
3. Dry-run summary and gate invariant validation.
4. Future service-boundary docs.
5. Real Drift read-only decode proof once access/source inputs are confirmed.
