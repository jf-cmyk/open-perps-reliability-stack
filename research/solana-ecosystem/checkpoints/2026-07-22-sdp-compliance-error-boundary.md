# SDP Compliance Provider Error Boundary

Observed: 2026-07-22

## Verified Fact

Solana Developer Platform's official treasury-fund tutorial says address screening runs Range, Elliptic, TRM, and Chainalysis in parallel. It instructs integrators to treat any provider returning `status: "error"` as a defense-in-depth gap, not a clean pass. The tutorial records that Chainalysis credentials were broken in the production sandbox and returned that status as of May 22, 2026. SDP's compliance guide exposes provider-level `provider`, `status`, `riskScore`, `riskLevel`, `message`, and `evaluatedAt` fields.

Sources:

- https://platform.solana.com/docs/tutorials/tokenize-a-treasury-fund
- https://platform.solana.com/docs/guides/freeze-and-compliance

## Blocksize Implication

Blocksize can specify a read-only institutional proof pack that records provider completeness, freshness, latency, disagreement, missing results, and fail-closed handling alongside SDP prepare/execute diagnostics. The product should report evidence state and operational gaps without deciding whether an address or transaction is compliant.

## Evidence Boundary

The May 22 note is dated sandbox evidence. It does not establish that Chainalysis or SDP is currently unavailable or that production screening failed. Successful responses from other providers do not establish compliance, and Blocksize should not certify AML/KYC, sanctions status, provider quality, or transaction eligibility.

## Next Action

Map the documented screening response into a non-authoritative proof-pack schema and verify current sandbox behavior using only separately approved test access. Preserve provider errors, stale timestamps, absent responses, and disagreement as explicit evidence states.
