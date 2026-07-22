# Blocksize Pay.sh Provider

Observed: 2026-07-22

## Finding

Blocksize Market Data is live in Solana Foundation's Pay.sh catalog under `blocksize/market-data`. The registry entry was added on June 10, 2026 and points to `https://mcp.blocksize.info`. Its committed OpenAPI snapshot lists four x402 endpoints: BTC-USD bid/ask, BTC-USD VWAP, EURUSD FX, and XAUUSD metals, priced from $0.002 to $0.005 per call.

The committed OpenAPI server is the direct Blocksize service. An unpaid request to the VWAP path returned x402 v2 HTTP 402 with exact-payment options for Solana-mainnet USDC and Base USDC. No payment was attempted, so successful settlement, routing through Pay.sh infrastructure, and revenue remain unverified.

## Blocksize Opportunity

The existing catalog presence removes most channel-discovery risk for commercial read-only APIs. The next bounded extension is one reliability or proof-pack endpoint under the same provider family, with the open OPRS public-good layer kept free and paid hosting, freshness, or higher-service guarantees separated.

## Claim Boundary

The catalog verifies distribution metadata, not a formal partnership, Foundation endorsement, current uptime, successful payments, users, customers, revenue, profitability, or demand.

## Sources

- https://github.com/solana-foundation/pay-skills/tree/d005f07ed3f247559341abae68c0ce60d99c6eee/providers/blocksize/market-data
- https://pay.sh/
- https://mcp.blocksize.info/v1/vwap/BTC-USD
