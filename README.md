# Open Perps Reliability Stack

Open-source reliability infrastructure for Solana onchain perps: protocol adapters, market-quality data, Pyth-aware risk tooling, liquidation dry-run/replay, and execution reliability analytics.

Initial scope: read-only and dry-run only. No production trading, custody, or live execution.

## Current Workstreams

- [Roadmap](docs/roadmap.md)
- [Agent work packages](docs/agent-work-packages.md)
- [Decision log](docs/decision-log.md)
- [Protocol targets](docs/protocol-targets.md)
- [Grant package](docs/grant-package.md)
- [Grant application draft](docs/grant-application-draft.md)
- [Solana Foundation application fields](docs/solana-foundation-application-fields.md)
- [Solana Foundation Developer Tooling proposal](docs/solana-foundation-developer-tooling-proposal.md)
- [Local Word proposal](deliverables/Open%20Perps%20Reliability%20Stack%20-%20Solana%20Foundation%20Proposal.docx)
- [Architecture](docs/architecture.md)
- [Adapter standard](docs/adapter-standard.md)
- [Data model](docs/data-model.md)
- [Liquidation dry-run and replay](docs/liquidation-dry-run.md)
- [OSS and commercial boundary](docs/oss-commercial-boundary.md)
- [Reviewer proof-pack index](index.html)
- [Public API schema](schemas/api/public-api-v0.json)
- [Public dashboard schema](schemas/dashboard/public-dashboard-v0.json)
- [Sample Drift fixture dataset](datasets/sample/drift_synthetic_margin_001/manifest.json)
- [Fixture catalog](datasets/sample/fixture_catalog.json)
- [API response examples](examples/api/)
- [Static dashboard demo](apps/dashboard/index.html)

## Local Verification

```bash
cargo run -p oprs-replay --example validate_fixtures
cargo run -p oprs-api-types --example validate_api_examples
cargo test
```
