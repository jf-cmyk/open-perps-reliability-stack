# Tokenized-Equity Market-State Reliability

Date: 2026-07-22

## Verified Signal

Solana Foundation's July 10 SK Hynix report describes three Solana representations of the same equity exposure with materially different mechanics: SKHY through Sunrise and Backpack Securities, SKHYx through xStocks, and SKHYon through Ondo. The report describes 24/7 transfer for SKHYx and SKHYon, 24/5 minting and redemption for SKHYon, and different dividend handling through rebasing or reinvestment.

The Foundation's July 1 Sunrise report says canonical external-asset mints generated more than $3.5B across 14M trades and roughly 221K wallets in the first six months through mid-June 2026. These are Foundation-reported aggregates, not independently reproduced measurements.

## Ondo Adapter Surface

Ondo's official Global Markets API documentation provides a concrete read-only schema for representation-aware monitoring. The asset-status endpoint exposes scheduled and unscheduled restrictions with symbol, active/upcoming status, reason, start/end time, event ID, and whether the shares multiplier will change. Documented reasons include dividends, splits, mergers, acquisitions, spinoffs, earnings, and maintenance. The per-asset market endpoint separates `primaryMarket` token data from `underlyingMarket` stock data and exposes tradable sessions, `sharesMultiplier`, and an update timestamp.

Both endpoints require an API key. Ondo explicitly describes the market-data prices as display-only, does not recommend them as an oracle, and says an official oracle is in development. Public documentation was not enough to verify that SKHYon currently resolves through these endpoints.

## Blocksize Opportunity

Build a read-only market-state evidence layer that identifies the exact token representation and records:

- underlying exchange open, closed, halted, or unavailable state;
- reference-price timestamp and age;
- Solana venue versus underlying and cross-representation divergence;
- oracle source and freshness where public;
- corporate-action treatment;
- published mint and redemption availability.

This is adjacent to OPRS today and becomes directly relevant when a perpetual or other derivative references a tokenized external asset. The smallest validation artifact is a schema-first SKHY-family comparison using verified mint addresses and issuer terms, with status and corporate-action evidence separated from non-oracle display prices.

## Claim Boundary

Do not treat these checks as certification of securities compliance, collateral, legal ownership, redemption, fair value, liquidity, eligibility, or oracle correctness. Do not use Ondo's documented display prices as a production oracle or claim SKHYon API availability without a verified response. The official sources establish product descriptions and an implementation schema; they do not establish buyer demand, Blocksize relationships, or a pricing failure.

## Sources

- https://solana.com/news/skhy-is-now-live
- https://solana.com/news/how-external-assets-start-trading-on-solana-from-day-one
- https://docs.ondo.finance/api-reference/status/get-asset-statuses
- https://docs.ondo.finance/api-reference/assets/get-market-data-for-an-asset
