# Open Perps Reliability Stack

Open-source reliability infrastructure for Solana onchain perps: protocol adapters, market-quality data, Pyth-aware risk tooling, liquidation dry-run/replay, and execution reliability analytics.

Initial scope: read-only and dry-run only. No production trading, custody, or live execution.

Hosted proof-pack MVP:

- Railway proof pack: https://refreshing-art-production-86de.up.railway.app/
- Railway dashboard: https://refreshing-art-production-86de.up.railway.app/apps/dashboard/
- GitHub Pages fallback: https://jf-cmyk.github.io/open-perps-reliability-stack/
- Railway deployment notes: [docs/deployment-railway.md](docs/deployment-railway.md)

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
- [Helius read-only proof plan](docs/helius-readonly-proof.md)
- [Drift decoder provenance](docs/drift-decoder-provenance.md)
- [OSS and commercial boundary](docs/oss-commercial-boundary.md)
- [Service boundaries](docs/service-boundaries.md)
- [Public artifact boundary](docs/public-artifact-boundary.md)
- [MVP proof checklist](docs/mvp-proof-checklist.md)
- [Reviewer proof-pack index](index.html)
- [Railway deployment notes](docs/deployment-railway.md)
- [Public API schema](schemas/api/public-api-v0.json)
- [Public dashboard schema](schemas/dashboard/public-dashboard-v0.json)
- [Data reconstruction envelope schema](schemas/datasets/data-reconstruction-envelope-v0.json)
- [Sample Drift fixture dataset](datasets/sample/drift_synthetic_margin_001/manifest.json)
- [Fixture catalog](datasets/sample/fixture_catalog.json)
- [API response examples](examples/api/)
- [Dataset provenance example](examples/datasets/data_reconstruction_envelope.json)
- [Read-only target discovery example](examples/datasets/readonly_target_discovery_example.json)
- [Drift read-only state discovery example](examples/datasets/drift_readonly_state_example.json)
- [Jupiter Perps read-only target example](examples/datasets/jupiter_perps_readonly_targets_example.json)
- [Static dashboard demo](apps/dashboard/index.html)

## Local Verification

```bash
cargo run -p oprs-replay --example validate_fixtures
cargo run -p oprs-api-types --example validate_api_examples
cargo test
```

Run the full local MVP check:

```bash
scripts/run_mvp_checks.sh
```

Build the same filtered public artifact used by GitHub Pages:

```bash
scripts/build_public_artifact.sh target/public-proof-pack
```

Run the hosted Railway smoke check:

```bash
scripts/run_hosted_smoke_checks.sh https://refreshing-art-production-86de.up.railway.app
```

Run the GitHub Pages fallback smoke check:

```bash
scripts/run_hosted_smoke_checks.sh https://jf-cmyk.github.io/open-perps-reliability-stack
```

Run the local Helius-backed read-only target discovery proof:

```bash
scripts/discover_readonly_targets.py --out target/oprs-readonly-target-discovery/latest.json
```

Run the deeper Drift state, market, and oracle metadata proof:

```bash
scripts/discover_drift_readonly_state.py --out target/oprs-drift-readonly-state/latest.json
```

Run the Jupiter Perps program, custody, and oracle metadata proof:

```bash
scripts/discover_jupiter_perps_readonly_targets.py --out target/oprs-jupiter-perps-readonly-targets/latest.json
```
