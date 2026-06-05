# Drift Shape Snapshot Checkpoint

Timestamp: 2026-06-05T01:43:02Z

## Current State

- Railway remains canonical for reviewer hosting.
- GitHub Pages remains the fallback mirror.
- Scope remains read-only and dry-run only.
- Local `.env` contains `HELIUS_RPC_URL`, but the value must never be printed or committed.
- Live Helius outputs remain under `target/` and are not committed.

## Completed In This Slice

- Added optional Drift shape snapshot mode to `scripts/discover_drift_readonly_state.py`.
- Added public example `examples/datasets/drift_shape_snapshot_example.json`.
- Updated proof docs and checklists:
  - `docs/drift-decoder-provenance.md`
  - `docs/helius-readonly-proof.md`
  - `docs/mvp-proof-checklist.md`
  - `docs/protocol-targets.md`
  - `README.md`
  - `docs/README.md`
- Updated validation scripts:
  - `scripts/run_mvp_checks.sh`
  - `scripts/run_hosted_smoke_checks.sh`

## Shape Snapshot Boundary

The optional Drift mode fetches raw account bytes through read-only RPC and uses them only in memory.

It emits:

- expected IDL account type
- expected and observed Anchor discriminator
- discriminator match result
- account data length
- account data SHA-256
- owner and executable metadata
- `raw_account_data_committed=false`
- `field_decode_claimed=false`
- `replay_ready=false`

It does not emit:

- raw account bytes
- decoded market economics
- user account state
- liquidation pre-state
- transaction history
- replay-ready claims

## Live Proof Observed Locally

Command:

```bash
scripts/discover_drift_readonly_state.py --include-shape-snapshot --out target/oprs-drift-readonly-state/latest-shape.json
```

Confirmed live:

- Drift `State` discriminator matched.
- SOL/BTC/ETH `PerpMarket` discriminators matched.
- USDC/SOL `SpotMarket` discriminators matched.
- Raw account bytes were not committed.
- `HELIUS_RPC_URL` was not printed.

## Agent Guidance Applied

The Solana Expert thread and sidecar agent both recommended Drift safe binary/shape evidence before Jupiter transaction-history proof because Drift provenance is pinned while Jupiter canonical IDL provenance remains unresolved.

## Validation Run

Passed:

```bash
scripts/run_mvp_checks.sh
git diff --check
python3 -m json.tool examples/datasets/drift_shape_snapshot_example.json
scripts/discover_drift_readonly_state.py --include-shape-snapshot --out target/oprs-drift-readonly-state/latest-shape.json
```

## Next Queue

1. Commit and push the Drift shape snapshot package.
2. Deploy Railway and run hosted smoke checks on Railway plus GitHub Pages.
3. Start Drift public-field decode only after offset validation against pinned Drift IDL/SDK decoder.
4. Start Jupiter request/fulfillment transaction-history proof as a separate lane; keep Jupiter binary decode blocked until canonical IDL/source confirmation.
