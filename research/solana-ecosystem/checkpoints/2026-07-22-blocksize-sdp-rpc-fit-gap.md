# Blocksize / SDP RPC Fit-Gap

Observed: 2026-07-22

Sources:

- https://platform.solana.com/provider-onboarding/rpc-providers.pdf
- https://blocksize.info/

## Decision

Public evidence is insufficient to establish that Blocksize passes SDP RPC-provider onboarding. This is an evidence-readiness gap, not proof that Blocksize fails technically.

## Hard Gates

| SDP criterion | Public Blocksize evidence | Status |
| --- | --- | --- |
| Full standard JSON-RPC and versioned transactions | Site says Blocksize runs RPC nodes where needed; no Solana RPC endpoint or compliance results published | Unverified |
| Transaction landing reliability | No 100+ transaction benchmark, leader-connectivity evidence, or retry results | Unverified |
| Devnet and mainnet-beta endpoints | No public endpoints identified | Unverified |
| Standard reads below 200ms p95 | No 24-hour Solana RPC latency results | Unverified |
| 99.5%+ Solana endpoint uptime for six months | Oracle-network uptime claims and monitored failover are not endpoint-specific history | Unverified |
| Rate limiting and capacity | No Solana RPC rate-limit policy or load-test evidence | Unverified |
| Incident response | 24/7 monitoring is stated; no Solana RPC incident policy or history is published | Partial signal; gate unverified |
| Six months production RPC and paying customers | Operating-business signals are public; Solana RPC tenure and paying customers are not | Partial signal; gate unverified |
| No disqualifying events | Requires self-attestation and public-record review | Unverified |

## Scored Criteria

The strongest public fit is Solana infrastructure expertise: Blocksize identifies Solana validator operations, RPC-node operations, and oracle publishing. General market-data API documentation and an institutional contact provide partial developer-experience and business-maturity signals.

No public evidence supports scoring Solana RPC latency/throughput, landing rate, freshness/commitment consistency, enhanced RPC APIs, websocket/geyser streaming, Solana RPC SLA quality, dedicated support, custom limits, or compliance certification.

## Minimum Evidence Packet

- Functional devnet and mainnet-beta endpoints plus automated JSON-RPC compliance output.
- At least 100 test transactions compared with the SDP landing baseline.
- A 24-hour latency report and load/capacity test.
- Six months of endpoint-specific uptime, status history, incidents, and maintenance policy.
- Published limits and increase mechanism.
- Production tenure and paying-customer attestation.
- P50/P99 geography, slot-lag/commitment consistency, enhanced APIs, streaming, documentation/dashboard, SLA/support, and compliance evidence for scoring.

## Grant Safety

Keep this opportunity adjacent to OPRS. Do not imply that Blocksize has applied, passed, been approved, or received Foundation endorsement.
