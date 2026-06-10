# Checkpoint: Contract Index And Jupiter Gap

Date: 2026-06-09

## Status

The MVP remains read-only and dry-run only. No production execution, signing, custody, priority-fee bidding, or capital deployment is in scope.

Latest development slice:

- Added a public contract index:
  - `examples/public/contract-index.json`
  - `schemas/datasets/public-contract-index-v0.json`
  - `scripts/validate_public_contract_index.py`
- Kept package validators specialized while making package discovery and claim boundaries machine-readable.
- Added a Jupiter authority-gap package:
  - `schemas/datasets/jupiter-authority-gap-v0.json`
  - `examples/public/jupiter-authority-gap-v0/gap_report.json`
  - `examples/public/jupiter-authority-gap-v0/manifest.json`
  - `examples/public/jupiter-authority-gap-v0/dq.json`
  - `scripts/validate_public_jupiter_authority_gap.py`
- Added the ninth replay fixture:
  - `datasets/sample/jupiter_synthetic_lifecycle_candidate_unverified_001/`
  - Status: `Rejected`
  - Reason codes: `AdapterDecodeFailed`, `DataQualityLow`, `ExecutionDisabledDryRun`
- Added the tenth replay fixture:
  - `datasets/sample/jupiter_synthetic_lifecycle_weak_no_shared_jupiter_account_001/`
  - Status: `Rejected`
  - Reason codes: `AdapterDecodeFailed`, `DataQualityLow`, `ExecutionDisabledDryRun`
- Added the eleventh replay fixture:
  - `datasets/sample/jupiter_synthetic_malformed_source_authority_001/`
  - Status: `Rejected`
  - Reason codes: `AdapterDecodeFailed`, `AdapterVersionMismatch`, `DataQualityLow`, `ExecutionDisabledDryRun`
- Added an invalid public-package fixture corpus:
  - `tests/fixtures/public-packages/invalid/cases.json`
  - `scripts/validate_invalid_public_package_fixtures.py`
  - Cases cover Drift replay-ready overclaims, raw payload leaks, Jupiter verified-pairing overclaims, RPC URL leaks, and contract-index schema drift.
- Extracted a minimal shared validation helper:
  - `scripts/public_package_contract.py`
  - Shared checks cover paths, contract index lookup, blocked public-text patterns, checksums, row counts, and manifest/DQ publish gates.
- Added Rust replay validation for Jupiter evidence boundaries, including a negative test that rejects canonical decode or verified-pairing overclaims.
- Updated proof-pack index, dashboard, MVP checks, hosted smoke checks, README, protocol docs, Helius proof docs, and grant proposal language.

## Current Public Claim Boundary

Allowed:

- Drift selected public guardrail fields are source-backed and package-validated.
- Jupiter lifecycle candidates are public metadata evidence only.
- Malformed Jupiter source-authority evidence is rejected before binary decode or pairing claims.
- Jupiter source authority, binary decode, verified pairing, and replay readiness remain blocked.
- Both Drift and Jupiter artifacts are read-only, dry-run only, and public-scrubbed.

Blocked:

- Jupiter binary account decode.
- Verified Jupiter request/fulfillment lifecycle pairing.
- Historical Jupiter liquidation replay.
- Any signing, transaction submission, route execution, custody control, or capital deployment claim.

## Validation To Run

```bash
scripts/validate_public_contract_index.py
scripts/validate_public_guardrail_package.py
scripts/validate_public_jupiter_authority_gap.py
scripts/validate_invalid_public_package_fixtures.py
cargo run -p oprs-replay --example validate_fixtures
scripts/run_mvp_checks.sh
git diff --check
```

Then deploy and smoke-check:

```bash
git push
railway up --detach
scripts/run_hosted_smoke_checks.sh https://refreshing-art-production-86de.up.railway.app
scripts/run_hosted_smoke_checks.sh https://jf-cmyk.github.io/open-perps-reliability-stack
```

## Agent Guidance Applied

- Architecture: keep validators specialized for now; introduce a generic package abstraction only after multiple package families create real shared-validation pressure.
- Protocol: pause broad Drift expansion and make Jupiter source authority/request-fulfillment blockers explicit.
- Data: add a lightweight contract index and harden publish/scrub/claim-boundary gates.
- Liquidator/SDK: add Jupiter unverified lifecycle and malformed source-authority fixtures before more Drift fixtures; never mark them eligible.
- Grant Positioning: present guardrail proof as primary public-good evidence and Jupiter source authority as the next milestone.

## Next Queue

1. Run full validation, commit, push, deploy Railway, and smoke-check both hosted surfaces.
2. Research Jupiter `PositionRequest` source authority as the next protocol blocker.
3. Add a source-contact note or issue for Jupiter canonical IDL/source confirmation.
4. Keep Jupiter verified pairing blocked until canonical source authority proves request/position account roles and lifecycle keys.
5. Keep Drift expansion paused unless a very small source-backed field is explicitly needed for the grant story.
