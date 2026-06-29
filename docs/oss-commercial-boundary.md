# OSS and Commercial Boundary

The grant-funded/public repo must stay public, read-only, reproducible, and dry-run only.

## Open-Source Public-Good Scope

- Adapter standard.
- Sample/fixture adapters.
- Read-only protocol adapters.
- Normalized schemas.
- Pyth-aware risk SDK.
- Dry-run and replay harness.
- Public API schemas.
- Public dashboard subset.
- Sample datasets.
- Docs, ADRs, and grant milestone artifacts.
- Source-backed ecosystem context about public Solana reliability trends, including validator readiness, when clearly marked as context and not as a running OPRS service.

## Commercial or Private Scope

- Premium low-latency APIs.
- Private execution analytics.
- Managed protocol integrations.
- Proprietary routing.
- Validator-specific performance intelligence.
- Private validator telemetry, validator routing, skip-rate optimization, block-propagation optimization, XDP/kernel tuning, priority-fee strategy, and block-engine strategy.
- Live liquidation services.
- Signer infrastructure.
- Capital/inventory controls.
- Partner-specific adapters under NDA.
- SLA-backed services.
- Any BUSL/private Express Relay auction-server reuse unless explicitly licensed.

## Boundary Rules

- OSS modules must not depend on private execution, signer, capital, validator-routing, or BUSL auction-server code.
- Public datasets must be scrubbed for secrets, private routing, internal infra, and strategy fields.
- Commercial work may build on public artifacts, but cannot privatize grant-funded deliverables.
- Production execution requires a separate approval package and does not belong in v0.
