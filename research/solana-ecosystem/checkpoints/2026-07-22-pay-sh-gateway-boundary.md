# Pay.sh Gateway Reliability Boundary

Observed: 2026-07-22

## Verified Fact

Solana Foundation says Pay.sh was launched in collaboration with Google Cloud and operates as an API proxy built on Google Cloud. The described gateway authorizes x402 requests through verified endpoints and applies rate limits, quotas, and access controls before stablecoin settlement and provider reconciliation. Pay.sh uses the x402 and MPP open standards. Solana's agentic-payment documentation describes x402 as a stateless HTTP challenge-and-retry flow with an optional facilitator handling verification and onchain settlement.

Sources:

- https://solana.com/news/solana-foundation-launches-pay-sh-in-collaboration-with-google-cloud
- https://solana.com/docs/payments/agentic-payments

## Blocksize Implication

Blocksize's separately verified Pay.sh catalog presence creates a low-friction distribution path for a metered OPRS reliability or proof-pack endpoint. The endpoint should expose distinct reason codes and latency spans for upstream-data failures, provider computation failures, gateway authorization or throttling, and payment or facilitator settlement. That separation keeps commercial delivery evidence compatible with OPRS's deterministic reliability model.

## Evidence Boundary

The general gateway architecture does not prove that Blocksize's current requests traverse any particular Google Cloud service or control. It does not make Blocksize a Google Cloud or Pay.sh launch partner and does not establish endorsement, successful settlement, availability, usage, customers, revenue, compliance, or demand.

## Blocksize Route Snapshot

The committed Blocksize OpenAPI sidecar names `https://mcp.blocksize.info` as its server and documents `200` and `402` responses without a separate OpenAPI security scheme. An unpaid, unauthenticated GET to `/v1/vwap/BTC-USD` returned HTTP 402 and an x402 v2 `exact` challenge for 2,000 atomic units, accepting Solana-mainnet USDC and Base USDC. No payment or challenge retry was attempted.

This verifies the direct request and challenge surface, not Pay.sh's internal proxy path or any settlement. Because two chains are offered, future Open Perps revenue-routing evidence must identify the rail actually used or constrain the paid OPRS tier to Solana; a generic x402 success would not by itself prove value returned to Solana.

## Next Action

Specify one rail-aware OPRS endpoint with source provenance, latency spans, and distinct challenge, payment, settlement-rail, provider, and upstream reason codes. Verify paid settlement only in a separately approved test; this research loop must not pay or retry the challenge.
