# Jupiter Perps Provenance

This document records the current Jupiter Perps target and decoder provenance status. It supports read-only target discovery, source-authorized account-layout decode, and lifecycle field planning. It does not authorize verified request/fulfillment pairing, historical replay, keeper behavior, signing, or production execution.

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

Onchain Anchor IDL and account-layout decode commands:

```bash
scripts/fetch_jupiter_onchain_idl.py --out target/oprs-jupiter-onchain-idl/latest.json
scripts/decode_jupiter_position_examples.py --out target/oprs-jupiter-position-decode/latest.json
scripts/validate_public_jupiter_onchain_decode.py
```

Confirmed:

- Jupiter Perpetuals program metadata.
- SOL/ETH/BTC/USDC/USDT custody account metadata.
- SOL/ETH/BTC/USDC/USDT documented oracle account metadata.
- Public Jupiter Perps program signatures and transaction summaries can be sampled with read-only Solana RPC.
- The live Jupiter Perps program exposes a hashable onchain Anchor IDL at `38GK1i4cQPAxqrbfKX4RRMNfXpKRn5PgLFHVJeXm1C8Y`.
- The extracted normalized IDL hash is `611de36592f4508438df16ebee2ff73b9789eda105ec712575d515b432d1ebaa`.
- Source-authorized scrubbed account-layout decode now exists for `Position` and `PositionRequest`.
- Scrubbed local output under `target/`.
- No RPC URL, key, signer, wallet, custody, capital, or transaction-submission data is printed or committed.

The transaction-history sample now emits shared-account-key lifecycle candidates as `candidate_pair_unverified` and probes shared account metadata with `getMultipleAccounts` using `dataSlice` length 0. A shared Jupiter-owned non-executable account is labeled as a stronger candidate signal, but it is intentionally not a verified request/fulfillment reconstruction. It emits `verified_request_fulfillment_pair_claimed=false`, `request_fulfillment_pair_claimed=false`, `position_request_decoded=false`, and `raw_transaction_committed=false`.

## IDL Sources

Current canonical decode authority for account-layout proof:

| Item | Value |
| --- | --- |
| Program ID | `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu` |
| Anchor IDL account | `38GK1i4cQPAxqrbfKX4RRMNfXpKRn5PgLFHVJeXm1C8Y` |
| IDL authority | `2j5nCxKzqiRBtpCq1wPtPjBy5JaCQWg28DtWnsv1o7M2` |
| IDL name / version | `perpetuals` / `0.1.0` |
| Normalized IDL SHA-256 | `611de36592f4508438df16ebee2ff73b9789eda105ec712575d515b432d1ebaa` |
| Public proof package | `examples/public/jupiter-onchain-decode-v0/` |

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

The docs-linked candidate remains useful context, but it does not match the live onchain IDL hash used for the public decode proof.

## Provenance Status

Status: `onchain_anchor_idl_hashable`.

The independent onchain Anchor IDL extraction path is reviewed, hash-pinned, and tied to the live Jupiter Perps program. OPRS may now claim source-authorized account-layout decode for the `Position` and `PositionRequest` examples in the scrubbed public package.

The docs-linked third-party IDL sample is not treated as canonical because its normalized content does not match the live onchain IDL. `JUPITER_API_KEY` can still be used only for local authenticated read-only discovery if a relevant endpoint is available. It must not be committed, deployed to the static Railway proof pack, printed in logs, or treated as lifecycle authority unless the endpoint returns or references a canonical hashable artifact.

OPRS may claim Jupiter program/custody/oracle metadata discovery, public transaction-history sampling, unverified stronger candidate labeling, and source-authorized `Position` / `PositionRequest` account-layout decode. It still must not claim verified request/fulfillment pairing, keeper behavior, historical liquidation replay, protocol safety, or production readiness.

The exact confirmation package needed to unblock verified lifecycle pairing is tracked in [Jupiter position authority confirmation](jupiter-position-authority-confirmation.md). The narrow remaining ask is whether Jupiter can confirm instruction account-role maps, request/fulfillment lifecycle semantics, and public mainnet fixture signatures for mainnet program `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu`.

## Safe Next Steps

1. Use the onchain IDL hash as the account-layout decode authority.
2. Keep live decode output under `target/` and publish only scrubbed public packages.
3. Use the transaction-history sample as the foundation for later request/fulfillment pairing, but do not claim pairing until shared `PositionRequest` / `Position` evidence is source-linked.
4. Send the narrowed lifecycle confirmation ask in [Jupiter position authority confirmation](jupiter-position-authority-confirmation.md) before promoting verified lifecycle or replay claims.
5. If a Jupiter API key is used, keep it in `.env` as `JUPITER_API_KEY` and restrict probes to read-only metadata/schema/fixture discovery.

Forbidden actions remain unchanged: no signing, no transaction submission, no priority-fee bidding, no keypair loading, no custody, no capital management, and no calls to `/order`, `/execute`, `/build`, `/submit`, auth, keeper, or RFQ/order-routing paths.
