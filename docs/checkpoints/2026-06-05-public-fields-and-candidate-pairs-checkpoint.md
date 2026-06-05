# Public Fields And Candidate Pairs Checkpoint

Timestamp: 2026-06-05T02:05:31Z

## Current State

- Scope remains read-only and dry-run only.
- Drift public-field decode is now limited to identity fields with pinned offsets.
- Jupiter lifecycle evidence is now limited to shared-account-key candidate pairs.
- Jupiter verified request/fulfillment pairing is still not claimed.
- Jupiter binary decode remains blocked by canonical IDL/source uncertainty.

## Completed In This Slice

- Extended `scripts/discover_drift_readonly_state.py` with `--include-public-fields`.
- Extended `scripts/discover_jupiter_perps_transaction_history.py` with shared-account-key lifecycle candidates.
- Updated examples:
  - `examples/datasets/drift_shape_snapshot_example.json`
  - `examples/datasets/jupiter_perps_transaction_history_example.json`
- Updated docs:
  - `README.md`
  - `docs/drift-decoder-provenance.md`
  - `docs/jupiter-perps-provenance.md`
  - `docs/helius-readonly-proof.md`
  - `docs/mvp-proof-checklist.md`
  - `docs/protocol-targets.md`
- Updated hosted smoke assertions in `scripts/run_hosted_smoke_checks.sh`.

## Drift Public-Field Boundary

Command:

```bash
scripts/discover_drift_readonly_state.py --include-public-fields --out target/oprs-drift-readonly-state/latest-public-fields.json
```

Decoded fields:

- `State.admin`
- `State.signer`
- `PerpMarket.pubkey`
- `SpotMarket.pubkey`
- `SpotMarket.oracle`
- `SpotMarket.mint`
- `SpotMarket.vault`
- `SpotMarket.name`

Live validation:

- Selected Drift state/perp/spot accounts reached `public_fields_decoded`.
- Validation failures were empty.
- Raw account bytes were not committed.
- `market_economics_decoded=false`.
- `user_state_decoded=false`.
- `replay_ready=false`.
- `HELIUS_RPC_URL` was not printed.

## Jupiter Candidate-Pair Boundary

Command:

```bash
scripts/discover_jupiter_perps_transaction_history.py --limit 10 --transaction-limit 6 --min-shared-keys 2 --out target/oprs-jupiter-perps-transaction-history/latest-pairs.json
```

Live validation:

- Public Jupiter Perps program signatures were sampled.
- Structural transaction summaries were emitted.
- Candidate lifecycle pairs were emitted with `proof_status=candidate_pair_unverified`.
- Pairing basis was shared public account keys after common program-account exclusion.
- `verified_request_fulfillment_pair_claimed=false`.
- `raw_account_key_sets_committed=false`.
- Raw transaction bodies, instruction data, and logs were not committed.
- `HELIUS_RPC_URL` was not printed.

## Validation Run

Passed:

```bash
scripts/run_mvp_checks.sh
git diff --check
python3 -m json.tool examples/datasets/drift_shape_snapshot_example.json
python3 -m json.tool examples/datasets/jupiter_perps_transaction_history_example.json
scripts/discover_drift_readonly_state.py --include-public-fields --out target/oprs-drift-readonly-state/latest-public-fields.json
scripts/discover_jupiter_perps_transaction_history.py --limit 10 --transaction-limit 6 --min-shared-keys 2 --out target/oprs-jupiter-perps-transaction-history/latest-pairs.json
```

## Next Queue

1. Commit, push, deploy Railway, and smoke-check hosted mirrors.
2. Upgrade Jupiter pairing only after adding stronger PositionRequest/Position heuristics from public transaction keys.
3. Decode additional Drift market fields only after offset/source validation and explicit scrub review.
4. Keep Jupiter binary decode blocked until canonical IDL/source confirmation.
