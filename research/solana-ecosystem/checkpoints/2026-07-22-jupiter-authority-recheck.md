# Jupiter Perps Authority Recheck

Observed: 2026-07-22

Sources:

- https://github.com/jup-ag/docs/tree/d1c158738438f4c066882da23f74d25083da9798/perps
- https://github.com/jup-ag/docs/blob/572dcd7df5f81519f7ed589734d67a587d8bde7a/perps/position-request-account.mdx

## Partial Unlock

Jupiter's first-party documentation now supports these descriptive semantics:

- `PositionRequest` is derived from the underlying `Position`, constant seeds, and a random integer seed.
- A request-associated token account holds deposits or withdrawals until transfer to custody or return to the trader.
- Ordinary requests close after execution or rejection.
- TP/SL requests persist until triggered and executed.
- `PositionRequest` and `Position` share owner, pool, custody, collateral-custody, side, and state concepts that can inform unverified candidate labels.

## Still Blocked

The Perps overview calls the API work-in-progress and recommends a third-party repository for IDL parsing. The reviewed first-party docs do not provide a canonical current source/IDL with:

- account discriminators, byte sizes, offsets, and enum encodings;
- exact constant PDA seeds and derivation order;
- a revision-to-mainnet-deployment mapping;
- public request, execution/rejection, and resulting-position signature pairs suitable for regression fixtures.

Therefore OPRS must continue emitting:

- `position_request_decoded=false`;
- `verified_request_fulfillment_pair_claimed=false`;
- no Jupiter historical replay-readiness claim.

## Decision

`Q-006` is resolved as a partial semantic unlock, not a decode or pairing unlock. Further public-source searching has diminishing value until Jupiter publishes a canonical current IDL/source or directly confirms the exact source-authority package already documented by OPRS.

## Grant Safety

Grant materials may cite first-party account lifecycle semantics and OPRS's source-governance discipline. They must not imply canonical decoding, verified pair reconstruction, or Jupiter endorsement.
