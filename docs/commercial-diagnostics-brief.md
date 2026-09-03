# Commercial Diagnostics Brief

This brief defines the first revenue path for Open Perps Reliability Stack before any production execution exists.

## Positioning

Blocksize can sell read-only reliability diagnostics, protocol proof-pack support, and integration review for Solana perps venues and builders.

This is not a trading, custody, liquidation-execution, or profit-guarantee product.

## Buyer Context

Likely buyers:

- perps protocols that need adapter, oracle, replay, and liquidation-health evidence
- market makers that need independent venue-risk visibility
- integrators that need source-backed protocol reliability checks
- grant reviewers or ecosystem programs that want transparent public-good infrastructure
- infrastructure teams that want scrubbed post-incident or readiness reports

Likely buyer pressure:

- fragmented venue mechanics
- inconsistent public schemas and decoders
- unclear oracle and liquidation-risk boundaries
- difficult reviewer handoff for grants, audits, and integrations
- need for repeatable evidence without exposing private trading strategy

## Offer Shape

### Open Source Proof-Pack Support

Customer outcome:

- A protocol or builder gets a public, reviewer-safe proof pack with schemas, fixtures, reason codes, and claim boundaries.

Deliverables:

- protocol adapter scope memo
- source authority review
- scrubbed fixture package
- public data-quality report
- dashboard-ready metrics summary
- grant or ecosystem reviewer handoff

Boundary:

- No private route logic, wallets, keys, live transaction submission, or capital deployment.

### Read-Only Diagnostics API

Customer outcome:

- A customer can monitor venue reliability indicators from source-backed public data.

Deliverables:

- authenticated read-only API
- private dashboard
- adapter health, oracle risk, stale-input, schema-drift, and replay-readiness indicators
- daily or weekly reliability summaries

Boundary:

- Diagnostics only. No trading signals, order routing, custody, execution, or profit claims.

### Protocol Integration Review

Customer outcome:

- A customer can decide whether a venue is ready for integration, market making, or deeper due diligence.

Deliverables:

- source-pinned protocol map
- account and instruction surface review
- decoder confidence matrix
- dry-run/replay readiness assessment
- open blockers and next evidence plan

Boundary:

- Evidence and implementation support only. Execution design requires a separate approval track.

## Value Hypotheses

| Use Case | Value Bucket | Causal Chain | Evidence Posture | Confidence |
| --- | --- | --- | --- | --- |
| Proof-pack support | Time to Market | source review and fixtures -> faster reviewer handoff -> fewer integration/grant delays | Inferred from current MVP artifact and grant workflow | Medium |
| Read-only diagnostics | Risk Reduction | continuous public-data checks -> earlier schema/oracle/freshness detection -> fewer blind operational decisions | Structural until 7-day soak exists | Low |
| Integration review | Cost Reduction | decoder and claim-boundary review -> fewer false assumptions -> less wasted engineering diligence | Inferred from current Drift/Jupiter/Phoenix blockers | Medium |

## Pricing Structure To Validate

Use structural pricing until customer discovery provides budget evidence.

Possible packages:

- Fixed-fee proof-pack sprint.
- Monthly read-only diagnostics subscription.
- Protocol integration review retainer.
- Grant-support package tied to public OSS deliverables.

Do not publish exact pricing until buyer willingness-to-pay is validated.

See [Commercial diagnostics pricing](commercial-diagnostics-pricing.md) for current-source infrastructure cost anchors and the first package price test.

## Proof We Can Show Today

- Hosted static proof pack on Railway and GitHub Pages.
- Validated fixture replay and API examples.
- Drift read-only guardrail and scan-boundary evidence.
- Jupiter onchain-IDL layout decode and lifecycle role-map probe contract.
- Phoenix telemetry and validator planning package.
- Explicit service, public artifact, OSS/commercial, and live-readiness boundaries.

## Missing Before Revenue Launch

- Chosen first customer profile.
- Named buyer problem and buying trigger.
- One validated package with scope, timeline, exclusions, and acceptance criteria.
- Lightweight commercial terms excluding custody, trading advice, execution guarantees, and profit guarantees.
- Private delivery surface, if diagnostics are not fully public.
- Founder approval for auth, billing, and customer-facing pricing.

## Recommended First Commercial Motion

Recommended first package: Protocol proof-pack support.

Reason:

- It uses the artifacts already built.
- It is closest to the Solana Foundation grant story.
- It creates customer value without a live worker.
- It can produce public-good outputs while also funding custom implementation support.

The read-only diagnostics API should follow after the 7-day soak proves the worker creates useful, stable output.
