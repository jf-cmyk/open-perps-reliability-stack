# Jupiter Source Authority Audit

This note records the current Jupiter Perps source-authority boundary for OPRS. It supports field planning and target/lifecycle research, but it does not authorize Jupiter binary account decode claims.

## Audited Sources

| Source | Status | Use |
| --- | --- | --- |
| Jupiter technical reference | Official docs | Request/fulfillment model, oracle model, custody addresses, and external IDL example reference. |
| Jupiter Position account guide | Official docs | Public Position field planning and derivation context. |
| Jupiter PositionRequest account guide | Official docs | Public PositionRequest field planning, request lifecycle, and closure/execution context. |
| `julianfssen/jupiter-perps-anchor-idl-parsing` | Docs-linked example repo | Candidate Anchor IDL and TypeScript examples only. |
| Jupiter position authority confirmation ask | OPRS confirmation checklist | Exact evidence needed before `Position` / `PositionRequest` decode or verified pairing. |
| Jupiter API key | Optional authenticated discovery input | Not source authority unless it returns or references a Jupiter-confirmed hashable schema, IDL, source, or fixture artifact tied to the live program. |

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

Status: `docs_linked_example_not_canonical`.

Allowed:

- Use official docs for target discovery and lifecycle model language.
- Use the docs-linked IDL candidate for field planning.
- Keep shared-account lifecycle candidates as `candidate_pair_unverified`.
- Use `JUPITER_API_KEY` only for local read-only discovery if a Jupiter API endpoint is confirmed to be relevant.

Blocked:

- Jupiter binary account decode claims.
- Verified request/fulfillment pair claims.
- PositionRequest or Position decode claims.
- Liquidation replay claims.
- Treating API-key access alone as source authority.

## Reproducible Audit Command

```bash
scripts/audit_jupiter_source_authority.py --out target/oprs-jupiter-source-authority/latest.json
```

The command uses public HTTPS only. It does not load `HELIUS_RPC_URL`, wallet state, signers, keypairs, custody, or private API routes.

## API-Key Boundary

If a Jupiter API key is available, store it only in `.env` as `JUPITER_API_KEY` and keep it out of public artifacts, Railway static hosting variables, screenshots, logs, and chat. It may support authenticated read-only discovery, but OPRS should promote it to source authority only if the response itself is a hashable Jupiter-confirmed artifact or points to one with stable versioning.

## Unlock Criteria

One of these must happen before OPRS can claim Jupiter binary decoding:

1. Jupiter publishes or confirms a canonical Perps IDL/source revision.
2. The docs-linked IDL is explicitly confirmed as canonical for the current onchain program.
3. An independent onchain/program-IDL extraction path is reviewed, hashed, and matched to current program semantics.

For `Position` / `PositionRequest` specifically, OPRS also needs discriminator, account size, field order, offsets, field types, enum layouts, PDA seeds, bump/counter encoding, and instruction account-role maps for mainnet program `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu`. Verified pairing additionally needs source-backed lifecycle semantics and preferably public mainnet signature pairs for regression fixtures. The exact ask is tracked in [Jupiter position authority confirmation](jupiter-position-authority-confirmation.md).
