# Slot Regime Benchmark Boundary

This note defines the public benchmark boundary for Solana's 400ms-to-350ms slot-time activation.

## Current State

The Solana Foundation reported that feature gates reduced mainnet slot time from 400ms to 350ms. The source-governed boundary used by OPRS is feature account `iBRL5RuWhw4yqaAZu96RUULHckHTZAoe2b77qaV38JZ`, activation slot `440208000`, and public block time `2026-08-19T05:50:49Z`.

OPRS uses this as a benchmark boundary only. It does not claim achieved slot duration, faster confirmations, lower latency, improved transaction landing, lower skip rates, tighter spreads, lower replay pressure, better catchup behavior, Blocksize readiness, or venue-level market-quality improvement.

## Public Package

The package `examples/public/slot-regime-benchmark-v0/` publishes two static windows:

- A pre-activation reference window ending at slot `440207999` with a 400ms target duration.
- A post-activation reference window starting at slot `440208000` with a 350ms target duration.

The package is intended to help future read-only measurements normalize landing, confirmation, replay, catchup, and oracle-age evidence by slot-duration regime.

## Promotion Gate

Any future measured benchmark claim must include:

1. Provider, commitment, query shape, and slot-range provenance.
2. Separate pre/post windows with compatible metric definitions.
3. Data-quality treatment for missing slots, skipped slots, provider lag, and RPC errors.
4. No signer, transaction submission, custody, capital, or live trading dependency.
5. Explicit separation between network-level observations and Drift, Jupiter, Phoenix, or Blocksize-specific claims.
