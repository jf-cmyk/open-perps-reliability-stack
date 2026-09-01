# Jupiter Position Authority Confirmation

This document is the exact source-authority ask for moving Jupiter Perps from source-authorized account-layout decode toward verified request/fulfillment pairing and replay. It does not authorize production execution.

## Narrow Ask

Can Jupiter confirm the canonical source of truth for mainnet Jupiter Perps program `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu`, specifically instruction account roles, request/fulfillment lifecycle semantics, and public fixture signatures?

## Current Public Evidence

Official Jupiter docs and the live onchain Anchor IDL currently provide useful evidence:

- `Position` account guide: `https://developers.jup.ag/docs/perps/position-account`
- `PositionRequest` account guide: `https://developers.jup.ag/docs/perps/position-request-account`
- Technical reference: `https://docs.jup.ag/user-docs/trade/perps-and-jlp/technical-reference`

What these docs support:

- Jupiter Perps uses `Position` accounts for trader position state.
- Jupiter Perps uses `PositionRequest` accounts for requests to open, close, increase, decrease, deposit, withdraw, and manage TP/SL or limit-style flows.
- `Position` accounts are described as stable PDAs derived from trader wallet, custody, collateral custody, and constant seeds.
- `PositionRequest` accounts are described as unique PDAs derived from the underlying `Position` account, constant seeds, and a random integer seed.
- Jupiter Perps uses a two-transaction request/fulfillment model: a request transaction creates/submits the trade request, and a keeper fulfillment transaction executes the trade.
- Official docs list field names and high-level types for `Position` and `PositionRequest`.
- Current public Jupiter CLI documentation describes read-only position/history/market commands and `--dry-run` previews for trading commands, which is useful for workflow research but does not provide binary account-layout authority.
- The live onchain Anchor IDL account `38GK1i4cQPAxqrbfKX4RRMNfXpKRn5PgLFHVJeXm1C8Y` has normalized hash `611de36592f4508438df16ebee2ff73b9789eda105ec712575d515b432d1ebaa` and supports source-authorized account-layout decode for the checked `Position` and `PositionRequest` records.

What these docs do not yet support:

- current live-program source commit
- instruction account-role maps
- verified request/fulfillment pairing
- liquidation replay
- whether any Jupiter API-key-gated endpoint is canonical for schema, IDL, source-revision, or fixture metadata

## Why The Current Evidence Is Not Enough For Pairing

The onchain IDL is enough for bounded account-layout decode, but it is not enough by itself to claim a verified request/fulfillment pair. Pairing needs source or fixture evidence for which instruction accounts identify the request, which account survives or closes, how fulfilled state links to final position state, and how keeper behavior should be interpreted.

The docs-linked example repository remains useful for research and field planning, but its current normalized IDL does not match the live onchain IDL hash. It should not be used as authority for public decode claims.

## Minimum Confirmation Ask

Ask Jupiter for all of the following:

1. Confirmation that `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu` is the current live Jupiter Perps program ID to use for this lifecycle proof.
2. Confirmation that onchain IDL account `38GK1i4cQPAxqrbfKX4RRMNfXpKRn5PgLFHVJeXm1C8Y` is acceptable account-layout authority, or a canonical replacement if it is not.
3. Instruction account-role maps for create/open/increase/decrease/close/cancel/reject/execute/fulfill flows.
4. Whether request and fulfillment transactions can be verified by a shared decoded `PositionRequest` account.
5. Whether a final `Position` account should be linked to the same lifecycle by PDA derivation, instruction accounts, event fields, or another source-defined key.
6. The role of `PositionRequestATA` or equivalent token accounts in deposit/withdraw flows.
7. Non-TP/SL request closure/execution semantics, including how `executed` should be interpreted.
8. TP/SL persistence, trigger, and closure semantics if they differ from ordinary requests.
9. One or more public mainnet signature pairs with expected account keys and decoded before/after state that can be used as regression-test fixtures.
10. Whether any keeper-only, internal, temporary, or deprecated accounts must be excluded from public interpretation.
11. Whether any authenticated Jupiter API endpoint provides canonical account-role, lifecycle, or fixture metadata, and if so, what response hash/checksum/version should be pinned.

## Jupiter API Key Boundary

`JUPITER_API_KEY` may be useful for authenticated read-only discovery if Jupiter exposes a relevant endpoint, but it is not source authority by itself. OPRS can use it only for local probes that do not create, build, submit, sign, route, or execute transactions.

The API key can unlock lifecycle work only if the response returns or references a Jupiter-confirmed hashable artifact tied to the live program, such as an instruction account-role map or public fixture set. Until then, API-key access remains a discovery aid and all Jupiter verified pairing, keeper execution, and replay claims stay blocked.

