# Protocol Targets

This is the coordinator-level target sheet. The Protocol Agent owns diligence details and will replace placeholder confidence levels with sourced findings.

## Selection Criteria

- Read-only data access is available without partner approval.
- Docs, IDLs, or open-source clients are available.
- Protocol exposes perps or price-discovery data useful for public reliability metrics.
- Margin, oracle, liquidation, funding, and execution surfaces can be normalized.
- Adapter work produces public-good value even before any commercial integration.
- Dry-run candidate detection can be tested without signing or live execution.

## Initial Target Matrix

| Protocol / Venue | Role | Expected Integration Type | Why It Matters | Initial Priority |
| --- | --- | --- | --- | --- |
| Drift | Perps venue | Likely permissionless read-only, deeper execution may require more diligence | Rich perps mechanics, liquidations, oracle risk, funding, and keeper ecosystem | High |
| Jupiter Perps | Perps venue | Read-only likely feasible, execution/liquidation path needs diligence | Major user-facing perps surface and useful oracle/pool contrast | High |
| Phoenix / orderbook-style venues | Price-discovery primitive | Permissionless read-only expected where programs/data are public | Useful for market-quality and price-discovery benchmarks | Medium-high |
| Zeta / Bullet lineage | Perps/options lineage | Needs current-state diligence | Relevant Solana derivatives history and possible adapter lessons | Medium |
| FlashTrade | Perps venue | Needs docs/IDL and partner-dependency diligence | Active perps venue candidate with market-quality relevance | Medium |
| GMTrade | Perps venue | Needs docs/IDL and partner-dependency diligence | Active venue candidate for breadth and comparison | Medium |
| Pacifica | Perps venue | Needs docs/IDL and partner-dependency diligence | Active venue candidate for breadth and comparison | Medium |
| Other emerging venues | Discovery lane | Case by case | Keeps stack current as Solana perps market changes | Watch |

## First Recommendation Pending

The expected first adapter path is:

1. Start with the protocol that has the best combination of public docs/IDLs, permissionless read surfaces, liquidation/risk relevance, and stable account schemas.
2. Add one price-discovery/orderbook adapter for market-quality benchmarking.
3. Keep partner-required or execution-dependent integrations out of the first read-only milestone.

The Protocol Agent will produce the final first-adapter recommendation.
