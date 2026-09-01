# 2026-09-01 Jupiter Onchain Decode Checkpoint

## Status

Jupiter Perps canonical account-layout decode is resolved for the current MVP boundary.

OPRS derived the live Anchor IDL address for program `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu`, fetched the program-owned IDL account, inflated and normalized the IDL, and pinned normalized SHA-256 `611de36592f4508438df16ebee2ff73b9789eda105ec712575d515b432d1ebaa`.

The docs-linked third-party IDL candidate remains useful background, but it does not match the live onchain IDL hash.

## Public Artifacts

- `schemas/datasets/jupiter-onchain-decode-v0.json`
- `examples/public/jupiter-onchain-decode-v0/`
- `scripts/fetch_jupiter_onchain_idl.py`
- `scripts/decode_jupiter_position_examples.py`
- `scripts/validate_public_jupiter_onchain_decode.py`

## Claim Boundary

Allowed:

- Jupiter program/custody/oracle metadata discovery.
- Jupiter public transaction-history sampling.
- Unverified lifecycle candidate labeling.
- Source-authorized account-layout decode for checked `Position` and `PositionRequest` examples.

Blocked:

- Verified request/fulfillment pairing.
- Keeper behavior.
- Historical liquidation replay.
- Signing, transaction submission, order building, custody, capital deployment, and production execution.

## Next Queue

1. Keep the onchain decode package in the public contract index and hosted smoke checks.
2. Build a local-only Jupiter lifecycle role-map probe from public transactions and the onchain IDL.
3. Keep active account identifiers scrubbed or hashed in public packages.
4. Ask Jupiter only for lifecycle role maps, fixture signatures, or API-key-gated read-only fixture metadata; no external ask is needed for account-layout decode.
5. Continue Drift legacy liquidation-history pagination from cursor `297aqf8WJXieG1rMtb7LcpDak8i6f5WWcGogvSYsrQcnHA5RFjV2c4JyadMjPfi8BQWaDaPVZTdgeW2PBWQSE14h`.
