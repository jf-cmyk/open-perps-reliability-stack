# Checkpoint: Split Guardrails And Oracle Identity

Date: 2026-06-09

## Status

The MVP remains read-only and dry-run only. No production execution, signing, custody, priority-fee bidding, or capital deployment is in scope.

Latest development slice:

- Split the public Drift guardrail example package into typed spot and perp payloads:
  - `schemas/datasets/spot-guardrail-snapshot-v0.json`
  - `schemas/datasets/perp-guardrail-snapshot-v0.json`
  - `examples/public/drift-guardrails-v0/spot_guardrails.json`
  - `examples/public/drift-guardrails-v0/perp_guardrails.json`
- Kept one shared manifest/DQ package contract:
  - `examples/public/drift-guardrails-v0/manifest.json`
  - `examples/public/drift-guardrails-v0/dq.json`
  - `docs/public-dataset-contract.md`
- Added a source-backed Drift `PerpMarket.amm.oracle` public-field decode at offset 40.
- Added the eighth synthetic replay fixture, `drift_synthetic_perp_pause_flag_001`, for an observed ETH-PERP `SettleRevPool` perp pause flag.
- Updated replay fixture validation, MVP checks, hosted smoke checks, proof-pack links, dashboard fixture data, and grant/proof docs.

## Why It Matters

The public proof now shows more than a generic worker contract: it shows a guardrail-first public dataset package with separate spot/perp schemas, explicit data-quality gates, and a fixture that rejects observed public pause-state risk before any execution path exists.

This is a stronger grant-review story because the OSS output is:

- reproducible
- source-pinned
- scrubbed for public release
- useful without private liquidator infrastructure
- bounded away from live execution

## Validation To Run

```bash
scripts/validate_public_guardrail_package.py
cargo run -p oprs-replay --example validate_fixtures
scripts/run_mvp_checks.sh
git diff --check
```

Then deploy and smoke-check:

```bash
git push
railway up --detach
scripts/run_hosted_smoke_checks.sh https://refreshing-art-production-86de.up.railway.app
scripts/run_hosted_smoke_checks.sh https://jf-cmyk.github.io/open-perps-reliability-stack
```

## Agent Guidance Applied

- Architecture: split public guardrail schemas into spot/perp payloads while keeping one package manifest.
- Protocol: add one final small Drift field family, oracle identity/provenance, then pause broad Drift expansion.
- Data: keep the guardrail validator specialized for this package and document the shared public dataset contract.
- Liquidator/SDK: add a perp pause-flag replay fixture classified as `Rejected` with `DataQualityLow` plus `ExecutionDisabledDryRun`.
- Grant Positioning: emphasize guardrail proof as the main public-good evidence; worker contract is supporting evidence.

## Next Queue

1. Finish local validation and scrub checks.
2. Commit, push, deploy Railway, and run hosted smoke checks.
3. Keep Railway and GitHub Pages equivalent.
4. Move the next protocol proof to Jupiter source authority and request/fulfillment lifecycle semantics.
5. Add more Drift fields only after explicit source/offset validation and scrub review.
