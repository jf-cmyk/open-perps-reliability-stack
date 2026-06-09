# Stronger Jupiter Candidates And Spot Pool Checkpoint

Timestamp: 2026-06-09T00:00:00Z

## Current State

- Scope remains read-only and dry-run only.
- Drift public-field decode now includes one more selected spot metadata field: `SpotMarket.pool_id`.
- Jupiter transaction-history sampling can now label stronger unverified candidates when a shared Jupiter-owned non-executable account is observed.
- Verified Jupiter request/fulfillment pairing is still not claimed.
- Jupiter binary decode remains blocked by canonical IDL/source uncertainty.

## Completed In This Slice

- Extended `scripts/discover_drift_readonly_state.py` public-field mode with:
  - `SpotMarket.pool_id`
- Extended `scripts/discover_jupiter_perps_transaction_history.py` with:
  - `candidate_strength`
  - shared-account owner metadata summaries
  - `stronger_candidate_count`
  - deterministic sorting that places stronger candidate evidence first
- Updated examples, docs, and hosted smoke assertions.

## Drift Boundary

Command:

```bash
scripts/discover_drift_readonly_state.py --include-public-fields --out target/oprs-drift-readonly-state/latest-public-fields.json
```

New field:

- `SpotMarket.pool_id`

Validation expectation:

- USDC/SOL spot `pool_id=0` should match selected public constants.
- Raw account bytes must not be committed.
- `market_economics_decoded=false`.
- `user_state_decoded=false`.
- `replay_ready=false`.
- `HELIUS_RPC_URL` must not be printed.

## Jupiter Boundary

Command used for wider live sample:

```bash
scripts/discover_jupiter_perps_transaction_history.py --limit 30 --transaction-limit 20 --min-shared-keys 2 --out target/oprs-jupiter-perps-transaction-history/latest-wide-sample.json
```

Observed live sample:

- 139 heuristic lifecycle candidates.
- 8 stronger candidates included a shared Jupiter-owned non-executable account.
- Stronger candidates remain `candidate_pair_unverified`.
- `verified_request_fulfillment_pair_claimed=false`.
- `request_fulfillment_pair_claimed=false`.
- `position_request_decoded=false`.
- `raw_transaction_committed=false`.
- `HELIUS_RPC_URL` was not printed.

## Next Queue

1. Validate, commit, push, deploy Railway, and smoke-check hosted mirrors.
2. Keep stronger Jupiter candidates as unverified until PositionRequest/Position semantics are source-pinned.
3. Decode additional Drift fields only after offset/source validation and explicit scrub review.
4. Keep Jupiter binary decode blocked until canonical IDL/source confirmation.
