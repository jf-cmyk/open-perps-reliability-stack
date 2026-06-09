# Source Authority And Guardrails Checkpoint

Timestamp: 2026-06-09T21:45:00Z

## Current State

- Scope remains read-only and dry-run only.
- Drift public-field decode now includes selected spot guardrail fields.
- Jupiter source authority is now audited separately from target/lifecycle evidence.
- Jupiter binary decode remains blocked by canonical IDL/source uncertainty.
- Verified Jupiter request/fulfillment pairing remains unclaimed.

## Completed In This Slice

- Added `scripts/audit_jupiter_source_authority.py`.
- Added `docs/jupiter-source-authority-audit.md`.
- Updated Jupiter provenance with:
  - docs-linked example repo commit `630cfd72cad499f45453a53383d7ac6d3e09e022`
  - unsigned commit verification status
  - IDL Git blob SHA `e7f21c9c44b077d0d10116305b97bbc152081b77`
  - IDL content SHA-256 `8a150cee26dc07c040ca7c1640dc7ec36ba9a0f063923ec50b2438e306b19cab`
- Extended Drift public-field mode with:
  - `SpotMarket.orders_enabled`
  - `SpotMarket.status`
  - `SpotMarket.asset_tier`
  - `SpotMarket.paused_operations`
  - `SpotMarket.if_paused_operations`
- Updated proposal and proof-pack docs to reflect current MVP evidence.

## Jupiter Boundary

Audit command:

```bash
scripts/audit_jupiter_source_authority.py --out target/oprs-jupiter-source-authority/latest.json
```

Current authority decision:

- `authority_status=docs_linked_example_not_canonical`
- `field_planning_authorized=true`
- `binary_decode_authorized=false`
- `verified_lifecycle_pairing_authorized=false`

The docs-linked IDL candidate can inform field planning only. It does not authorize Jupiter binary decode, verified request/fulfillment pairing, PositionRequest decode, or liquidation replay claims.

## Drift Boundary

Command:

```bash
scripts/discover_drift_readonly_state.py --include-public-fields --out target/oprs-drift-readonly-state/latest-public-fields.json
```

New guardrail fields are emitted as observed public values. Follow-on checkpoint `2026-06-09-drift-guardrail-labels-checkpoint.md` adds source-backed semantic labels for selected Drift guardrail enums and bitsets.

Required invariant:

- Raw account bytes must not be committed.
- `market_economics_decoded=false`.
- `user_state_decoded=false`.
- `replay_ready=false`.
- `HELIUS_RPC_URL` must not be printed.

## Next Queue

1. Validate, commit, push, deploy Railway, and smoke-check hosted mirrors.
2. Keep Jupiter binary decode blocked until canonical IDL/source confirmation.
3. Review additional source-backed semantic labels before rendering more Drift/Jupiter fields as names.
4. Continue grant proposal refinement from the updated MVP proof language.
