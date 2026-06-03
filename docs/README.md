# Documentation

- [Roadmap](roadmap.md)
- [Agent work packages](agent-work-packages.md)
- [Decision log](decision-log.md)
- [Protocol targets](protocol-targets.md)
- [Grant package](grant-package.md)
- [Grant application draft](grant-application-draft.md)
- [Solana Foundation application fields](solana-foundation-application-fields.md)
- [Solana Foundation Developer Tooling proposal](solana-foundation-developer-tooling-proposal.md)
- [Local Word proposal](../deliverables/Open%20Perps%20Reliability%20Stack%20-%20Solana%20Foundation%20Proposal.docx)
- [Architecture](architecture.md)
- [Adapter standard](adapter-standard.md)
- [Data model](data-model.md)
- [Liquidation dry-run and replay](liquidation-dry-run.md)
- [OSS and commercial boundary](oss-commercial-boundary.md)

Schema and fixture artifacts:

- [Public API schema](../schemas/api/public-api-v0.json)
- [Public dashboard schema](../schemas/dashboard/public-dashboard-v0.json)
- [Sample Drift fixture manifest](../datasets/sample/drift_synthetic_margin_001/manifest.json)
- [Fixture catalog](../datasets/sample/fixture_catalog.json)
- [API response examples](../examples/api/)
- [Static dashboard demo](../apps/dashboard/index.html)

Validation commands:

```bash
cargo run -p oprs-replay --example validate_fixtures
cargo run -p oprs-api-types --example validate_api_examples
```

Planned detail areas:

- Pyth-aware risk SDK
- Execution reliability analytics
