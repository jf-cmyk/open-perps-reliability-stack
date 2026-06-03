# Drift Synthetic Margin Fixture 001

This is a deterministic, synthetic, read-only fixture for proposal and schema validation. It is not a decoded historical Drift liquidation and must not be presented as live trading evidence.

The fixture demonstrates:

- Adapter-normalized event lineage.
- Pyth-style oracle snapshot shape.
- Position/margin snapshot shape.
- Dry-run output with `requires_signer=false` and `submission_disabled=true`.
- Data quality publish gate warnings for synthetic source disclosure.

No private keys, signing, transaction submission, custody, capital deployment, RPC URLs, API keys, private route labels, or local absolute paths are included.
