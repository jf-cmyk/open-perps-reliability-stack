# Jupiter Perps Provenance

This document records the current Jupiter Perps target and decoder provenance status. It supports read-only target discovery but does not yet authorize binary decode claims.

## Official Target Sources

| Item | Source |
| --- | --- |
| Jupiter Perpetuals program ID | `https://developers.jup.ag/docs/get-started/index` |
| Oracle model and oracle account addresses | `https://docs.jup.ag/user-docs/trade/perps-and-jlp/technical-reference` |
| Custody account addresses and field descriptions | `https://docs.jup.ag/user-docs/trade/perps-and-jlp/technical-reference` |
| Custody account field guide | `https://developers.jup.ag/docs/perps/custody-account` |
| Pool account field guide | `https://developers.jup.ag/docs/perps/pool-account` |
| Position account field guide | `https://developers.jup.ag/docs/perps/position-account` |
| PositionRequest account field guide | `https://developers.jup.ag/docs/perps/position-request-account` |

## Current Target Proof

Current local command:

```bash
scripts/discover_jupiter_perps_readonly_targets.py --out target/oprs-jupiter-perps-readonly-targets/latest.json
```

Confirmed:

- Jupiter Perpetuals program metadata.
- SOL/ETH/BTC/USDC/USDT custody account metadata.
- SOL/ETH/BTC/USDC/USDT documented oracle account metadata.
- Scrubbed local output under `target/`.
- No RPC URL, key, signer, wallet, custody, capital, or transaction-submission data is printed or committed.

## IDL Candidate

Jupiter's custody-account docs link to a sample repository for working with the Jupiter Perps IDL:

| Item | Value |
| --- | --- |
| Repository | `julianfssen/jupiter-perps-anchor-idl-parsing` |
| Repository URL | `https://github.com/julianfssen/jupiter-perps-anchor-idl-parsing` |
| Current inspected commit | `630cfd72cad499f45453a53383d7ac6d3e09e022` |
| Commit message | `Add examples on swaps and mint/burn` |
| IDL path | `src/idl/jupiter-perpetuals-idl.ts` |
| IDL blob SHA | `e7f21c9c44b077d0d10116305b97bbc152081b77` |
| IDL source URL | `https://github.com/julianfssen/jupiter-perps-anchor-idl-parsing/blob/630cfd72cad499f45453a53383d7ac6d3e09e022/src/idl/jupiter-perpetuals-idl.ts` |

## Provenance Status

Status: `target_discovered_not_binary_decoded`.

The docs-linked IDL sample is useful for research and field planning, but it should remain a candidate until one of these is true:

- Jupiter publishes or confirms a canonical Perps IDL/source revision.
- The docs-linked IDL is explicitly confirmed as canonical for the current onchain program.
- An independent onchain/program-IDL extraction path is reviewed and hashed.

Until then, OPRS may claim Jupiter program/custody/oracle metadata discovery, but not Jupiter binary account decoding or historical replay.

## Safe Next Steps

1. Use the docs-linked IDL only to plan candidate public fields.
2. Keep any decode experiment under `target/` until source authority is resolved.
3. Start with account discriminator/type, data length, owner, and documented public fields only.
4. Keep request/fulfillment proof separate from account decode; it needs public transaction-history evidence.

Forbidden actions remain unchanged: no signing, no transaction submission, no priority-fee bidding, no keypair loading, no custody, no capital management, and no calls to `/order`, `/execute`, `/build`, `/submit`, auth, keeper, or RFQ/order-routing paths.
