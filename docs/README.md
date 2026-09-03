# Documentation

- [Roadmap](roadmap.md)
- [Agent work packages](agent-work-packages.md)
- [Decision log](decision-log.md)
- [Protocol targets](protocol-targets.md)
- [Grant package](grant-package.md)
- [Grant application draft](grant-application-draft.md)
- [Solana Foundation application fields](solana-foundation-application-fields.md)
- [Solana Foundation Developer Tooling proposal](solana-foundation-developer-tooling-proposal.md)
- [Solana real-money rails BD brief](solana-real-money-rails-bd-brief.md)
- [Local Word proposal](../deliverables/Open%20Perps%20Reliability%20Stack%20-%20Solana%20Foundation%20Proposal.docx)
- [Architecture](architecture.md)
- [Adapter standard](adapter-standard.md)
- [Data model](data-model.md)
- [Liquidation dry-run and replay](liquidation-dry-run.md)
- [Helius read-only proof plan](helius-readonly-proof.md)
- [Drift decoder provenance](drift-decoder-provenance.md)
- [Drift liquidation scan boundary](drift-liquidation-scan-boundary.md)
- [Drift public field source review checklist](drift-public-field-source-review-checklist.md)
- [Jupiter Perps provenance](jupiter-perps-provenance.md)
- [Jupiter position authority confirmation](jupiter-position-authority-confirmation.md)
- [Jupiter position authority outbound note](jupiter-position-authority-outbound.md)
- [Jupiter source authority resolution](jupiter-source-authority-resolution.md)
- [Jupiter verified pairing validator](jupiter-verified-pairing-validator.md)
- [Phoenix / Rise source authority](phoenix-source-authority.md)
- [Phoenix / Hawkeye validator plan](phoenix-hawkeye-validator-plan.md)
- [Slot regime benchmark boundary](slot-regime-benchmark.md)
- [Source review records](source-review-records.md)
- [OSS and commercial boundary](oss-commercial-boundary.md)
- [Service boundaries](service-boundaries.md)
- [Public artifact boundary](public-artifact-boundary.md)
- [Proof-pack changelog](proof-pack-changelog.md)
- [Public dataset contract](public-dataset-contract.md)
- [MVP proof checklist](mvp-proof-checklist.md)
- [Live readiness path](live-readiness-path.md)
- [Railway read-only worker service plan](railway-readonly-worker-service-plan.md)
- [Slack alerting](slack-alerting.md)
- [Read-only soak runbook](read-only-soak-runbook.md)
- [Commercial diagnostics brief](commercial-diagnostics-brief.md)
- [Railway deployment](deployment-railway.md)
- [Reviewer proof-pack index](../index.html)

Schema and fixture artifacts:

- [Public API schema](../schemas/api/public-api-v0.json)
- [Public dashboard schema](../schemas/dashboard/public-dashboard-v0.json)
- [Data reconstruction envelope schema](../schemas/datasets/data-reconstruction-envelope-v0.json)
- [Read-only soak summary schema](../schemas/datasets/readonly-soak-summary-v0.json)
- [Slack alert payload schema](../schemas/datasets/slack-alert-payload-v0.json)
- [Source review record schema](../schemas/datasets/source-review-record-v0.json)
- [Sample Drift fixture manifest](../datasets/sample/drift_synthetic_margin_001/manifest.json)
- [Fixture catalog](../datasets/sample/fixture_catalog.json)
- [API response examples](../examples/api/)
- [Dataset provenance example](../examples/datasets/data_reconstruction_envelope.json)
- [Read-only soak summary example](../examples/datasets/readonly_soak_summary_example.json)
- [Slack alert payload example](../examples/datasets/slack_alert_payload_example.json)
- [Jupiter position authority source review example](../examples/datasets/jupiter_position_authority_source_review_example.json)
- [Phoenix Hawkeye source review example](../examples/datasets/phoenix_hawkeye_source_review_example.json)
- [Phoenix Hawkeye validator plan example](../examples/datasets/phoenix_hawkeye_validator_plan_example.json)
- [Drift public field source review template](../examples/datasets/drift_public_field_source_review_template.json)
- [Read-only target discovery example](../examples/datasets/readonly_target_discovery_example.json)
- [Drift read-only state discovery example](../examples/datasets/drift_readonly_state_example.json)
- [Drift shape snapshot example](../examples/datasets/drift_shape_snapshot_example.json)
- [Jupiter Perps read-only target example](../examples/datasets/jupiter_perps_readonly_targets_example.json)
- [Jupiter Perps transaction history example](../examples/datasets/jupiter_perps_transaction_history_example.json)
- [Public package contract index](../examples/public/contract-index.json)
- [Drift guardrails public package](../examples/public/drift-guardrails-v0/)
- [Jupiter authority-gap public package](../examples/public/jupiter-authority-gap-v0/)
- [Jupiter onchain decode public package](../examples/public/jupiter-onchain-decode-v0/)
- [Phoenix market telemetry public package](../examples/public/phoenix-market-telemetry-v0/)
- [Slot-regime benchmark public package](../examples/public/slot-regime-benchmark-v0/)
- [Invalid public package corpus](../tests/fixtures/public-packages/invalid/cases.json)
- [Static dashboard demo](../apps/dashboard/index.html)

Validation commands:

```bash
cargo run -p oprs-replay --example validate_fixtures
cargo run -p oprs-api-types --example validate_api_examples
scripts/send_slack_alert_sample.py --dry-run
scripts/run_mvp_checks.sh
```

Planned detail areas:

- Pyth-aware risk SDK
- Execution reliability analytics

Project-memory docs live under `docs/checkpoints/`. They are kept in the GitHub repo for development continuity but excluded from the Railway proof-pack image because reviewer artifacts should not include local resume prompts, operational notes, or local filesystem paths.
