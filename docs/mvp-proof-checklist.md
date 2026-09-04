# MVP Proof Checklist

This checklist maps current reviewer-facing claims to public artifacts, validation commands, and known caveats.

## Reviewer URLs

| Surface | URL | Role |
| --- | --- | --- |
| Railway proof pack | `https://refreshing-art-production-86de.up.railway.app/` | Canonical reviewer URL |
| Railway dashboard | `https://refreshing-art-production-86de.up.railway.app/apps/dashboard/` | Canonical dashboard |
| GitHub Pages proof pack | `https://jf-cmyk.github.io/open-perps-reliability-stack/` | Equivalent fallback mirror |
| GitHub Pages dashboard | `https://jf-cmyk.github.io/open-perps-reliability-stack/apps/dashboard/` | Equivalent fallback dashboard |

## Claims And Evidence

| Claim | Evidence | Validation |
| --- | --- | --- |
| The MVP is read-only and dry-run only. | ADR-0001, dashboard markers, dry-run docs, adapter capabilities. | `scripts/run_mvp_checks.sh` checks `Read-only`, `Dry-run`, `No live execution`, `ExecutionDisabledDryRun`, and execute-disabled adapter tests. |
| The public dashboard/API contract exists. | `schemas/api/public-api-v0.json`, `schemas/dashboard/public-dashboard-v0.json`, `examples/api/`. | `cargo run -p oprs-api-types --example validate_api_examples` |
| Dry-run/replay outputs are deterministic and guarded. | `datasets/sample/*`, `crates/oprs-replay`, `docs/liquidation-dry-run.md`. | `cargo run -p oprs-replay --example validate_fixtures` and `cargo test`; replay tests include tx-plan negatives for signer/submission/execution-policy regressions. |
| Pyth-aware risk primitives are implemented as policy helpers. | `crates/oprs-risk/src/lib.rs` and unit tests. | `cargo test -p oprs-risk` or full `cargo test` |
| Data reconstruction provenance is specified. | `schemas/datasets/data-reconstruction-envelope-v0.json`, `examples/datasets/data_reconstruction_envelope.json`. | `scripts/run_mvp_checks.sh` validates JSON and `oprs-data` tests enforce scrub rules. |
| Solana runtime failure modes are modeled for dry-run explanation. | Expanded `RiskReasonCode` variants and `docs/liquidation-dry-run.md`. | `cargo test -p oprs-replay` covers expanded reason-code fixture coverage. |
| A read-only decode worker contract exists without hosting secrets. | `docs/read-only-decode-worker.md`, `schemas/datasets/readonly-decode-worker-run-v0.json`, `examples/datasets/drift_readonly_decode_worker_run_example.json`, `schemas/datasets/readonly-worker-run-envelope-v0.json`, `examples/datasets/readonly_worker_run_envelope_example.json`, `schemas/datasets/readonly-worker-public-candidate-v0.json`, `examples/datasets/readonly_worker_public_candidate_example.json`, `examples/public/readonly-worker-candidate-template-v0/`. | `scripts/run_mvp_checks.sh` validates JSON, validates the run-envelope, public-candidate, and promotion-template examples, compiles the one-shot worker wrapper and candidate builders, and checks the contract/example files exist. |
| Public package contracts are indexed with explicit claim boundaries. | `examples/public/contract-index.json`, `schemas/datasets/public-contract-index-v0.json`, `docs/public-dataset-contract.md`, `tests/fixtures/public-packages/invalid/cases.json`. | `scripts/validate_public_contract_index.py` validates package paths, JSON Schema shape, payload schema versions, validators, and blocked claims; `scripts/validate_invalid_public_package_fixtures.py` proves dangerous public claims, malformed schema shape, and leak patterns are rejected before publication. |
| Drift public guardrails can be packaged as scrubbed public data. | `schemas/datasets/spot-guardrail-snapshot-v0.json`, `schemas/datasets/perp-guardrail-snapshot-v0.json`, `examples/public/drift-guardrails-v0/`. | `scripts/validate_public_guardrail_package.py` validates split spot/perp JSON Schema shape, payload checksums, row counts, readiness flags, and public-data scrub gates. |
| Jupiter Perps onchain IDL and account-layout decode are source-authorized. | `schemas/datasets/jupiter-onchain-decode-v0.json`, `examples/public/jupiter-onchain-decode-v0/`, `scripts/fetch_jupiter_onchain_idl.py`, `scripts/decode_jupiter_position_examples.py`. | `scripts/validate_public_jupiter_onchain_decode.py` validates the onchain Anchor IDL address, normalized IDL hash, scrubbed `Position` and `PositionRequest` decode records, and explicit no-pairing/no-replay/no-execution flags. |
| Jupiter Perps lifecycle and replay gaps are public and bounded. | `schemas/datasets/jupiter-authority-gap-v0.json`, `examples/public/jupiter-authority-gap-v0/`, `datasets/sample/jupiter_synthetic_lifecycle_candidate_unverified_001/`, `datasets/sample/jupiter_synthetic_lifecycle_weak_no_shared_jupiter_account_001/`, `datasets/sample/jupiter_synthetic_malformed_source_authority_001/`. | `scripts/validate_public_jupiter_authority_gap.py` validates JSON Schema shape, checksums, DQ gates, repo-relative evidence refs, and no verified-pairing/replay claims. |
| Phoenix/Rise market telemetry readiness is public and bounded. | `schemas/datasets/phoenix-market-telemetry-v0.json`, `examples/public/phoenix-market-telemetry-v0/`, `schemas/datasets/phoenix-market-telemetry-probe-v0.json`. | `scripts/validate_public_phoenix_market_telemetry.py` validates the public package; `scripts/validate_phoenix_market_telemetry_probe.py` validates local-only `target/` probe outputs when a public HTTP probe is run. |
| Solana slot-regime benchmark windows are source-governed and bounded. | `schemas/datasets/slot-regime-benchmark-v0.json`, `examples/public/slot-regime-benchmark-v0/`, `docs/slot-regime-benchmark.md`. | `scripts/validate_public_slot_regime_benchmark.py` validates the 400ms-to-350ms activation boundary, pre/post windows, checksums, DQ gates, and blocked performance claims. |
| Source-review records keep decode promotion gates machine-readable. | `schemas/datasets/source-review-record-v0.json`, `examples/datasets/jupiter_position_authority_source_review_example.json`, `examples/datasets/drift_public_field_source_review_template.json`, `docs/source-review-records.md`. | `scripts/validate_source_review_records.py` validates schema shape, Jupiter onchain-IDL layout gates, still-blocked lifecycle gates, forbidden production/replay claims, and Drift local-validator requirements. |
| Drift is first, Jupiter Perps is second, and Phoenix/Rise is third. | `docs/protocol-targets.md` and decision log. | Manual review of `docs/protocol-targets.md`; Drift public perp/spot identity, oracle identity, selected metadata, and guardrail decode, Jupiter target discovery, Jupiter onchain-IDL account-layout decode, and Jupiter candidate pairing are live, while Drift market-economics decode and verified Jupiter request/fulfillment pairing remain pending. |
| Helius read-only proof is local-only, scrubbed, and source-pinned before binary decode. | `scripts/discover_readonly_targets.py`, `scripts/discover_drift_readonly_state.py`, `scripts/validate_drift_readonly_state.py`, `scripts/discover_jupiter_perps_readonly_targets.py`, `scripts/discover_jupiter_perps_transaction_history.py`, `scripts/audit_jupiter_source_authority.py`, `docs/drift-decoder-provenance.md`, `docs/drift-public-field-source-review-checklist.md`, `docs/jupiter-perps-provenance.md`, `docs/jupiter-source-authority-audit.md`, `examples/datasets/readonly_target_discovery_example.json`, `examples/datasets/drift_readonly_state_example.json`, `examples/datasets/drift_shape_snapshot_example.json`, `examples/datasets/jupiter_perps_readonly_targets_example.json`, `examples/datasets/jupiter_perps_transaction_history_example.json`. | `scripts/run_mvp_checks.sh` validates example JSON and compiles proof commands; `scripts/validate_drift_readonly_state.py` validates local target outputs when public-field mode is run; the Drift checklist gates any new public-field offsets; live reports stay under `target/`. |
| Public reviewer artifacts exclude internal project memory and deployment configs. | `scripts/build_public_artifact.sh`, `.dockerignore`, `.railway/railway.ts`, `docs/public-artifact-boundary.md`. | Hosted smoke checks assert 404 for checkpoints, `.env.example`, `Dockerfile`, `.railway/railway.ts`, package metadata, and Railway Nginx config. |
| Railway and GitHub Pages remain equivalent reviewer surfaces. | Railway static deployment and Pages filtered artifact workflow. | `scripts/run_hosted_smoke_checks.sh` against both hosted URLs; `.github/workflows/hosted-smoke.yml` runs hourly and on manual dispatch. |

