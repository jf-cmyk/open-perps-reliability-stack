# Source Review Records

Source review records make protocol-source decisions machine-readable before OPRS promotes any decode, pairing, or replay claim. They are local/offline evidence metadata, not live execution artifacts.

Current schema:

- `schemas/datasets/source-review-record-v0.json`

Current examples:

- `examples/datasets/jupiter_position_authority_source_review_example.json`
- `examples/datasets/drift_public_field_source_review_template.json`
- `examples/datasets/phoenix_hawkeye_source_review_example.json`

Current validator:

```bash
scripts/validate_source_review_records.py
```

## Review Statuses

- `blocked`: evidence is insufficient and the claim must remain blocked.
- `pending`: a review template exists, but the field or source has not been approved.
- `approved`: all approval gates are true and the claim remains inside the read-only/dry-run boundary.
- `rejected`: the evidence is invalid, unsafe, or contradicted by source review.

## Required Boundary

Every record must keep production and replay claims false:

- `verified_pairing_claimed`
- `replay_ready_claimed`
- `execution_claimed`
- `signing_claimed`
- `custody_or_capital_claimed`

`binary_decode_claimed` may be true only for a source-reviewed account-layout package, such as the Jupiter onchain Anchor IDL decode record. It is not a pairing, replay, keeper, or execution claim.

An `approved` source review record is still not a production permission. It only allows a future local read-only implementation step if the target validator and scrub review also pass.
