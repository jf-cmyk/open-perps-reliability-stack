# Phoenix External-Asset Perpetuals

Observed: 2026-07-22

## Verified Fact

Solana Foundation reports that Phoenix launched 24/7 onchain gold and crude-oil perpetuals in May 2026. Phoenix's official `GOLD` market surface exposes mark and index prices, 24-hour volume, open interest, one-hour funding, and isolated-margin labeling. Phoenix documentation says its mark price combines an adjusted oracle price, Phoenix order-book data, and external perpetual prices. Official docs and terms describe access as private beta, pre-release, or geographically restricted.

Sources:

- https://solana.com/news/solana-ecosystem-roundup-may-2026
- https://www.phoenix.trade/GOLD
- https://docs.phoenix.trade/phoenix/perpetual-futures

## Blocksize And OPRS Implication

Phoenix creates a direct external-asset perps reliability target. A read-only adapter can distinguish whether the underlying commodity reference market is open, closed, or stale; measure mark/index/reference divergence and component freshness; track funding continuity, liquidity depth, and liquidation evidence; and preserve venue-access state separately from onchain protocol state.

## Evidence Boundary

The public market and semantic surfaces do not verify Phoenix's canonical program/source, exact oracle providers or external-perp inputs, account layouts, historical events, liquidity quality, fair pricing, unrestricted access, production readiness, customer demand, Blocksize integration, partnership, or causal risk reduction.

## Next Action

Pin Phoenix's canonical program and source, identify exact oracle and external-perpetual inputs, map the public `GOLD` telemetry into the OPRS adapter contract, and verify one public transaction or account pair without executing a trade.
