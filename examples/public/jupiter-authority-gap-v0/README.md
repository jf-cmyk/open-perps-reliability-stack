# Jupiter Authority Gap v0

This public package records why Jupiter Perps request/fulfillment pairing is still unverified.

Canonical onchain Anchor IDL source authority is now resolved for account-layout decode and is packaged separately in `examples/public/jupiter-onchain-decode-v0/`.

This is now a remaining-gap report for lifecycle pairing and replay. It is not a transaction reconstruction artifact. It contains no account bytes, transaction bodies, logs, private route data, signing material, capital controls, or replay-ready claims.

The exact source-authority confirmation needed for `Position` and `PositionRequest` decode is tracked in `docs/jupiter-position-authority-confirmation.md`.
