# Phoenix Market Telemetry v0

This package records the safe public claim boundary for a Phoenix/Rise market-quality adapter spike.

It is source-backed and static. It does not include live API responses, trader state, wallet-authenticated flows, instruction builders, order routes, signing, or transaction submission.

Allowed public claims:

- Phoenix/Rise exposes public HTTP surfaces for exchange snapshots, market configuration, L2 orderbook snapshots, market statistics history, and funding history.
- Phoenix/Rise exposes typed WebSocket adapters for live L2 market data.
- These surfaces are suitable for future read-only market-quality telemetry such as spread, depth, stale-book, funding, and latency checks.

Blocked claims:

- Trader state is decoded or monitored.
- Historical replay is ready.
- Order, cancel, wallet-authenticated, instruction-builder, signing, or transaction-submission paths are supported.
