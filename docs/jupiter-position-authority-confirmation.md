# Jupiter Position Authority Confirmation

This document is the exact source-authority ask for moving Jupiter Perps from target discovery and unverified lifecycle candidates toward any future binary decode or verified request/fulfillment pairing. It does not authorize new Jupiter decode claims by itself.

## Narrow Ask

Can Jupiter confirm the canonical source of truth for mainnet Jupiter Perps program `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu`, specifically the `PositionRequest` and `Position` account layouts and lifecycle semantics?

## Current Public Evidence

Official Jupiter docs currently provide useful field-planning evidence:

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

What these docs do not yet support:

- canonical binary layout
- Anchor discriminator confirmation
- exact field offsets
- enum variant integer values
- account size
- canonical IDL hash
- current live-program source commit
- instruction account-role maps
- verified request/fulfillment pairing
- liquidation replay

## Why The Current Evidence Is Not Enough

Docs-level field lists are not the same as source authority. For OPRS to decode public Jupiter account bytes or claim a verified request/fulfillment pair, the implementation needs a canonical source that ties field semantics to the current live Jupiter Perps program.

The docs-linked example repository remains useful for research and field planning, but its current status is still `docs_linked_example_not_canonical`. It should not be used as authority for public binary decode claims unless Jupiter explicitly confirms it or publishes a canonical replacement.

## Minimum Confirmation Ask

Ask Jupiter for all of the following:

1. Confirmation that `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu` is the current live Jupiter Perps program ID to use for this proof.
2. Canonical IDL or source repository URL.
3. Commit, release, package version, or onchain IDL address that ties the IDL/source to the live program.
4. Hashable artifact for the IDL or source revision.
5. `Position` account discriminator, account size, field order, field types, enum layouts, and PDA seeds.
6. `PositionRequest` account discriminator, account size, field order, field types, enum layouts, PDA seeds, bump encoding, and counter/random-seed encoding.
7. Instruction account-role maps for create/open/increase/decrease/close/cancel/reject/execute/fulfill flows.
8. Whether request and fulfillment transactions can be verified by a shared decoded `PositionRequest` account.
9. Whether a final `Position` account should be linked to the same lifecycle by PDA derivation, instruction accounts, event fields, or another source-defined key.
10. The role of `PositionRequestATA` or equivalent token accounts in deposit/withdraw flows.
11. Non-TP/SL request closure/execution semantics, including how `executed` should be interpreted.
12. TP/SL persistence, trigger, and closure semantics if they differ from ordinary requests.
13. One or more public mainnet signature pairs with expected account keys and decoded before/after state that can be used as regression-test fixtures.
14. Whether any keeper-only, internal, temporary, or deprecated accounts must be excluded from public interpretation.

## Decode Unlock

Binary decode for `Position` and `PositionRequest` can move forward only after Jupiter-controlled or source-reviewed evidence confirms:

- canonical IDL/source revision: repo or org, commit SHA, file path, IDL hash, package release, onchain IDL address, or explorer program-IDL hash
- live-program linkage to `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu`
- `Position` and `PositionRequest` discriminators
- total account sizes
- field order and byte offsets
- enum integer encodings
- PDA seeds and bump/counter/random-seed encoding

This unlocks a future local decode experiment only. It does not by itself unlock verified request/fulfillment pairing or replay readiness.

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

Jupiter binary decode or verified lifecycle pairing can only move forward when one of these source-authority paths lands:

- Jupiter publishes a canonical Perps IDL/source revision for the live program.
- Jupiter explicitly confirms the docs-linked IDL candidate is canonical for the current live program.
- A reviewed onchain/program-IDL extraction path produces a hashable IDL that matches current program semantics.
- Jupiter provides written confirmation for the exact `Position` and `PositionRequest` layouts plus instruction account-role maps.

After source authority lands, OPRS still needs a local-only implementation phase:

1. Decode account discriminator and data length first.
2. Decode only source-reviewed `Position` / `PositionRequest` identity and lifecycle fields.
3. Keep outputs under `target/` until scrub review passes.
4. Add a local validator before public examples or grant claims.
5. Keep transaction submission, order building, keeper behavior, signing, custody, priority-fee bidding, and capital deployment blocked.

## Still Blocked

Until the unlock criteria are met, OPRS must not claim:

- Jupiter binary account decoding.
- Decoded `Position` account support.
- Decoded `PositionRequest` account support.
- Verified request/fulfillment pairing.
- Keeper execution verification.
- Historical Jupiter liquidation replay.
- Jupiter adapter readiness beyond read-only target discovery and unverified lifecycle candidates.

Allowed interim language:

- `target_discovered`
- `candidate_pair_unverified`
- `docs_linked_example_not_canonical`
- `source_authority_blocked`
- `verified_request_fulfillment_pair_claimed=false`
- `position_request_decoded=false`
- `position_decoded=false`
- `replay_ready=false`

## Contact Template

```text
Hi Jupiter team,

We are building Open Perps Reliability Stack, an open-source, read-only and dry-run developer tooling project for Solana perps reliability. We are not building execution, signing, custody, order submission, keeper automation, or trading infrastructure in the grant MVP.

For Jupiter Perps, we currently use official docs only for target discovery and unverified lifecycle research. We do not claim binary decode or verified request/fulfillment pairing because we have not found canonical source authority for the live program `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu`.

Could you confirm the canonical source/IDL authority for the current Jupiter Perps program?

Specifically, we need:

1. Confirmation that `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu` is the current live Jupiter Perps program ID for this proof.
2. Canonical IDL/source repo, package, release, or onchain IDL address.
3. Commit/release/hash tying that IDL/source to the live program.
4. Position account discriminator, account size, field order/types/offsets, enum layouts, and PDA seeds.
5. PositionRequest account discriminator, account size, field order/types/offsets, enum layouts, PDA seeds, bump encoding, and counter/random-seed encoding.
6. Instruction account-role maps for create/open/increase/decrease/close/cancel/reject/execute/fulfill flows.
7. Confirmation of whether a request tx and fulfillment tx can be verified by a shared decoded PositionRequest account.
8. Confirmation of how the final Position account should be linked to the request lifecycle, if applicable.
9. PositionRequestATA or equivalent token-account roles in deposit/withdraw flows.
10. Non-TP/SL execution/closure semantics, including how executed should be interpreted.
11. TP/SL persistence, trigger, and closure semantics if different from ordinary requests.
12. One or more public mainnet signature pairs with expected account keys and decoded before/after state for regression fixtures.
13. Any keeper-only/internal/deprecated accounts that should not be interpreted publicly.

We will keep all live reads read-only, keep raw payloads out of public artifacts, and mark any unconfirmed evidence as source-authority blocked.
```
