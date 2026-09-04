# Read-Only Worker Candidate Package Template

This directory is a public promotion template, not a promoted worker output.

Use it only after a generated read-only worker public candidate has passed validation and founder review. The final package must replace every template placeholder, bind deterministic checksums, preserve read-only and dry-run scope, and add a reviewed entry to `examples/public/contract-index.json`.

## Required Inputs

- A validated `oprs.readonly_worker_public_candidate.v0` candidate.
- A recorded founder review decision for the selected candidate id.
- A manifest generated from the selected candidate, not from private worker payload bodies.
- A DQ report where every `block_publish` check passes.
- A public-package validator for the final package profile.

## Still Blocked Here

- Public output promotion.
- Replay-readiness claims.
- Verified liquidation-opportunity claims.
- Signing, submission, or capital-moving scope.
- Private worker payload body publication.
- Secret, RPC URL, webhook, wallet, or local machine path publication.

