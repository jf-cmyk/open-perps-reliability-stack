# ADR 0004: Deterministic Replay Before Shadow Mode

## Status

Proposed

## Context

The stack should not claim reliability or liquidation readiness from incomplete perps data. Existing research has strong lending-liquidation fixtures, while perps-specific decoded liquidation corpora still need to be built.

## Decision

Every liquidation/risk claim must be backed by deterministic fixtures or historical replay before any live shadow-mode milestone. Live shadow mode remains read-only and dry-run only.

## Consequences

- Adapter changes can be regression-tested against known fixtures.
- Public reports can distinguish observed evidence from inference.
- Dry-run quality improves before any production execution review.
- Production execution remains blocked until separate signer, security, capital, and operations approvals exist.
