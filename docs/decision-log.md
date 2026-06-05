# Decision Log

Use this file as the index for project decisions. Larger decisions should become ADRs under `docs/adr/`.

## Open Decisions

| ID | Decision | Owner | Needed By | Status |
| --- | --- | --- | --- | --- |
| D-001 | Confirm first protocol targets | Founder + Coordinator | M0 | Accepted |
| D-002 | Confirm OSS vs commercial boundary | Founder + Architecture + Grant | M0 | Accepted |
| D-003 | Confirm grant milestone budget range | Founder + Grant | M5 draft | Open |
| D-004 | Confirm dashboard/API public subset | Founder + Architecture + Data | M4 | Open |
| D-005 | Confirm production execution remains out of scope through v0 | Founder + Coordinator | M0 | Accepted |
| D-006 | Confirm Railway as canonical reviewer URL | Founder + DevOps | M1 | Accepted |
| D-007 | Confirm Drift/read-only targets for Helius decode proof | Founder + Architecture + Data | M1 | Accepted |
| D-008 | Confirm branded domain and Railway service naming | Founder + DevOps | M1 | Open |

## Decision Template

```md
# Decision: <short title>

Date:
Owner:
Status: Proposed | Accepted | Rejected | Superseded

## Context

## Options Considered

## Decision

## Rationale

## Scope Impact

## OSS/Commercial Impact

## Security or Execution Impact

## Dependencies

## Follow-up Actions

## Review Date
```

## Accepted Decisions

| ID | Decision | Record |
| --- | --- | --- |
| ADR-0001 | Read-only and dry-run first | [ADR-0001](adr/0001-read-only-dry-run-first.md) |
| D-002 | OSS and commercial tracks are both in scope, but grant-funded artifacts stay public and reproducible | [OSS and commercial boundary](oss-commercial-boundary.md) |
| D-005 | Production execution, signing, custody, private-key handling, live transaction submission, and capital deployment remain out of scope through v0 | [ADR-0001](adr/0001-read-only-dry-run-first.md) |
| D-009 | Railway proof-pack image excludes project-memory checkpoints while GitHub keeps them for development continuity | [Public artifact boundary](public-artifact-boundary.md) |
| D-010 | Helius RPC belongs only in local or separate read-only decode-worker contexts, never in the static Railway proof-pack service | [Service boundaries](service-boundaries.md) |
| D-006 | Railway is canonical for grant reviewers; GitHub Pages remains an equivalent fallback mirror | [Railway deployment](deployment-railway.md) |
| D-011 | Protocol target order is Drift first, Jupiter second, Phoenix/Rise telemetry third, with FlashTrade/Adrena/Pacifica/Zeta-Bullet as follow-on diligence | [Protocol targets](protocol-targets.md) |
| D-001 | First protocol targets confirmed as Drift first, Jupiter second, Phoenix/Rise third, then FlashTrade/Adrena/Pacifica/Zeta-Bullet diligence | [Protocol targets](protocol-targets.md) |
| D-007 | Drift read-only target discovery confirmed for program, state, selected market, and selected oracle metadata through local Helius proof commands | [Helius read-only proof plan](helius-readonly-proof.md) |
