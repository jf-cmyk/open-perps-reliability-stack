# Solana Ecosystem Loop Bootstrap

Date: 2026-07-21

## Current Position

OPRS has moved beyond concept stage. The workspace contains a Rust reliability stack, normalized contracts, read-only and dry-run boundaries, fixture-backed Drift work, Jupiter source-authority analysis, Phoenix telemetry research, proof-pack surfaces, hosted artifacts, and grant materials. The remaining work is evidence completion, partner qualification, and careful scope control.

The Solana Expert task still exists and has retained research deltas. It was functioning as a passive memory thread; the new loop makes the workspace files the canonical state and uses the expert task for synthesis and specialist follow-up.

## New Material Finding

Solana Developer Platform now documents a self-service infrastructure-provider onboarding path and publishes detailed RPC-provider assessment criteria:

- Onboarding: https://platform.solana.com/docs/reference/provider-onboarding
- RPC criteria: https://platform.solana.com/provider-onboarding/rpc-providers.pdf

Facts:

- Hard gates cover standard JSON-RPC, transaction landing reliability, devnet and mainnet endpoints, sub-200ms p95 standard-read latency, six months at 99.5 percent or better uptime, capacity, incident response, and operating maturity.
- Performance and reliability account for 50 percent of the scored evaluation.
- Solana ecosystem depth accounts for 25 percent and includes enhanced APIs, validator/core expertise, and streaming support.
- Providers passing all gates and a 3.0 composite threshold may be added to the SDP round-robin pool; inclusion is not an endorsement.

Inference:

This is a high-priority Blocksize business-development lane because Blocksize's stated assets include Solana RPC, state-data infrastructure, and validator operations. The first step is evidence qualification, not outreach: map every hard gate and scoring item to public proof or a missing-evidence request.

Grant safety:

The official criteria are safe to cite. It is not safe to claim that Blocksize qualifies, has applied, is approved, or is endorsed without direct confirmation.

