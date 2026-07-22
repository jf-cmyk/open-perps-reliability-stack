# Stablecoin Increase Decomposition

Observed: 2026-07-22

## Finding

DefiLlama's July 21-22 Solana daily chart increased by approximately $143.87M in dollar-pegged circulating supply. The accompanying asset snapshot attributes about $79.94M to USDT and $62.43M to USDC. Its source categories show native-minted supply rising about $144.64M while bridged supply declined about $0.78M.

## Implication

The earlier aggregate increase is better framed as analytics-reported native USDT/USDC expansion than as bridge inflow. The next useful evidence is issuer or public onchain mint-event confirmation and recipient concentration, followed by a 30-day comparison with DEX volume, perps volume, and market depth.

## Endpoint Discrepancy

A later July 22 refresh superseded the earlier two-endpoint comparison. DefiLlama's live `stablecoinchains` Solana dollar-peg total was approximately $15.408B, the July 22 `stablecoincharts/Solana` point was approximately $15.859B, and a direct sum of current Solana `peggedUSD` values in `stablecoins?includePrices=true` was approximately $16.022B. The chart exceeded the live total by $450.8M or 2.84% of the chart; components exceeded the live total by $613.7M or 3.98% of live; and components exceeded the chart by $162.9M or 1.03% of the chart.

Pinned DefiLlama source partially resolves why these surfaces differ. The live chain builder excludes assets marked `doublecounted` and deduplicates normalized chain aliases per asset. The public chain-chart aggregate is built without the `excludeDoublecounted` option, although a separate no-doublecounted series is generated for another internal map. The per-asset response does not expose the internal marker, so a naive component sum cannot reproduce the live total by construction. Exact reconciliation still requires a pinned join to the asset flags plus timestamp and price alignment.

The earlier statement that current components aligned with the live chain total is therefore retracted. The three surfaces disagree, potentially because of timestamp, asset status, duplicate or bridged representation, deduplication, or inclusion methodology. None of the gaps is evidence of a same-day inflow or outflow.

The current level is therefore unreconciled. Resolve asset inclusion, status, representation, and timestamp methodology before using any endpoint for capital-flow, whale, or demand attribution.

## Claim Boundary

This does not prove net capital inflow or outflow, identify mint recipients or whales, establish idle liquidity, or demonstrate derivatives demand. DefiLlama remains a third-party analytics source, and its live chain total currently disagrees with its latest daily chart.

## Sources

- https://stablecoins.llama.fi/stablecoincharts/Solana
- https://stablecoins.llama.fi/stablecoinchains
- https://stablecoins.llama.fi/stablecoins?includePrices=true
- https://github.com/DefiLlama/peggedassets-server/blob/8040e0c4540296ab1c6b75abf824a3fa7896d395/api2/cron-task/getStablecoinChains.ts
- https://github.com/DefiLlama/peggedassets-server/blob/8040e0c4540296ab1c6b75abf824a3fa7896d395/api2/cron-task/index.ts
