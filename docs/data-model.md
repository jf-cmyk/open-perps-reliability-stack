# Data Model

Data v0 keeps raw chain evidence immutable, normalizes perps events into typed tables, and publishes scrubbed public datasets with reproducible lineage.

## Storage Layers

- `bronze`: raw Solana transactions, account snapshots, oracle payloads, adapter decode attempts, and job manifests.
- `silver`: normalized perps events and typed facts.
- `gold`: public aggregates for dashboard/API/datasets.
- `control`: adapter registry, backfill jobs, manifests, and publish state.

## Canonical Entities

- `protocol`: venue/program family, program IDs, adapter status, capability.
- `market`: protocol market, base/quote/index asset, market type, oracle feed IDs.
- `asset`: mint, symbol, decimals, stablecoin flag, public metadata.
- `price_feed`: provider, feed account/id, confidence/staleness rules.
- `position_snapshot`: margin, collateral, size, side, liquidation state.
- `order_event`: placed, cancelled, amended, expired.
- `fill_event`: maker/taker, price, quantity, fee, slot/signature.
- `funding_event`: funding rate, payment, update.
- `liquidation_event`: candidate or executed liquidation.
- `oracle_snapshot`: price, confidence, exponent, publish time, slot.
- `dry_run_decision`: simulated opportunity with reason codes and no signing.
- `execution_reliability_event`: observed landed/failed/expired/delayed outcomes.
- `adapter_health_event`: decode success, stale slots, schema mismatch, missing accounts.

## Canonical Event Envelope

Every normalized row must include:

```text
event_id
schema_version
adapter_name
adapter_version
chain_id
protocol
program_id
market_id
event_type
event_subtype
slot
block_time
signature
instruction_index
inner_index
actor
subject_account
source_account_keys
raw_ref
raw_hash
decode_status
quality_flags
attrs_json
created_at
```

`event_id = sha256(chain_id|protocol|program_id|signature|instruction_index|inner_index|event_type|event_subtype|adapter_version)`.

## Core Tables

- `perps_events`
- `perps_oracle_snapshots`
- `perps_positions_snapshot`
- `perps_fills`
- `perps_orders`
- `perps_funding`
- `perps_liquidations`
- `perps_dry_run_decisions`
- `adapter_registry`
- `dataset_manifest`

Gold aggregates:

- `market_quality_1m`
- `oracle_risk_1m`
- `liquidation_health_daily`
- `adapter_health_daily`
- `execution_reliability_1m`

## Backfill Strategy

1. Register adapter metadata: protocol, program IDs, IDL hash, schemas, supported event types.
2. Fetch raw data by bounded slot/date chunks; persist state after every chunk.
3. Decode raw transactions/accounts into adapter-local events.
4. Normalize to canonical envelope and typed fact tables.
5. Join oracle snapshots by nearest valid publish time/slot.
6. Run data quality checks and write `dataset_manifest`.
7. Publish only scrubbed, quality-passing partitions.
8. Never require private keys, signing, or transaction submission.

## Public Dataset Format

Publish partitioned Parquet plus small CSV samples:

```text
datasets/perps/v0/protocol=drift/event_type=fills/date=2026-06-01/*.parquet
datasets/perps/v0/protocol=drift/event_type=oracle_snapshots/date=2026-06-01/*.parquet
datasets/perps/v0/manifests/date=2026-06-01/manifest.json
```

Manifest fields:

- Manifest version and dataset name.
- Schema version, protocol, chain ID, and adapter version.
- Event types and source window.
- Source slot range where applicable.
- Partition paths.
- Row count, distinct event count, and raw ref count.
- Raw hash algorithm, root checksum, and content checksums.
- Data quality status and DQ results reference.
- Quality score.
- Known gaps and source limitations.
- Scrub policy version.
- Generated timestamp and generator identity.

## Data Quality Checks

- No duplicate `event_id`.
- No null `signature`, `slot`, `protocol`, or `event_type`.
- Raw hash present for every public row.
- Decode failure rate by protocol/day.
- Missing slot range detector.
- Oracle staleness and confidence flags.
- Fill price sanity against oracle/index price.
- Position/open-interest reconciliation where venue accounts permit.
- Liquidation candidate reason code present.
- Dry-run rows include `simulation_status`.
- Public export checksum matches manifest.

Severity levels: `block_publish`, `warn_public`, `internal_only`.

## Sensitive-Data Scrubbing

Scrub before public release:

- RPC URLs, API keys, bearer tokens, env names, internal hostnames.
- Absolute local file paths.
- Private route labels, RPC/vendor route performance, validator internals.
- Private profile mappings and commercial customer labels.
- Strategy thresholds, capital limits, execution policy.
- Signer, wallet inventory, or custody metadata.

Wallet addresses from public chain data may remain, but labels must be generic unless independently public.
