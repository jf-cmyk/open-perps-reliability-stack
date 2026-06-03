# Agent Work Packages

All work packages report to the Coordinator. The first wave is active now and scoped to planning, specifications, and read-only/dry-run deliverables.

## Coordinator / PM

Owns roadmap, dependency tracking, GitHub issues, decision log, milestone acceptance criteria, and founder-facing status.

Immediate outputs:

- Roadmap and dependency map.
- GitHub milestones, labels, and issues.
- Weekly status format.
- Founder decision queue.

## Architecture Agent

Owns module boundaries, system diagrams, integration contracts, and architecture decisions.

Immediate outputs:

- Architecture v0 for protocol adapters, data layer, risk SDK, dry-run/replay, API, and dashboard.
- OSS vs commercial component map.
- ADR recommendations beyond ADR-0001.

## Protocol Agent

Owns venue diligence and adapter prioritization.

Immediate outputs:

- Target ranking for Drift, Jupiter Perps, Phoenix/orderbook-style venues, Zeta/Bullet lineage, GMTrade, Pacifica, FlashTrade, and relevant emerging venues.
- Permissionless vs partner-required matrix.
- First adapter recommendation with risks.

## Data Agent

Owns normalized schemas, backfill strategy, lineage, public dataset format, and data quality checks.

Immediate outputs:

- Entity and event model v0.
- Backfill and realtime ingest strategy.
- Sensitive-data scrubbing policy.
- Data quality acceptance tests.

## Liquidator/SDK Agent

Owns dry-run opportunity model, adapter interfaces, risk reason codes, replay fixtures, and non-signing simulations.

Immediate outputs:

- SDK interface specification.
- Candidate liquidation model.
- Risk reason-code taxonomy.
- Replay and dry-run acceptance criteria.
- Explicit production-execution exclusion list.

## Grant Positioning Agent

Owns Solana Foundation grant narrative, milestone budget, public-good framing, and application readiness.

Immediate outputs:

- One-page grant narrative.
- Milestone and budget table.
- Evidence/demo plan.
- Diligence risk register.

## Second Wave

Second-wave agents start after the v0 scope lock:

- Backend: APIs, services, queueing, storage integration, observability.
- Frontend: dashboard UX for reliability and market quality.
- Testing/QA: automated and manual acceptance matrix.
- DevOps/Ops: CI/CD, secrets policy, runbooks, environments.
- Efficiency: indexing, query, and simulation performance.
- Monetization/Marketing: commercial boundary, launch narrative, partner materials.
