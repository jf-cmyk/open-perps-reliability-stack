# Architecture v0

The Open Perps Reliability Stack is read-only and dry-run infrastructure for Solana onchain perps. It provides protocol adapters, normalized market data, Pyth-aware risk tooling, liquidation replay/dry-run, execution reliability analytics, public APIs, and dashboard views.

Out of scope: production execution, signing, custody, live capital deployment, autonomous trading, private-key handling, and live liquidation submission.

## System Map

- Solana RPC/Geyser/data providers: raw account, transaction, slot, and log sources.
- Pyth: price, confidence, exponent, publish time, and freshness.
- Protocol adapters: venue-specific decoding and risk inputs.
- Data layer: normalized market, oracle, position, liquidation, and reliability data.
- Risk SDK: Pyth-aware validation, margin helpers, liquidation thresholds, and stress tests.
- Dry-run engine: candidate detection, replay, classification, and unsigned transaction plans.
- Public API: read-only REST/WebSocket/query surface.
- Dashboard: public operational views for market quality, oracle risk, liquidation health, adapter health, and reliability.

## Module Map

```text
crates/
  oprs-core
  oprs-adapter
  oprs-risk
  oprs-data
  oprs-replay
  oprs-dry-run
  oprs-api-types

adapters/
  fixture
  drift-readonly
  jupiter-perps-readonly
  phoenix-readonly

services/
  ingest-service
  indexer-service
  oracle-risk-service
  dry-runner-service
  reliability-service
  public-api-service

apps/
  dashboard

schemas/
  events
  api
  datasets

datasets/
  sample
```

## Component Boundaries

### Ingest Service

Owns raw observations only: slots, account snapshots, transaction logs, program events, and oracle updates. It does not compute trading decisions.

### Indexer Service

Owns normalized protocol data: markets, fills, funding, positions, open interest, depth, spreads, liquidation events, adapter health, and decode quality.

### Oracle Risk Service

Owns Pyth-aware risk snapshots: stale feeds, confidence width, publish-time lag, missing feeds, oracle/orderbook divergence, and circuit-breaker flags.

### Dry-Runner Service

Owns liquidation candidate detection, replay, profitability estimates, failure classification, and unsigned simulation plans. It must not sign or submit transactions.

### Reliability Service

Owns observed execution analytics: landed, failed, expired, delayed, fee range, compute budget, account lock, blockhash, RPC, and route labels where safe to publish.

### Public API Service

Owns read-only access to normalized data and aggregate metrics. It must not expose privileged execution endpoints.

### Dashboard

Owns public views only. It must not expose private strategy, private routes, keys, wallet balances, capital allocations, or live execution controls.

## Public Dashboard Views

- Market Quality: spread, depth, open interest, volume, funding, venue health.
- Oracle Risk: confidence, staleness, divergence, missing feed alerts.
- Liquidation Health: candidates, replay outcomes, reason-code distribution.
- Execution Reliability: aggregate landing/failure taxonomy from observed data only.
- Adapter Health: decode success, stale slots, schema mismatch, missing accounts.

## Architecture Risks

- Adapter ambiguity or account schema drift.
- Perps-specific historical fixture scarcity.
- License contamination from BUSL/private Express Relay components.
- Public leakage of private execution strategy.
- Dashboard/API endpoints accidentally implying trade recommendations.
- Scope creep from dry-run into production execution.
