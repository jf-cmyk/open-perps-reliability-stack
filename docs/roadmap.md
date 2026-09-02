# Roadmap

The Open Perps Reliability Stack is staged as public-good reliability infrastructure first, with commercial services separated behind later approvals.

## Scope Rule

Initial scope is read-only and dry-run only:

- No production trading.
- No custody.
- No private-key handling.
- No live transaction submission.
- No capital deployment.

## Milestones

### M0: Scope Lock

Goal: agree on first targets, deliverables, boundaries, and grant posture.

Acceptance criteria:

- First protocol target list approved.
- OSS and commercial boundary confirmed.
- Read-only and dry-run rule documented in ADR-0001.
- Initial GitHub issues and agent work packages opened.

### M1: Architecture and Protocol Diligence

Goal: establish the technical shape of the stack and prove the first adapter target is feasible.

Acceptance criteria:

- Architecture v0 covers modules, boundaries, data flow, and integration contracts.
- Protocol target ranking covers feasibility, permissions, docs/IDL availability, read-only surfaces, and risks.
- First adapter recommendation has explicit acceptance criteria.

### M2: Adapter and Data Model Proof

Goal: define the normalized read-only data layer and first adapter contract.

Acceptance criteria:

- Adapter standard v0 includes required metadata, surfaces, errors, freshness, and confidence fields.
- Data model v0 covers market, position, oracle, funding, fill, liquidation candidate, dry-run result, and reliability event entities.
- Public sample dataset format is defined with scrubbing rules.

### M3: Risk SDK and Dry-Run Alpha

Goal: produce a non-signing SDK/dry-run design that can identify and explain candidate liquidations.

Acceptance criteria:

- SDK interface supports read-only protocol state, candidate detection, risk scoring, and reason codes.
- Dry-run/replay design specifies fixtures, deterministic outputs, and simulation gates.
- Out-of-scope production execution controls are explicit.

### M4: Dashboard and Public Demo Plan

Goal: define the first builder-facing experience for reliability and market quality.

Acceptance criteria:

- Dashboard slices are scoped around market quality, oracle risk, liquidation health, adapter health, and execution reliability.
- Demo narrative can be used for grant review without implying trading profits.
- Public API/dashboard subset is separated from premium/commercial surfaces.

### M5: Grant Package

Goal: submit a credible grant package for public-good infrastructure.

Acceptance criteria:

- Grant narrative, budget categories, milestones, and evidence plan are ready for founder review.
- Deliverables map to public OSS artifacts.
- Commercial services are framed as future optional extensions.

### M6: Continuous Ecosystem And Business-Development Loop

Goal: keep OPRS aligned with current Solana priorities while converting source-backed ecosystem changes into qualified Blocksize partnership and product opportunities.

Acceptance criteria:

- A compact hot-state file, append-only evidence ledger, ranked opportunity pipeline, and dated checkpoint archive are maintained under `research/solana-ecosystem/`.
- Five-minute checks are delta-gated, source-bounded, and quiet when nothing material changes.
- Open Perps grant implications remain separate from adjacent Blocksize commercial opportunities.
- Each material run resolves one queued question and re-ranks the next action.
- Claims about protocols, validators, partnerships, or Foundation status are labeled as fact, inference, or verification-needed.

### M7: Live Read-Only Service Readiness

Goal: move beyond the static MVP into repeatable hosted diagnostics without introducing execution, custody, signing, or capital deployment.

Acceptance criteria:

- [Live readiness path](live-readiness-path.md) distinguishes static proof-pack hosting, live read-only services, commercial diagnostics, and any future execution pilot.
- [Railway read-only worker service plan](railway-readonly-worker-service-plan.md) exists before any server-side secret is added to Railway.
- [Read-only soak runbook](read-only-soak-runbook.md) defines the 7-day operational acceptance gate.
- Generated datasets include source, slot, provider, freshness, checksum, and scrub metadata.
- Continuous read-only runs soak for at least 7 days without secret leakage or unexplained data drift.
- Paid diagnostics and partner-support offers are framed around [read-only reliability outputs](commercial-diagnostics-brief.md), not production trading or profit claims.
- Any execution pilot remains blocked until security, legal, signer, capital, monitoring, runbook, and founder approval gates are complete.

## Active Dependencies

- Protocol diligence feeds architecture, data model, SDK design, and grant narrative.
- Architecture defines component contracts for all implementation streams.
- Data model defines adapter outputs and dry-run/replay fixtures.
- Liquidator/SDK design depends on protocol mechanics and normalized data.
- Grant positioning depends on all of the above.
- The continuous ecosystem loop feeds protocol priorities, network-regime assumptions, partner qualification, and grant-safe evidence into every milestone without expanding the read-only/dry-run scope.
- Live read-only service readiness depends on the public proof pack, source-governed protocol evidence, scrubbed datasets, Railway service separation, and explicit commercial boundary decisions.
