# ADR 0003: OSS and Commercial Separation

## Status

Proposed

## Context

The project has both public-good grant outputs and possible future commercial services. Some surrounding Express Relay components may have license or private-strategy constraints.

## Decision

The public repo contains schemas, SDKs, read-only adapters, dry-run tooling, sample datasets, and public dashboard/API surfaces. Commercial/private systems contain live execution, signer/capital controls, premium APIs, private reliability intelligence, managed integrations, and any restricted-license infrastructure.

## Consequences

- Grant deliverables stay public, reusable, and auditable.
- Production execution is impossible inside v0 OSS modules.
- BUSL/private code is not copied into public grant modules without an explicit license decision.
- Future commercial services can build on the OSS foundation without privatizing grant-funded outputs.
