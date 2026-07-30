# Drift Liquidation Scan Boundary

This note defines what the current legacy Drift liquidation-history scan does and does not prove.

## Current State

As of the latest Solana research state, the read-only paginator has scanned 140,000 finalized transactions for the legacy Drift program from July 22 back through slot `418377065` on May 8 without finding a log message that matches `Instruction: Liquidate`.

The next resume cursor is stored in `research/solana-ecosystem/state.json`. The research ledger in `research/solana-ecosystem/evidence.ndjson` is the audit trail for each bounded page.

## What The Scan Checks

The scanner pages finalized signatures with `getSignaturesForAddress`, fetches bounded transaction pages with `getTransaction`, and searches raw log messages for the expected `Liquidate*` instruction log shape. Output remains local, scrubbed, and read-only.

## What A No-Match Result Means

A no-match page means only that the scanned transactions did not contain the searched liquidation log prefix under the current RPC query, commitment, program address, and log filter.

It does not prove:

- Liquidations were absent.
- All liquidation variants share the searched log shape.
- The RPC archive returned every relevant historical transaction.
- Account roles, market economics, oracle inputs, or keeper behavior are decoded.
- Historical replay is ready to claim.

## Promotion Gate

Any historical liquidation candidate must stay out of reviewer-facing claims until it has:

1. Public Solana transaction evidence.
2. Pinned Drift source and instruction semantics for the relevant historical program.
3. Account role validation against source-backed layouts.
4. A scrubbed fixture and validation output.
5. A local dry-run or replay artifact that keeps signing, submission, custody, and capital deployment disabled.

Until then, the scan is source-governance progress only.
