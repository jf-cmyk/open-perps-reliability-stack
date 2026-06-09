# Worker And Guardrail Package Checkpoint

Timestamp: 2026-06-09T23:25:00Z

## Current State

- Scope remains read-only and dry-run only.
- Railway remains a static proof-pack service and must not receive worker secrets.
- Drift public-field decode now includes selected perp and spot identity/metadata/guardrail fields.
- Jupiter binary decode remains blocked until canonical IDL/source authority is confirmed.

## Completed In This Slice

- Added read-only decode worker v0 contract:
  - `docs/read-only-decode-worker.md`
  - `schemas/datasets/readonly-decode-worker-run-v0.json`
  - `examples/datasets/drift_readonly_decode_worker_run_example.json`
- Added public Drift guardrail snapshot package:
  - `schemas/datasets/guardrail-snapshot-v0.json`
  - `examples/public/drift-guardrails-v0/guardrails.json`
  - `examples/public/drift-guardrails-v0/manifest.json`
  - `examples/public/drift-guardrails-v0/dq.json`
- Added offline guardrail package validator:
  - `scripts/validate_public_guardrail_package.py`
- Added seventh replay fixture:
  - `drift_synthetic_guardrail_unknown_pause_bit_001`
  - expected reason codes: `DataQualityLow`, `ExecutionDisabledDryRun`
- Extended Drift public-field decode for selected `PerpMarket` fields:
  - `market_index`
  - `status`
  - `contract_type`
  - `contract_tier`
  - `paused_operations`
- Updated proof-pack index, dashboard, MVP checklist, Helius proof plan, Drift provenance, and grant proposal language.

## Live Read-Only Drift Validation

The local command validated the new PerpMarket offsets with no validation failures:

```bash
scripts/discover_drift_readonly_state.py --include-public-fields --out target/oprs-drift-readonly-state/latest-public-fields.json
```

Observed examples:

- SOL-PERP: `Active`, `Perpetual`, `B`, empty pause bitset
- BTC-PERP: `Active`, `Perpetual`, `A`, empty pause bitset
- ETH-PERP: `Active`, `Perpetual`, `B`, `SettleRevPool` pause flag

Live output remains under `target/` and is not committed.

## Boundaries

- No raw account bytes are committed.
- `user_state_decoded=false`
- `market_economics_decoded=false`
- `replay_ready=false`
- No signing, transaction submission, retrying, priority-fee bidding, keypair loading, custody, or capital management.

## Next Queue

1. Validate local JSON, Rust tests, MVP checks, public guardrail package, and hosted smoke checks.
2. Commit, push, deploy Railway, and verify GitHub Pages mirror.
3. Consider a normalized `perp_guardrail_snapshot.v0` extension after deciding whether perp and spot guardrails should share one public schema.
4. Continue Jupiter source-authority work without claiming binary decode.
5. Update the Word grant deliverable only when the founder asks to regenerate it.
