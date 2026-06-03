# Protocol Targets

This is the coordinator-level target sheet. The Protocol Agent owns diligence details and will replace placeholder confidence levels with sourced findings.

## Selection Criteria

- Read-only data access is available without partner approval.
- Docs, IDLs, or open-source clients are available.
- Protocol exposes perps or price-discovery data useful for public reliability metrics.
- Margin, oracle, liquidation, funding, and execution surfaces can be normalized.
- Adapter work produces public-good value even before any commercial integration.
- Dry-run candidate detection can be tested without signing or live execution.

## Target Matrix

| Protocol / Venue | Role | Expected Integration Type | Why It Matters | Initial Priority |
| --- | --- | --- | --- | --- |
| Drift v2 | Perps venue | Permissionless read-only and dry-run; live liquidation is out of scope | Best OSS/public-good fit, open program/SDK, rich margin/oracle/liquidation mechanics | 1 |
| Phoenix / orderbook-style venues | Price-discovery primitive | Phoenix legacy is public; Phoenix Perps/Rise may be API/onboarding-gated | Best price-discovery/orderbook telemetry lane | 2 |
| Jupiter Perps | Perps venue | Public read-only; execution/keeper path is Jupiter-operated | Major user-facing perps surface and useful oracle/pool contrast | 3 |
| FlashTrade | Pool perps venue | Public docs/GitHub/SDK; team-operated liquidation bot per docs | Good oracle/pool-perps telemetry target | 4 |
| GMTrade | Pool perps venue | Docs plus Rust SDK; deeper decode validation needed | Good GMX-v2-style pool venue and RWA/perps surface | 5 |
| Pacifica | API-centric perps venue | Public REST/WS API; likely partner/API-gated for deeper integration | Valuable commercial/API data adapter, weaker OSS-first fit | 6 |
| Zeta / Bullet lineage | Perps/options lineage | Zeta legacy public; Bullet is newer and likely partner-led | Useful research precedent, not first adapter | 7 |
| Other emerging venues | Discovery lane | Case by case | Keeps stack current as Solana perps market changes | Watch |

## First Recommendation

Build `DriftReadOnlyAdapter` first.

Drift is the cleanest first adapter because it has public mechanics, open-source program/SDK surface, actual liquidation and margin complexity, and a strong Solana public-good story. It should decode and simulate only:

- Markets, user accounts, positions, open orders, funding, and oracle state.
- Canonical margin health and liquidation eligibility.
- `LiquidationCandidate`, `OracleRiskSnapshot`, and `MarketQualitySnapshot`.
- Dry-run liquidation simulation using fixtures or local simulation.

Add Phoenix/orderbook telemetry in parallel for spread/depth/fill/latency baselines. Add Jupiter Perps next to contrast oracle/pool/keeper models.
