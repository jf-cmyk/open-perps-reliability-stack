# Jupiter Perps Provenance

This document records the current Jupiter Perps target and decoder provenance status. It supports read-only target discovery and field planning but does not yet authorize binary decode claims.

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
| Jupiter CLI perps guide | `https://github.com/jup-ag/cli/blob/main/docs/perps.md` |
| Source-authority audit | `jupiter-source-authority-audit.md` |
| Position authority confirmation ask | `jupiter-position-authority-confirmation.md` |

## Current Target Proof

Current local command:

```bash
scripts/discover_jupiter_perps_readonly_targets.py --out target/oprs-jupiter-perps-readonly-targets/latest.json
```

Read-only transaction-history sample command:

```bash
scripts/discover_jupiter_perps_transaction_history.py --limit 10 --transaction-limit 6 --min-shared-keys 2 --out target/oprs-jupiter-perps-transaction-history/latest-pairs.json
```

Confirmed:

- Jupiter Perpetuals program metadata.
- SOL/ETH/BTC/USDC/USDT custody account metadata.
- SOL/ETH/BTC/USDC/USDT documented oracle account metadata.
- Public Jupiter Perps program signatures and transaction summaries can be sampled with read-only Solana RPC.
- Scrubbed local output under `target/`.
- No RPC URL, key, signer, wallet, custody, capital, or transaction-submission data is printed or committed.

The transaction-history sample now emits shared-account-key lifecycle candidates as `candidate_pair_unverified` and probes shared account metadata with `getMultipleAccounts` using `dataSlice` length 0. A shared Jupiter-owned non-executable account is labeled as a stronger candidate signal, but it is intentionally not a verified request/fulfillment reconstruction. It emits `verified_request_fulfillment_pair_claimed=false`, `request_fulfillment_pair_claimed=false`, `position_request_decoded=false`, and `raw_transaction_committed=false`.

## IDL Candidate

Jupiter's custody-account docs link to a sample repository for working with the Jupiter Perps IDL:

| Item | Value |
| --- | --- |
| Repository | `julianfssen/jupiter-perps-anchor-idl-parsing` |
| Repository URL | `https://github.com/julianfssen/jupiter-perps-anchor-idl-parsing` |
| Current inspected commit | `630cfd72cad499f45453a53383d7ac6d3e09e022` |
| Commit message | `Add examples on swaps and mint/burn` |
| Commit verification | `unsigned` |
| IDL path | `src/idl/jupiter-perpetuals-idl.ts` |
| IDL Git blob SHA | `e7f21c9c44b077d0d10116305b97bbc152081b77` |
| IDL content SHA-256 | `8a150cee26dc07c040ca7c1640dc7ec36ba9a0f063923ec50b2438e306b19cab` |
| IDL source URL | `https://github.com/julianfssen/jupiter-perps-anchor-idl-parsing/blob/630cfd72cad499f45453a53383d7ac6d3e09e022/src/idl/jupiter-perpetuals-idl.ts` |

## Provenance Status

Status: `docs_linked_example_not_canonical`.

The docs-linked IDL sample is useful for research and field planning, but it should remain a candidate. It does not authorize binary decode claims until one of these is true:

- Jupiter publishes or confirms a canonical Perps IDL/source revision.
- The docs-linked IDL is explicitly confirmed as canonical for the current onchain program.
- An independent onchain/program-IDL extraction path is reviewed and hashed.
- A Jupiter-confirmed API endpoint returns canonical schema/IDL/source metadata with a stable version, checksum, or hashable artifact tied to the live program.

`JUPITER_API_KEY` can be used only for local authenticated read-only discovery if a relevant endpoint is available. It must not be committed, deployed to the static Railway proof pack, printed in logs, or treated as source authority unless the endpoint returns or references a canonical hashable artifact.

Until then, OPRS may claim Jupiter program/custody/oracle metadata discovery, public transaction-history sampling, and unverified stronger candidate labeling, but not Jupiter binary account decoding, verified request/fulfillment pairing, or historical replay.

The exact confirmation package needed to unblock `Position` / `PositionRequest` decode and pairing is tracked in [Jupiter position authority confirmation](jupiter-position-authority-confirmation.md). The narrow ask is whether Jupiter can confirm canonical source authority for mainnet program `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu`, including the two account layouts and lifecycle semantics.

## Safe Next Steps

1. Use the docs-linked IDL only to plan candidate public fields.
2. Keep any decode experiment under `target/` until source authority is resolved.
3. Start with account discriminator/type, data length, owner, and documented public fields only.
4. Use the transaction-history sample as the foundation for later request/fulfillment pairing, but do not claim pairing until shared PositionRequest/Position evidence is linked.
5. Send the confirmation ask in [Jupiter position authority confirmation](jupiter-position-authority-confirmation.md) before promoting any Jupiter account decode claim.
6. If a Jupiter API key is used, keep it in `.env` as `JUPITER_API_KEY` and restrict probes to read-only metadata/schema discovery.

Forbidden actions remain unchanged: no signing, no transaction submission, no priority-fee bidding, no keypair loading, no custody, no capital management, and no calls to `/order`, `/execute`, `/build`, `/submit`, auth, keeper, or RFQ/order-routing paths.