## Commands

Run the full local validation suite:

```bash
scripts/run_mvp_checks.sh
```

Run hosted smoke checks:

```bash
scripts/run_hosted_smoke_checks.sh https://refreshing-art-production-86de.up.railway.app
scripts/run_hosted_smoke_checks.sh https://jf-cmyk.github.io/open-perps-reliability-stack
```

Build the filtered public artifact used by GitHub Pages:

```bash
scripts/build_public_artifact.sh target/public-proof-pack
```

Run the local read-only target discovery proofs:

```bash
scripts/discover_readonly_targets.py --out target/oprs-readonly-target-discovery/latest.json
scripts/discover_drift_readonly_state.py --out target/oprs-drift-readonly-state/latest.json
scripts/discover_drift_readonly_state.py --include-shape-snapshot --out target/oprs-drift-readonly-state/latest-shape.json
scripts/discover_drift_readonly_state.py --include-public-fields --out target/oprs-drift-readonly-state/latest-public-fields.json
scripts/validate_drift_readonly_state.py target/oprs-drift-readonly-state/latest-public-fields.json
scripts/discover_jupiter_perps_readonly_targets.py --out target/oprs-jupiter-perps-readonly-targets/latest.json
scripts/discover_jupiter_perps_transaction_history.py --limit 10 --transaction-limit 6 --min-shared-keys 2 --out target/oprs-jupiter-perps-transaction-history/latest-pairs.json
scripts/audit_jupiter_source_authority.py --out target/oprs-jupiter-source-authority/latest.json
scripts/discover_phoenix_market_telemetry.py --out target/oprs-phoenix-market-telemetry/latest.json
scripts/validate_phoenix_market_telemetry_probe.py target/oprs-phoenix-market-telemetry/latest.json
scripts/build_readonly_worker_run_envelope.py
scripts/validate_readonly_worker_run_envelope.py target/oprs-worker-run-envelopes/latest.json
scripts/build_readonly_worker_public_candidate.py
scripts/validate_readonly_worker_public_candidate.py target/oprs-worker-public-candidates/latest.json
```

