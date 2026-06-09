# Drift Decoder Provenance

This document pins the public Drift sources used for the current read-only metadata proof and narrow public-field decode. It does not claim user-state, market economics, or replay-ready account decoding.

## Pinned Source

| Item | Value |
| --- | --- |
| Repository | `drift-labs/protocol-v2` |
| Commit | `0ae3e3b1db782a6765c3525b3dec38ad4d9d3a62` |
| Commit message | `sdk: release v2.163.0-beta.0` |
| SDK version | `2.163.0-beta.0` |
| Drift IDL blob SHA | `9646dd6a893568d85d8dc47507e047010bf7e945` |

## Source Files

- PDA helpers: `https://github.com/drift-labs/protocol-v2/blob/0ae3e3b1db782a6765c3525b3dec38ad4d9d3a62/sdk/src/addresses/pda.ts`
- Perp market constants: `https://github.com/drift-labs/protocol-v2/blob/0ae3e3b1db782a6765c3525b3dec38ad4d9d3a62/sdk/src/constants/perpMarkets.ts`
- Spot market constants: `https://github.com/drift-labs/protocol-v2/blob/0ae3e3b1db782a6765c3525b3dec38ad4d9d3a62/sdk/src/constants/spotMarkets.ts`
- Drift IDL: `https://github.com/drift-labs/protocol-v2/blob/0ae3e3b1db782a6765c3525b3dec38ad4d9d3a62/sdk/src/idl/drift.json`
- Account fetch helpers: `https://github.com/drift-labs/protocol-v2/blob/0ae3e3b1db782a6765c3525b3dec38ad4d9d3a62/sdk/src/accounts/fetch.ts`
- Perp market state: `https://github.com/drift-labs/protocol-v2/blob/0ae3e3b1db782a6765c3525b3dec38ad4d9d3a62/programs/drift/src/state/perp_market.rs`
- Spot market state: `https://github.com/drift-labs/protocol-v2/blob/0ae3e3b1db782a6765c3525b3dec38ad4d9d3a62/programs/drift/src/state/spot_market.rs`
- Paused operation bitsets: `https://github.com/drift-labs/protocol-v2/blob/0ae3e3b1db782a6765c3525b3dec38ad4d9d3a62/programs/drift/src/state/paused_operations.rs`

## Current Proof Level

Current local command:

```bash
scripts/discover_drift_readonly_state.py --out target/oprs-drift-readonly-state/latest.json
```

Optional shape snapshot command:

```bash
scripts/discover_drift_readonly_state.py --include-shape-snapshot --out target/oprs-drift-readonly-state/latest-shape.json
scripts/discover_drift_readonly_state.py --include-public-fields --out target/oprs-drift-readonly-state/latest-public-fields.json
```

Confirmed:

- Drift state PDA derivation and metadata read.
- SOL/BTC/ETH perp market PDA derivation and metadata reads.
- USDC/SOL spot market PDA derivation and metadata reads.
- Deduplicated oracle metadata reads for those selected markets.
- Optional shape snapshots for Drift state, selected perp markets, and selected spot markets.
- Optional public-field decode for State admin/signer, selected PerpMarket identity/oracle/metadata/guardrail fields, and selected SpotMarket identity/metadata/guardrail fields.
- Source-backed semantic labels for selected `PerpMarket` and `SpotMarket` guardrails, including market status, contract type/tier, asset tier, and pause bitsets.
- Scrubbed local output under `target/`.
- No RPC URL, key, signer, wallet, custody, capital, or transaction-submission data is printed or committed.

Not yet claimed:

- Binary account decoding.
- Historical liquidation replay.
- User account or pre-state reconstruction.
- Jupiter Perps binary account decode.

## Shape Snapshot Scope

The optional shape snapshot mode fetches account bytes through read-only RPC, uses them in memory, and emits only:

- expected IDL account type
- expected and observed Anchor account discriminator
- discriminator match result
- account data length
- account data SHA-256
- owner/executable metadata
- explicit `raw_account_data_committed=false`, `field_decode_claimed=false`, and `replay_ready=false`

Raw account bytes are not written to output.

## Public Field Decode Scope

The optional public-field mode is intentionally limited to selected public identity, oracle identity, spot metadata, and guardrail fields with simple, pinned offsets:

- `State.admin` and `State.signer`
- `PerpMarket.pubkey`, `PerpMarket.amm.oracle`, `PerpMarket.market_index`, `PerpMarket.status`, `PerpMarket.contract_type`, `PerpMarket.contract_tier`, and `PerpMarket.paused_operations`
- `SpotMarket.pubkey`, `SpotMarket.oracle`, `SpotMarket.mint`, `SpotMarket.vault`, `SpotMarket.name`, `SpotMarket.decimals`, `SpotMarket.market_index`, `SpotMarket.orders_enabled`, `SpotMarket.status`, `SpotMarket.asset_tier`, `SpotMarket.paused_operations`, `SpotMarket.if_paused_operations`, and `SpotMarket.pool_id`

The command validates expected PDA, oracle, mint, symbol, decimals, market-index, and pool-id values where the selected target already has a public source. It also labels selected guardrail fields from pinned Drift Rust source:

- `status`: `MarketStatus` enum labels from `perp_market.rs`
- `contract_type`: `ContractType` enum labels from `perp_market.rs`
- `contract_tier`: `ContractTier` enum labels from `perp_market.rs`
- `asset_tier`: `AssetTier` enum labels from `spot_market.rs`
- `PerpMarket.paused_operations`: `PerpOperation` bitset labels from `paused_operations.rs`
- `paused_operations`: `SpotOperation` bitset labels from `paused_operations.rs`
- `if_paused_operations`: `InsuranceFundOperation` bitset labels from `paused_operations.rs`

It still emits `user_state_decoded=false`, `market_economics_decoded=false`, and `replay_ready=false`.

## Next Safe Decode Step

The next decode command should stay deliberately narrow:

1. Fetch account data through read-only RPC.
2. Decode only the account discriminator and IDL account type first.
3. Decode additional public market fields only after field offsets are validated against the pinned IDL or SDK decoder.
4. Emit decoded fields into `target/` only until scrub review passes.
5. Keep `decoded_snapshot` separate from `replay_ready`; do not claim replay readiness from a market/account snapshot alone.

Forbidden actions remain unchanged: no signing, no transaction submission, no priority-fee bidding, no keypair loading, no custody, and no capital management.
