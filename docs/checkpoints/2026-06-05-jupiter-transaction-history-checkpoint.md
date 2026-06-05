# Jupiter Transaction History Checkpoint

Timestamp: 2026-06-05T01:49:44Z

## Current State

- Scope remains read-only and dry-run only.
- Jupiter Perps target discovery is live for program, custody, and oracle metadata.
- Jupiter IDL provenance remains candidate-only, not canonical.
- The new transaction-history lane is a public signature and structural transaction-summary sample, not request/fulfillment pairing.

## Completed In This Slice

- Added `scripts/discover_jupiter_perps_transaction_history.py`.
- Added `examples/datasets/jupiter_perps_transaction_history_example.json`.
- Updated proof docs and checklists:
  - `docs/jupiter-perps-provenance.md`
  - `docs/helius-readonly-proof.md`
  - `docs/mvp-proof-checklist.md`
  - `docs/protocol-targets.md`
  - `README.md`
  - `docs/README.md`
- Updated validation scripts:
  - `scripts/run_mvp_checks.sh`
  - `scripts/run_hosted_smoke_checks.sh`

## History Sample Boundary

The command uses only:

- `getSlot`
- `getSignaturesForAddress`
- `getTransaction`

It emits:

- public signature rows
- transaction slot/block-time/fee/error/version summaries
- account key count
- top-level and inner Jupiter program instruction counts
- log-message count
- explicit `request_fulfillment_pair_claimed=false`
- explicit `position_request_decoded=false`
- explicit `raw_transaction_committed=false`

It does not emit:

- raw transaction bodies
- raw instruction data
- raw logs
- decoded PositionRequest or Position accounts
- request/fulfillment pairs
- keeper identity/strategy
- liquidation replay

Forbidden routes and actions remain excluded: no signing, no transaction submission, no `/order`, `/execute`, `/build`, `/submit`, auth, keeper operation, RFQ/order routing, custody, or capital management.

## Live Proof Observed Locally

Command:

```bash
scripts/discover_jupiter_perps_transaction_history.py --limit 8 --transaction-limit 3 --out target/oprs-jupiter-perps-transaction-history/latest.json
```

Confirmed live:

- Helius returned public Jupiter Perps program signatures.
- Three transactions were summarized structurally.
- Each summary carried `program_invocation_observed_only`.
- No request/fulfillment pairing was claimed.
- `HELIUS_RPC_URL` was not printed.

## Agent Guidance Applied

The Solana sidecar recommended a future `jupiter_perps_request_fulfillment_history` lane that links request signature, candidate PositionRequest account, fulfillment signature, and final status. This checkpoint implements the safer prerequisite sample only; the pairing lane remains next.

## Validation Run

Passed:

```bash
scripts/run_mvp_checks.sh
git diff --check
scripts/discover_jupiter_perps_transaction_history.py --limit 8 --transaction-limit 3 --out target/oprs-jupiter-perps-transaction-history/latest.json
python3 -m json.tool examples/datasets/jupiter_perps_transaction_history_example.json
```

## Next Queue

1. Commit and push the Jupiter transaction-history sample package.
2. Deploy Railway and run hosted smoke checks on Railway plus GitHub Pages.
3. Add request/fulfillment pairing only after identifying safe shared-account heuristics from public transaction keys.
4. Keep Jupiter binary decode blocked until canonical IDL/source confirmation.
