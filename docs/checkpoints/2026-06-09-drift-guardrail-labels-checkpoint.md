# Drift Guardrail Labels Checkpoint

Timestamp: 2026-06-09T22:30:00Z

## Current State

- Scope remains read-only and dry-run only.
- Drift public-field decode now includes source-backed semantic labels for selected spot-market guardrail fields.
- Jupiter binary decode remains blocked until canonical IDL/source authority is confirmed.
- Railway remains the canonical hosted target; GitHub Pages remains the mirror.

## Completed In This Slice

- Added semantic labels to `scripts/discover_drift_readonly_state.py` for:
  - `SpotMarket.status` from Drift `MarketStatus`
  - `SpotMarket.asset_tier` from Drift `AssetTier`
  - `SpotMarket.paused_operations` from Drift `SpotOperation` bit flags
  - `SpotMarket.if_paused_operations` from Drift `InsuranceFundOperation` bit flags
- Updated `examples/datasets/drift_shape_snapshot_example.json` to show:
  - `status` value `1` as `Active`
  - `asset_tier` value `0` as `Collateral`
  - empty pause bitsets as `[]`
- Updated hosted smoke checks to require these semantic labels in the published proof pack.
- Updated Drift decoder provenance to document the pinned source files that back each label family.

## Source Authority

Pinned Drift commit:

```text
0ae3e3b1db782a6765c3525b3dec38ad4d9d3a62
```

Pinned source files:

- `programs/drift/src/state/perp_market.rs`
- `programs/drift/src/state/spot_market.rs`
- `programs/drift/src/state/paused_operations.rs`

## Boundaries

- Raw account bytes are used only in memory for shape/public-field decoding and are not committed.
- `user_state_decoded=false`
- `market_economics_decoded=false`
- `replay_ready=false`
- No signing, transaction submission, priority-fee bidding, keypair loading, custody, or capital management.

## Next Queue

1. Validate local script syntax, JSON examples, live Drift read-only output, and full MVP checks.
2. Commit, push, deploy Railway, and run hosted smoke checks for Railway and GitHub Pages.
3. Keep Jupiter binary decode blocked until canonical source authority is resolved.
4. Continue grant proposal refinement using the stronger Drift guardrail proof language.
