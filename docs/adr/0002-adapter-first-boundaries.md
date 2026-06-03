# ADR 0002: Adapter-First Boundaries

## Status

Proposed

## Context

Solana perps venues differ in account layouts, oracle systems, margin logic, liquidation mechanics, funding, and data access. The stack needs reusable public-good components without tying core services to one venue.

## Decision

All protocol-specific logic lives behind adapter interfaces. Core services consume canonical types, not venue-native account layouts. Adapters declare capability levels and data-quality confidence.

## Consequences

- Drift, Jupiter Perps, Phoenix, and later venues can be added without reshaping the whole stack.
- Data quality and capability limits are visible to callers.
- Read-only/dry-run boundaries are enforceable by interface design.
- Partner-required or commercial adapters can remain isolated from OSS core modules.
