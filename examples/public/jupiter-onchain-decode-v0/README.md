# Jupiter Onchain Decode v0

This public package records the first source-authorized Jupiter Perps account decode proof for OPRS.

The package is based on the live program's onchain Anchor IDL account and scrubbed read-only account reads. It does not include account bytes, private RPC configuration, API keys, wallet secrets, signing material, transaction bodies, execution paths, or replay-ready claims.

This package promotes Jupiter from source-authority blocked to source-authorized local decode for `Position` and `PositionRequest` layouts only. Verified request/fulfillment pairing, liquidation replay, keeper semantics, signing, transaction submission, and production execution remain blocked.
