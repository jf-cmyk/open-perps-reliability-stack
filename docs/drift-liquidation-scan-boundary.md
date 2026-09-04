# Drift Liquidation Scan Boundary

This note defines what the current legacy Drift liquidation-history scan does and does not prove.

## Current State

As of the latest validated read-only scan, the paginator has scanned 328,000 finalized transactions for the legacy Drift program from July 22 back through slot `414754843` at `2026-04-21T19:23:41Z` without finding a log message that matches `Instruction: Liquidate`.

The next resume cursor is `51hCUKQToXRfTsFQq12voRR1LrQh4dvmoUWjVUogNi7x83mcfoV7rxEDSarpquJ4EqUbPnQVz4HG294SE43Uu5Ye`. The research ledger in `research/solana-ecosystem/evidence.ndjson` is the audit trail for background research pages; this reviewer note only promotes validated scrubbed scan boundaries.

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
