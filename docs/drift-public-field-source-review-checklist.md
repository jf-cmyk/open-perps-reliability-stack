# Drift Public Field Source Review Checklist

This checklist is required before adding any new entry to `PUBLIC_FIELD_LAYOUTS` in `scripts/discover_drift_readonly_state.py`. It keeps Drift public-field expansion source-backed, scrubbed, and bounded to read-only developer tooling.

## Scope

Applies to:

- `State`
- `PerpMarket`
- `SpotMarket`
- selected identity, metadata, oracle identity, and guardrail fields
- source-reviewed additions to local public-field target output under `target/`

Explicitly excludes:

- user, wallet, trader, or position-state decode
- market-economics claims such as solvency, PnL, profit, health, or liquidatability
- historical liquidation replay or replay-readiness claims
- raw account bytes, raw transaction bodies, instruction data, or logs in committed artifacts
- signing, custody, transaction submission, order building, priority-fee bidding, or capital management

## Field Review Table

Record one row per proposed field before implementation.

| Account type | Field path | Output name | Source file URL at pinned commit | IDL/source anchor | Offset derivation notes | Type / length / endian | Expected-value source | Semantic-label source | Public-safety class | Reviewer / date / status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PerpMarket` | `PerpMarket.example` | `example` | `https://github.com/drift-labs/protocol-v2/blob/<commit>/...` | IDL/Rust/SDK anchor | Anchor discriminator plus reviewed layout notes | `u16`, little-endian | SDK constants, if any | enum/bitset source, if any | identity / metadata / guardrail | name, date, pending |

Allowed public-safety classes:

- `identity`
- `metadata`
- `oracle_identity`
- `guardrail`

Do not use this checklist to approve user state, market economics, execution claims, or replay readiness.

## Required Gates

Every proposed field must satisfy all gates:

- Pinned Drift commit and IDL SHA match [Drift decoder provenance](drift-decoder-provenance.md).
- Offset derivation is documented from pinned Rust, IDL, or SDK source, not inferred only from live account bytes.
- Field type, length, byte order, and Anchor discriminator offset are stated.
- Field is public identity, public metadata, public oracle identity, or public guardrail data only.
- Any expected value has a public source, such as target PDA derivation, market constants, oracle constants, mint constants, or pool constants.
- Any semantic label has a pinned enum or bitset source.
- Local public-field run passes `scripts/validate_drift_readonly_state.py`.
- Output stays under `target/` until scrub review passes.
- Output keeps `user_state_decoded=false`, `market_economics_decoded=false`, and `replay_ready=false`.
- Reviewer confirms no new public claim language is needed, or updates docs with the same boundaries.

## Validation Commands

Run these after implementing a reviewed field:

```bash
scripts/discover_drift_readonly_state.py --include-public-fields --out target/oprs-drift-readonly-state/latest-public-fields.json
scripts/validate_drift_readonly_state.py target/oprs-drift-readonly-state/latest-public-fields.json
scripts/run_mvp_checks.sh
cargo fmt --check
git diff --check
```

Do not promote a field into docs, public examples, or grant language if the local validator fails, if source authority is ambiguous, or if the evidence requires a raw-byte exception.

## Future Machine-Readable Gate

The current validator checks source provenance, output shape, scrub boundaries, and claim flags. Source-review metadata is now scaffolded in [Source review records](source-review-records.md). A future `scripts/validate_drift_readonly_state.py` revision may require a `source_review_id` for each decoded field once concrete review records replace the pending template.
