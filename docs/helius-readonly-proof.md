# Helius Read-Only Proof Plan

This document defines the next read-only proof layer for Open Perps Reliability Stack. It turns Helius-backed Solana reads into scrubbed, reproducible evidence without signing, custody, transaction submission, priority-fee bidding, or capital deployment.

## Current Status

Local Helius access is confirmed for the first read-only target discovery command:

```bash
scripts/discover_readonly_targets.py --out target/oprs-readonly-target-discovery/latest.json
```

The command writes a scrubbed report under `target/`, confirms that the RPC credential was not printed, probes Drift's public program account metadata, and records Jupiter/Phoenix follow-on target lanes. Live output stays local and is not committed.

## Scope Boundary

Allowed:

- `getSlot`
- `getAccountInfo`
- read-only transaction/account history methods
- public account metadata
- public signatures, slots, block times, program IDs, logs, decoded instruction summaries, and provider provenance
- scrubbed data reconstruction envelopes

Forbidden:

- signing
- live transaction submission
- retry loops
- priority-fee bidding
- block-engine submission
- keypair or wallet loading
- custody, inventory, or capital management
- private keeper/searcher logs
- private RPC URLs, API keys, request headers, webhook secrets, or route labels

## Evidence Model

Every read-only proof should emit:

- provider label
- commitment
- slot range
- query config
- target protocol and account type
- parser/decoder version when available
- transaction-version support
- evidence refs that are relative public paths only
- source limitations
- known gaps
- explicit proof status

Proof statuses:

- `target_discovered`: public target exists and can be read.
- `decode_ready`: target shape and decoder source are identified.
- `decoded_snapshot`: account or transaction was decoded into public-safe fields.
- `replay_ready`: evidence is sufficient for deterministic dry-run/replay.
- `deferred`: target needs public source resolution or a safer evidence path.

## Drift Proof Sequence

Drift is first because it has public documentation for program accounts, markets, user state, liquidations, and oracle guardrails.

1. Program account discovery.
   - Target: Drift program account.
   - Current status: `target_discovered`.
   - Evidence: executable flag, owner, lamports, context slot.

2. Market and oracle state target resolution.
   - Resolve public `State`, `PerpMarketAccount`, `SpotMarketAccount`, and oracle accounts from official docs, SDK, or public registries.
   - Record target source and update timestamp.

3. Read-only account snapshots.
   - Fetch public account data with commitment and context slot.
   - Store only scrubbed metadata or decoded public fields.

4. Decoder and schema provenance.
   - Record adapter version, IDL/source version where available, supported account schema version, and parser caveats.

5. Dry-run readiness.
   - Mark replay as `replay_ready` only when account snapshots, oracle state, slot range, and known gaps are sufficient to explain a deterministic fixture or historical event.

## Jupiter Perps Proof Sequence

Jupiter Perps is second because its trader-to-LP/JLP model is structurally different from Drift and useful for public reliability comparison.

1. Public target resolution.
   - Resolve pool, custody, oracle, and relevant program/account targets from official Jupiter docs or public source references.
   - Current status: `deferred` until public targets are resolved.

2. Lifecycle evidence model.
   - Treat Jupiter flows as request and fulfillment lifecycle evidence, not only as a final signature.
   - Record request transaction, keeper fulfillment transaction, oracle selection/fallback context where public, custody state, and liquidation-price relation when reconstructable.

3. Public-safe output.
   - Publish only public signatures, slots, account addresses, decoded state summaries, and explicit caveats.
   - Do not publish private API routes, keeper internals, market-maker/RFQ secrets, or authenticated request headers.

## Continuity And Gap Proof

For each proof run, record:

- start slot and end slot
- commitment
- RPC methods
- address filters
- transaction detail level
- max supported transaction version
- unsupported transaction-version count
- missing slot or stream-gap count when available
- provider retention boundary if known

If using a stream or replay provider later, the proof must distinguish:

- complete window
- partial window
- provider-retention limited
- parser-limited
- target-resolution limited

## Public Proof-Pack Rules

Safe to include publicly:

- public account addresses
- public signatures
- slots and block times
- public program IDs
- decoded public account summaries
- scrubbed data reconstruction envelopes
- provider labels without full URLs
- source links to official docs

Do not include:

- API keys
- RPC URLs
- webhook secrets
- request headers
- private route labels
- signer or wallet metadata
- customer labels
- capital settings
- operational retry/bidding instructions

## Next Implementation Tasks

1. Resolve Drift market/oracle account targets from official public sources.
2. Add a second read-only discovery mode for Drift market/oracle snapshots.
3. Resolve Jupiter Perps public pool/custody/oracle targets.
4. Extend the data reconstruction envelope example to represent `target_discovered` and `decoded_snapshot` proof states.
5. Keep all live outputs under `target/` until scrubbed examples are reviewed for public release.
