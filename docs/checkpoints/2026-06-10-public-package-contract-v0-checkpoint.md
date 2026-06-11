# Checkpoint: Public Package Contract v0

Date: 2026-06-10

## Status

The MVP remains read-only and dry-run only. No production execution, signing, custody, priority-fee bidding, or capital deployment is in scope.

Latest development slice:

- Expanded the non-served invalid public-package fixture corpus from 6 to 16 cases:
  - `tests/fixtures/public-packages/invalid/cases.json`
  - `scripts/validate_invalid_public_package_fixtures.py`
- Added replay-layer tx-plan guardrail negatives:
  - Reject `requires_signer=true`.
  - Reject `submission_disabled=false`.
  - Reject signer/custody/execution-policy markers in dry-run output.
  - Replay test coverage is now 19 tests.
- Added invalid cases for:
  - Drift replay-readiness overclaim.
  - Drift raw-payload leak.
  - Drift manifest checksum mismatch.
  - Drift manifest absolute local path leak.
  - Drift schema missing required field.
  - Jupiter verified-pairing overclaim.
  - Jupiter verified record status overclaim.
  - Jupiter RPC URL leak.
  - Jupiter bearer-token marker leak.
  - Jupiter unsafe absolute evidence reference.
  - Jupiter schema extra record property.
  - Contract-index payload schema-version mismatch.
  - Contract-index duplicate package ID.
  - Contract-index missing validator path.
  - Contract-index missing schema path.
  - Contract-index missing manifest path.
- Added bounded dependency-free JSON Schema validation for:
  - Public contract index.
  - Drift spot guardrail payload.
  - Drift perp guardrail payload.
  - Jupiter authority-gap payload.

## Architecture Decision

Keep the current validator boundary:

- `scripts/public_package_contract.py` owns shared mechanical checks:
  - bounded JSON Schema validation for checked-in dataset schemas
  - safe relative paths
  - blocked public-text patterns
  - contract-index lookup
  - schema-version agreement
  - checksums
  - row counts
  - manifest/DQ publish gates
- Specialized validators own package semantics:
  - Drift guardrails: no replay/user-state/market-economics overclaims, public guardrail readiness, guardrail record shape.
  - Jupiter authority gap: no canonical source claim, no binary decode claim, no verified pairing claim, no replay readiness claim.
  - Contract index: package discovery, validator/schema paths, duplicate IDs, and claim-boundary metadata.

Do not introduce a broad generic package abstraction yet. Revisit only when a third package family creates real shared-validation pressure.

## Current Public Claim Boundary

Allowed:

- Static public proof packages with read-only/dry-run claim boundaries.
- Drift selected public guardrail fields with source-backed labels and package validation.
- Jupiter source-authority and lifecycle blockers as public negative evidence.
- Invalid fixtures as non-served CI/local validation inputs.

Blocked:

- Jupiter binary account decode.
- Verified Jupiter request/fulfillment lifecycle pairing.
- Historical Jupiter liquidation replay.
- Public raw account bytes, raw transaction bodies, raw logs, local paths, RPC URLs, API keys, bearer tokens, private-key material, custody/capital fields, or execution-resource controls.
- Any signing, transaction submission, route execution, custody control, or capital deployment claim.

## Validation

Run:

```bash
scripts/validate_invalid_public_package_fixtures.py
scripts/validate_public_contract_index.py
scripts/validate_public_guardrail_package.py
scripts/validate_public_jupiter_authority_gap.py
scripts/run_mvp_checks.sh
git diff --check
```

## Agent Guidance Applied

- Architecture: keep shared shell plus specialized validators; avoid a generic validation framework for now.
- Data: expand invalid corpus once before grant submission, then stop around a focused corpus; current coverage is 16 cases including schema-shape negatives.
- Liquidator/SDK: current Jupiter source-authority reason-code coverage is sufficient; tx-plan guardrail negatives now cover signer/submission/execution-resource regressions.
- Protocol: Jupiter `PositionRequest` canonical authority remains the main blocker; Phoenix is the best next source-backed venue if Jupiter stalls.
- Grant Positioning: say "synthetic dry-run scenarios", "rejected Jupiter blocker fixtures", and "source-authority enforcement".

## Next Queue

1. Continue Jupiter `PositionRequest` canonical authority diligence or request direct Jupiter confirmation.
2. If Jupiter remains blocked, start a Phoenix source-backed adapter/proof-package spike.
3. Refresh the local Word proposal from the improved markdown and grant-safe wording.
4. Address GitHub Actions Node 20 deprecation before June 16, 2026.
5. Add a validator dispatcher only if a third public package family creates real duplication.
