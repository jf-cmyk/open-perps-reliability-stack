# Spot Metadata And Shared Account Probes Checkpoint

Timestamp: 2026-06-08T23:01:12Z

## Current State

- Scope remains read-only and dry-run only.
- Drift public-field decode now includes selected spot metadata fields.
- Jupiter candidate pairing now includes metadata-only shared-account probes.
- Verified Jupiter request/fulfillment pairing is still not claimed.
- Jupiter binary decode remains blocked by canonical IDL/source uncertainty.

## Completed In This Slice

- Extended `scripts/discover_drift_readonly_state.py` public-field mode with:
  - `SpotMarket.decimals`
  - `SpotMarket.market_index`
- Extended `scripts/discover_jupiter_perps_transaction_history.py` with:
  - metadata-only `getMultipleAccounts` probes for shared candidate accounts
  - `shared_perps_owned_non_executable_count`
  - shared-account metadata probe summary fields
- Updated examples:
  - `examples/datasets/drift_shape_snapshot_example.json`
  - `examples/datasets/jupiter_perps_transaction_history_example.json`
- Updated docs and hosted smoke assertions.

## Drift Boundary

Command:

```bash
scripts/discover_drift_readonly_state.py --include-public-fields --out target/oprs-drift-readonly-state/latest-public-fields.json
```

New fields:

- `SpotMarket.decimals`
- `SpotMarket.market_index`

Live validation:

- USDC spot `decimals=6` matched expected.
- SOL spot `decimals=9` matched expected.
- USDC/SOL spot `market_index` values matched expected.
- Validation failures were empty.
- Raw account bytes were not committed.
- `market_economics_decoded=false`.
- `user_state_decoded=false`.
- `replay_ready=false`.
- `HELIUS_RPC_URL` was not printed.

## Jupiter Boundary

Command:

```bash
scripts/discover_jupiter_perps_transaction_history.py --limit 10 --transaction-limit 6 --min-shared-keys 2 --out target/oprs-jupiter-perps-transaction-history/latest-pairs.json
```

New evidence:

- Shared candidate accounts are probed with `getMultipleAccounts`.
- Probes use `dataSlice` length 0.
- No raw account bytes are emitted.
- Candidates include `shared_perps_owned_non_executable_count`.
- This live sample found no shared Jupiter-owned non-executable account, so candidates remain weaker and unverified.
- `verified_request_fulfillment_pair_claimed=false`.
- `raw_account_key_sets_committed=false`.
- `HELIUS_RPC_URL` was not printed.

## Validation Run

Passed so far:

```bash
python3 -B -c 'import ast, pathlib; ast.parse(pathlib.Path("scripts/discover_drift_readonly_state.py").read_text())'
python3 -B -c 'import ast, pathlib; ast.parse(pathlib.Path("scripts/discover_jupiter_perps_transaction_history.py").read_text())'
scripts/discover_drift_readonly_state.py --include-public-fields --out target/oprs-drift-readonly-state/latest-public-fields.json
scripts/discover_jupiter_perps_transaction_history.py --limit 10 --transaction-limit 6 --min-shared-keys 2 --out target/oprs-jupiter-perps-transaction-history/latest-pairs.json
python3 -m json.tool target/oprs-drift-readonly-state/latest-public-fields.json
python3 -m json.tool target/oprs-jupiter-perps-transaction-history/latest-pairs.json
```

Next validation before commit:

```bash
scripts/run_mvp_checks.sh
git diff --check
```

## Next Queue

1. Commit, push, deploy Railway, and smoke-check hosted mirrors.
2. Upgrade Jupiter pairing only after a sample exposes shared Jupiter-owned non-executable accounts or a safe PositionRequest/Position heuristic.
3. Decode additional Drift fields only after offset/source validation and explicit scrub review.
4. Keep Jupiter binary decode blocked until canonical IDL/source confirmation.
