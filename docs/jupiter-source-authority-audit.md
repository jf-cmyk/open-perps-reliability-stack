# Jupiter Source Authority Audit

This note records the current Jupiter Perps source-authority boundary for OPRS. It supports target discovery, field planning, and source-authorized `Position` / `PositionRequest` account-layout decode. It does not authorize verified lifecycle pairing, historical replay, keeper behavior, signing, or production execution.

## Audited Sources

| Source | Status | Use |
| --- | --- | --- |
| Jupiter technical reference | Official docs | Request/fulfillment model, oracle model, custody addresses, and external IDL example reference. |
| Jupiter Position account guide | Official docs | Public Position field planning and derivation context. |
| Jupiter PositionRequest account guide | Official docs | Public PositionRequest field planning, request lifecycle, and closure/execution context. |
| Live Anchor IDL account | Onchain program-owned artifact | Canonical account-layout authority for scrubbed `Position` and `PositionRequest` decode proof. |
| `julianfssen/jupiter-perps-anchor-idl-parsing` | Docs-linked example repo | Candidate Anchor IDL and TypeScript examples only. |
| Jupiter position authority confirmation ask | OPRS confirmation checklist | Exact evidence still needed before verified lifecycle pairing or replay. |
| Jupiter API key | Optional authenticated discovery input | Not lifecycle authority unless it returns or references a Jupiter-confirmed hashable source, account-role map, or fixture artifact tied to the live program. |

## Current Onchain IDL Authority

| Item | Value |
| --- | --- |
| Program ID | `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu` |
| Anchor IDL account | `38GK1i4cQPAxqrbfKX4RRMNfXpKRn5PgLFHVJeXm1C8Y` |
| IDL authority | `2j5nCxKzqiRBtpCq1wPtPjBy5JaCQWg28DtWnsv1o7M2` |
| IDL name / version | `perpetuals` / `0.1.0` |
| Normalized IDL SHA-256 | `611de36592f4508438df16ebee2ff73b9789eda105ec712575d515b432d1ebaa` |
| Status | `onchain_anchor_idl_hashable` |

## Current Docs-Linked IDL Candidate

| Item | Value |
| --- | --- |
| Repository | `julianfssen/jupiter-perps-anchor-idl-parsing` |
| Current main commit | `630cfd72cad499f45453a53383d7ac6d3e09e022` |
| Commit message | `Add examples on swaps and mint/burn` |
| Commit verification | `unsigned` |
| IDL path | `src/idl/jupiter-perpetuals-idl.ts` |
| Git blob SHA | `e7f21c9c44b077d0d10116305b97bbc152081b77` |
| IDL content SHA-256 | `8a150cee26dc07c040ca7c1640dc7ec36ba9a0f063923ec50b2438e306b19cab` |
| IDL source URL | `https://github.com/julianfssen/jupiter-perps-anchor-idl-parsing/blob/630cfd72cad499f45453a53383d7ac6d3e09e022/src/idl/jupiter-perpetuals-idl.ts` |

## Authority Decision

Status: `onchain_anchor_idl_hashable`.

Allowed:

- Use official docs for target discovery and lifecycle model language.
- Use the live onchain Anchor IDL for source-authorized account-layout decode of `Position` and `PositionRequest`.
- Use the docs-linked IDL candidate only as historical context because it does not match the live onchain IDL hash.
- Keep shared-account lifecycle candidates as `candidate_pair_unverified`.
- Use `JUPITER_API_KEY` only for local read-only discovery if a Jupiter API endpoint is confirmed to be relevant.

Blocked:

- Verified request/fulfillment pair claims.
- Liquidation replay claims.
- Treating API-key access alone as source authority.
- Keeper behavior, signing, transaction submission, custody, or production execution claims.

## Reproducible Audit Command

```bash
scripts/audit_jupiter_source_authority.py --out target/oprs-jupiter-source-authority/latest.json
```

The command uses public HTTPS only. It does not load `HELIUS_RPC_URL`, wallet state, signers, keypairs, custody, or private API routes.

## API-Key Boundary

If a Jupiter API key is available, store it only in `.env` as `JUPITER_API_KEY` and keep it out of public artifacts, Railway static hosting variables, screenshots, logs, and chat. It may support authenticated read-only discovery, but OPRS should promote it to lifecycle or fixture authority only if the response itself is a hashable Jupiter-confirmed artifact or points to one with stable versioning.

## Unlock Criteria

The account-layout decode authority is resolved for the checked `Position` and `PositionRequest` package. One of these must happen before OPRS can claim verified lifecycle pairing or replay:

1. Jupiter publishes or confirms instruction account-role maps for the current program.
2. Jupiter provides public mainnet fixture signatures and expected decoded before/after state.
3. A source-reviewed transaction-history reconstruction proves request/fulfillment linkage against the onchain IDL and public transactions.

For `Position` / `PositionRequest` specifically, OPRS now has discriminator, account size, field order, offsets, selected field types, enum layouts, and bump/counter encoding from the onchain IDL and scrubbed local decode. Verified pairing still needs source-backed instruction account-role maps, lifecycle semantics, and preferably public mainnet signature pairs for regression fixtures. The exact remaining ask is tracked in [Jupiter position authority confirmation](jupiter-position-authority-confirmation.md).
