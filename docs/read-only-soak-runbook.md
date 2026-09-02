# Read-Only Soak Runbook

This runbook defines the 7-day operational soak required before a read-only worker can be treated as a live service.

## Scope

The soak covers read-only diagnostics only.

Allowed:

- Fetch public Solana data through a read-only RPC provider.
- Decode reviewed public protocol surfaces.
- Validate schemas, scrub policies, and claim boundaries.
- Record private run outputs and scrubbed summaries.
- Alert on failures, stale data, schema drift, and secret-marker findings.

Forbidden:

- signing
- transaction construction
- transaction submission
- retry logic
- priority-fee bidding
- block-engine submission
- wallet loading
- custody
- capital deployment
- liquidation execution

## Entry Criteria

Start the soak only after:

- A separate read-only worker service exists or the local cron substitute is documented.
- Worker variables are scoped to read-only infrastructure.
- The static proof-pack service remains secret-free.
- The first worker command is bounded by low limits.
- Probe-specific validators pass locally.
- `scripts/run_mvp_checks.sh` passes.
- Hosted smoke checks pass against Railway and GitHub Pages.

## Daily Checklist

Run this checklist once per day for 7 consecutive days.

1. Confirm the worker completed or failed closed.
2. Confirm logs contain no secret values or private endpoints.
3. Confirm logs contain no signer, wallet, custody, capital, or transaction-submission markers.
4. Validate generated JSON against the relevant schema.
5. Run the probe-specific validator.
6. Confirm source, slot, provider, freshness, checksum, and scrub metadata are present.
7. Record provider errors, skipped targets, stale inputs, and schema drift.
8. Record claim-boundary changes in the daily note.
9. Do not publish generated output unless a separate public promotion review passes.

## Day-By-Day Goals

Day 1:

- Run the smallest bounded job.
- Confirm no secret leakage in logs or output.
- Confirm failure paths are understandable.

Day 2:

- Repeat the same job with the same limits.
- Compare output shape, source metadata, and validation status.

Day 3:

- Increase only one bound if Days 1-2 were clean.
- Keep public output disabled.

Day 4:

- Add one additional protocol probe only if the first probe remains stable.
- Confirm each protocol has independent claim boundaries.

Day 5:

- Review data-quality downgrades and provider errors.
- Decide whether the worker is producing useful diagnostics or only noise.

Day 6:

- Re-run hosted smoke checks for the static proof pack.
- Confirm the worker service has not changed the public static service boundary.

Day 7:

- Produce a soak summary with pass/fail status, incidents, open risks, and the next recommendation.

## Required Soak Summary

At the end of the soak, create a summary with:

- date range
- worker service name
- command and limits
- protocols covered
- run count
- success count
- failure count
- stale-input count
- schema-drift count
- secret-marker findings
- output-promotion decisions
- remaining blockers
- recommendation: continue local, extend soak, launch read-only service, or stop

Machine-readable contract:

- Schema: `schemas/datasets/readonly-soak-summary-v0.json`
- Example: `examples/datasets/readonly_soak_summary_example.json`
- Validator: `scripts/validate_readonly_soak_summary.py`

## Pass Criteria

The soak passes only if:

- 7 consecutive daily checks are recorded.
- No secret leakage is found.
- No signer, wallet, custody, capital, or transaction-submission surface appears.
- Failures are bounded, visible, and fail closed.
- Output schemas and validators pass.
- Freshness and provider limitations are recorded.
- The static proof-pack service remains public, inert, and secret-free.

## Fail Criteria

The soak fails if:

- Any secret appears in logs, outputs, public pages, or examples.
- Any transaction-building or transaction-submission marker appears.
- Any worker output is published without validation.
- Provider failures are hidden or mislabeled as healthy runs.
- A protocol claim is upgraded without source-backed evidence.
- The static proof-pack service receives worker secrets.

## Incident Response

If a leak or scope violation occurs:

1. Stop scheduled worker runs.
2. Rotate affected credentials.
3. Remove affected outputs from public and private destinations.
4. Record the incident in the soak summary.
5. Add or tighten validator checks.
6. Restart the soak from Day 1 only after the fix is validated.

## Exit Decision

After Day 7:

- If the soak passes, the worker can be considered for a live read-only diagnostics launch.
- If the soak is useful but noisy, extend the soak with lower limits or narrower protocol scope.
- If the soak fails on scope or leakage, block hosted read-only service launch until remediated.
- If the soak proves no useful diagnostics, return to local probes and source review.
