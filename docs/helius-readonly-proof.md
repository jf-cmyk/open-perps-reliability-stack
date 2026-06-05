# Helius Read-Only Proof Plan

This document defines the next read-only proof layer for Open Perps Reliability Stack. It turns Helius-backed Solana reads into scrubbed, reproducible evidence without signing, custody, transaction submission, priority-fee bidding, or capital deployment.

## Current Status

Local Helius access is confirmed for the first read-only target discovery command:

```bash
scripts/discover_readonly_targets.py --out target/oprs-readonly-target-discovery/latest.json
```

The command writes a scrubbed report under `target/`, confirms that the RPC credential was not printed, probes Drift's public program account metadata, and records Jupiter/Phoenix follow-on target lanes. Live output stays local and is not committed.

Drift state, market, and oracle metadata discovery is also confirmed:

```bash
scripts/discover_drift_readonly_state.py --out target/oprs-drift-readonly-state/latest.json
scripts/discover_drift_readonly_state.py --include-shape-snapshot --out target/oprs-drift-readonly-state/latest-shape.json
```

This second command derives public Drift PDAs from pinned official SDK source, probes the Drift state account, SOL/BTC/ETH perp market accounts, USDC/SOL spot market accounts, and the deduplicated oracle accounts with `getAccountInfo` data slices. Its optional shape snapshot mode fetches selected account bytes in memory and emits only discriminator, account type, account-data length, and account-data hash evidence. It emits a scrubbed local report under `target/`, keeps the Helius RPC URL local-only, and does not claim decoded market fields or historical liquidation replay.

Decoder provenance is pinned in [Drift decoder provenance](drift-decoder-provenance.md).

Jupiter Perps program, custody, and oracle metadata discovery is confirmed:

```bash
scripts/discover_jupiter_perps_readonly_targets.py --out target/oprs-jupiter-perps-readonly-targets/latest.json
scripts/discover_jupiter_perps_transaction_history.py --out target/oprs-jupiter-perps-transaction-history/latest.json
```

The target command resolves targets from current official Jupiter docs, probes the Jupiter Perpetuals program account, SOL/ETH/BTC/USDC/USDT custody accounts, and documented oracle accounts through `getAccountInfo` data slices. The transaction-history command samples public program signatures with `getSignaturesForAddress` and transaction summaries with `getTransaction`. Both emit scrubbed local output under `target/`, keep the Helius RPC URL local-only, and do not claim binary account decoding, request/fulfillment pairing, or liquidation replay.

Jupiter IDL/source status is tracked in [Jupiter Perps provenance](jupiter-perps-provenance.md). The current docs-linked IDL sample is useful as a candidate, but not yet sufficient for `decoded_snapshot` claims.

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
   - Current status: `target_discovered` for Drift state, SOL/BTC/ETH perp market accounts, USDC/SOL spot market accounts, and deduplicated oracle accounts.
   - Evidence: derived PDA, bump, executable flag, owner, lamports, rent epoch, and context slot.

3. Read-only account snapshots.
   - Fetch public account data with commitment and context slot.
   - Current status: `shape_snapshot_only` for Drift state, SOL/BTC/ETH perp market accounts, and USDC/SOL spot market accounts.
   - Store only scrubbed metadata, account-shape evidence, or decoded public fields after offset validation.

4. Decoder and schema provenance.
   - Record adapter version, IDL/source version where available, supported account schema version, and parser caveats.

5. Dry-run readiness.
   - Mark replay as `replay_ready` only when account snapshots, oracle state, slot range, and known gaps are sufficient to explain a deterministic fixture or historical event.

## Jupiter Perps Proof Sequence

Jupiter Perps is second because its trader-to-LP/JLP model is structurally different from Drift and useful for public reliability comparison.

1. Public target resolution.
   - Resolve pool, custody, oracle, and relevant program/account targets from official Jupiter docs or public source references.
   - Current status: `target_discovered` for the Jupiter Perpetuals program account, documented SOL/ETH/BTC/USDC/USDT custody accounts, and documented oracle accounts.
   - Evidence: official docs source refs, executable flag, owner, lamports, rent epoch, and context slot.

2. Lifecycle evidence model.
   - Treat Jupiter flows as request and fulfillment lifecycle evidence, not only as a final signature.
   - Current status: `transaction_history_sample_only` for public program signatures and structural transaction summaries.
   - Next status requires linking request transaction, fulfillment transaction, oracle selection/fallback context where public, custody state, and liquidation-price relation when reconstructable.

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

1. Add a binary decode-safe snapshot mode for Drift account discriminator, IDL account type, and public market fields only.
2. Pin canonical Jupiter Perps IDL/source provenance before any Jupiter `decoded_snapshot` claim.
3. Add Jupiter request/fulfillment lifecycle evidence using public transaction history only.
4. Extend the data reconstruction envelope example to represent `decoded_snapshot` and `replay_ready` proof states.
5. Keep all live outputs under `target/` until scrubbed examples are reviewed for public release.