## Decode Unlock

Binary account-layout decode for `Position` and `PositionRequest` has moved forward through the reviewed onchain Anchor IDL extraction. Future expansion of decoded fields should still pass source review and scrub checks.

This does not by itself unlock verified request/fulfillment pairing or replay readiness.

## Pairing Unlock

Verified request/fulfillment pairing needs a separate source-backed lifecycle/account-role map showing:

- request transaction creates or references a specific `PositionRequest`
- fulfillment transaction references the same `PositionRequest`
- fulfillment transaction links to the corresponding `Position`
- source-backed state transition semantics for request creation, execution, rejection, cancellation, closure, or persistence
- TP/SL request behavior when it differs from ordinary request flows
- `PositionRequestATA` or equivalent token-account role in deposits and withdrawals
- one or more public mainnet signature pairs with expected account keys and decoded before/after state

Without public signature examples, pairing may still be source-derived later, but it will be harder to regression-test and should remain local-only until a deterministic fixture can be validated.

## Unlock Criteria

Verified lifecycle pairing can only move forward when one of these source-authority paths lands:

- Jupiter provides written confirmation for the exact `Position` and `PositionRequest` layouts plus instruction account-role maps.
- Jupiter provides written confirmation for instruction account-role maps and lifecycle semantics.
- Jupiter provides public mainnet fixture signatures with expected decoded before/after state.
- A Jupiter-confirmed API endpoint returns canonical role-map, lifecycle, or fixture metadata with a stable version, checksum, or other hashable artifact tied to the live program.

After source authority lands, OPRS still needs a local-only implementation phase:

1. Link request and fulfillment signatures through source-reviewed account roles.
2. Decode only source-reviewed `Position` / `PositionRequest` lifecycle fields.
3. Keep outputs under `target/` until scrub review passes.
4. Add a local validator before public examples or grant claims.
5. Keep transaction submission, order building, keeper behavior, signing, custody, priority-fee bidding, and capital deployment blocked.

## Still Blocked

Until the unlock criteria are met, OPRS must not claim:

- Verified request/fulfillment pairing.
- Keeper execution verification.
- Historical Jupiter liquidation replay.
- Jupiter adapter readiness beyond read-only target discovery, account-layout decode, and unverified lifecycle candidates.

Allowed interim language:

- `target_discovered`
- `candidate_pair_unverified`
- `onchain_anchor_idl_hashable`
- `resolved_for_layout_decode`
- `verified_request_fulfillment_pair_claimed=false`
- `position_request_decoded=true`
- `position_decoded=true`
- `replay_ready=false`

## Contact Template

For a shorter founder-ready note, use [Jupiter position authority outbound note](jupiter-position-authority-outbound.md). For the exact operator steps Johann needs to take, use [Jupiter source authority resolution](jupiter-source-authority-resolution.md).

```text
Hi Jupiter team,

We are building Open Perps Reliability Stack, an open-source, read-only and dry-run developer tooling project for Solana perps reliability. We are not building execution, signing, custody, order submission, keeper automation, or trading infrastructure in the grant MVP.

For Jupiter Perps, we use official docs and the live onchain Anchor IDL for target discovery and scrubbed account-layout decode. We do not claim verified request/fulfillment pairing or replay readiness.

Could you confirm the canonical lifecycle authority for the current Jupiter Perps program?

Specifically, we need:

1. Confirmation that `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu` is the current live Jupiter Perps program ID for this proof.
2. Confirmation that onchain IDL account `38GK1i4cQPAxqrbfKX4RRMNfXpKRn5PgLFHVJeXm1C8Y` is acceptable account-layout authority, or the preferred replacement if not.
3. Instruction account-role maps for create/open/increase/decrease/close/cancel/reject/execute/fulfill flows.
4. Confirmation of whether a request tx and fulfillment tx can be verified by a shared decoded PositionRequest account.
5. Confirmation of how the final Position account should be linked to the request lifecycle, if applicable.
6. PositionRequestATA or equivalent token-account roles in deposit/withdraw flows.
7. Non-TP/SL execution/closure semantics, including how executed should be interpreted.
8. TP/SL persistence, trigger, and closure semantics if different from ordinary requests.
9. One or more public mainnet signature pairs with expected account keys and decoded before/after state for regression fixtures.
10. Any keeper-only/internal/deprecated accounts that should not be interpreted publicly.
11. Whether any API-key-gated read-only endpoint is canonical for role-map/lifecycle/fixture metadata, and how its response should be hash-pinned or versioned.

We will keep all live reads read-only, keep raw payloads out of public artifacts, and mark any unconfirmed lifecycle evidence as candidate-only.
```
