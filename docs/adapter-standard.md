# Adapter Standard

Protocol adapters isolate venue-specific account layouts, event formats, and margin logic behind stable read-only interfaces. Core services consume canonical types, not venue-native accounts.

## Required Metadata

Adapters must declare:

- Protocol name.
- Program IDs.
- Network.
- Adapter version.
- Account schema and IDL hash where available.
- Supported markets.
- Oracle dependencies.
- Capability level: `read_only`, `simulate`, or `execute_disabled`.
- Known caveats.
- Data quality confidence.

## Required Interfaces

```text
VenueAdapter
  metadata()
  capabilities()
  markets()
  oracle_feeds(market_id)
  positions(query)
  margin_state(position, oracle)
  liquidation_state(input)
  build_dry_run_liquidation(input)
  decode_event(input)
  fixture_loader()

OracleAdapter
  latest(feed)
  validate(snapshot, policy)
  confidence_adjusted_price(snapshot, side)
  divergence(input)

SimulationAdapter
  required_accounts(plan)
  simulate(plan, fixture)
  classify_failure(result)
```

## Capability Rules

Phase v0 allows only read-only and dry-run/simulate capabilities. `execute` must remain unimplemented. Adapters must not accept signers, private keys, wallets, custody handles, capital allocations, or live transaction submission endpoints.

## First Adapter Path

Build order:

1. `DriftReadOnlyAdapter`: first full perps adapter.
2. `PhoenixOrderbookAdapter`: price-discovery companion.
3. `JupiterPerpsReadOnlyAdapter`: oracle/pool/keeper contrast.
4. `FlashTrade` or `GMTrade`: second pool-perps venue.
5. `PacificaApiAdapter`: commercial/API data track.