## Deferred Claims

Do not claim these until evidence lands:

- Historical Drift liquidation reconstruction from live Helius reads.
- Verified Jupiter Perps request/fulfillment lifecycle reconstruction.
- Perps market-share or revenue claims without timestamped source snapshots.
- Production liquidation reliability, live execution, priority-fee bidding, custody, signing, or capital deployment.

## Current Helius Status

Local Helius access is confirmed for read-only target discovery. The first command probes the Drift program account and records follow-on venue lanes. The deeper Drift command derives public Drift PDAs from pinned official SDK source and confirms metadata access for the Drift state account, selected perp/spot market accounts, and selected oracle accounts. Its optional public-field mode confirms Drift identity fields plus selected perp/spot guardrail fields without committing raw bytes or claiming market-economics decode. The Jupiter target command resolves current official-doc program/custody/oracle targets and confirms metadata access. The Jupiter history command samples public program signatures, structural transaction summaries, shared-account-key lifecycle candidates, and metadata-only shared-account probes. Wider samples can now label stronger unverified candidates when a shared Jupiter-owned non-executable account is present. The onchain Anchor IDL proof now resolves Jupiter account-layout decode for `Position` and `PositionRequest` with a hash-pinned extracted IDL, while the older docs-linked third-party IDL remains a mismatch. The local Jupiter lifecycle role-map probe can bind sampled public transactions to onchain-IDL instruction roles using hashed summaries under `target/`. The public proof pack includes a Jupiter onchain decode package, a Jupiter lifecycle/replay authority-gap package, and three rejected Jupiter fixtures. Verified request/fulfillment pairing and raw transaction output remain unclaimed. The Phoenix package is source-backed static evidence for public market telemetry surfaces only; the local Phoenix probe can fetch the public exchange snapshot and writes only capped scrubbed shape summaries under `target/`. It does not commit live Phoenix API response bodies or claim replay readiness. All live commands write scrubbed output under `target/` and do not print the RPC URL. Drift decoder/IDL provenance is pinned; Jupiter before/after lifecycle state and public signature fixtures are the next blockers for verified pairing/replay proof.
