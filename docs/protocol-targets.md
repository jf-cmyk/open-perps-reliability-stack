# Protocol Targets

This is the coordinator-level target sheet. The Protocol Agent owns diligence details and should refresh source links before grant submission.

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
| Jupiter Perps | Perps venue | Public read-only surface; deeper onchain decode diligence needed | Major user-facing perps surface; trader-to-LP/JLP model gives a useful contrast to Drift margin/order mechanics | 2 |
| Phoenix / Rise | Orderbook/perps telemetry | Public HTTP/WS SDK surfaces; some onboarding may be gated | Best orderbook, market-data, fills, depth, and funding telemetry lane | 3 |
| FlashTrade | Pool perps venue | Public docs/GitHub/SDK; deeper account decode validation needed | Good oracle/pool-perps telemetry target with Pyth plus backup-oracle framing | 4 |
| Adrena | Pool perps venue | Public docs and open-source keeper references; deeper account decode validation needed | Useful peer-to-pool contrast with explicit oracle and keeper docs | 5 |
| Pacifica | API-centric perps venue | Public REST/WS API; trading operations require signing/auth | Valuable API data adapter, weaker OSS-first fit because core operation model is API/account based | 6 |
| Zeta / Bullet lineage | Perps/options lineage | Zeta legacy discontinued; Bullet mainnet/API maturity still developing | Useful research precedent, not first adapter | 7 |
| GMTrade / other emerging venues | Discovery lane | Case by case | Keeps stack current as Solana perps market changes | Watch |
| Other emerging venues | Discovery lane | Case by case | Keeps stack current as Solana perps market changes | Watch |

## First Recommendation

Build `DriftReadOnlyAdapter` first, then add a Jupiter Perps read-only target.

Drift is the cleanest first adapter because it has public mechanics, open-source program/SDK surface, actual liquidation and margin complexity, and a strong Solana public-good story. It should decode and simulate only:

- Markets, user accounts, positions, open orders, funding, and oracle state.
- Canonical margin health and liquidation eligibility.
- `LiquidationCandidate`, `OracleRiskSnapshot`, and `MarketQualitySnapshot`.
- Dry-run liquidation simulation using fixtures or local simulation.

Add Jupiter next because it is economically and product-wise relevant to Solana perps, but structurally different from Drift: Jupiter Perps is a trader-to-LP exchange where traders borrow from the JLP pool and liquidation/oracle behavior should be explained through pool/custody/oracle state rather than only user-margin accounts.

Add Phoenix/Rise telemetry in parallel when practical for spread, depth, fills, orderbook, funding, and latency baselines. Add FlashTrade and Adrena after the first two perps adapters to compare pool-perps oracle and keeper designs.

## Source-Backed Notes: 2026-06-04

Drift:

- Drift docs describe the Solana program account model around state, markets, user accounts, orders, oracle guards, fee structures, and account relationships: `https://docs.drift.trade/developers/concepts/account-model`
- Drift liquidation docs describe liquidation as position transfers between accounts, open-source liquidators/keepers, and oracle-price-based liquidation behavior: `https://docs.drift.trade/liquidations/liquidators`
- Drift liquidation-engine docs emphasize partial liquidation, throttling across slots, and oracle guardrails against bad price prints: `https://docs.drift.trade/protocol/trading/liquidations/liquidation-engine`

Jupiter Perps:

- Jupiter docs describe perps as a trader-to-LP model where traders borrow from the Jupiter Liquidity Pool: `https://docs.jup.ag/user-docs/trade/perps-and-jlp`
- Jupiter is relevant for OPRS because it is a major Solana perps surface, but it should be treated as a distinct pool/custody/oracle model rather than a Drift-style margin-account clone.
- Initial Jupiter target should be read-only market/pool/oracle/account state and public analytics, not execution, order placement, or keeper automation.

Phoenix / Rise:

- Phoenix/Rise docs expose developer-facing SDKs with HTTP/WS data, exchange/market/trader state, orderbook/fill/candle/funding-style data, and instruction builders: `https://docs.phoenix.trade/sdk/rise`
- OPRS should use Phoenix first as a read-only market-quality and orderbook telemetry lane. Any instruction-builder or order-submission surface remains out of scope.

FlashTrade and Adrena:

- FlashTrade docs describe a pool-to-peer model and Pyth plus backup oracle framing: `https://docs.flash.trade/`
- Adrena docs describe peer-to-pool perps, oracle dependencies, and open-source keeper references: `https://docs.adrena.trade/about-adrena/what-is-adrena`
- Adrena oracle docs describe Chaos Labs Edge as primary and Pyth as secondary source: `https://docs.adrena.xyz/technical-documentation/oracles-and-price-feeds`
- These are useful third-wave targets for oracle-risk and pool-perps reliability comparison after Drift and Jupiter.

Pacifica:

- Pacifica docs expose REST/WS APIs, but signing/auth operation docs make it a weaker OSS-first read-only adapter target: `https://docs.pacifica.fi/api-documentation/api`
- Pacifica operation docs list signed operations for trading/account actions: `https://pacifica.gitbook.io/docs/api-documentation/api/signing/operation-types`
- Treat as an API data adapter or commercial/partner diligence path, not the first Helius/onchain decode proof.

Zeta / Bullet:

- Zeta docs state Zeta Markets ceased operating as of May 2025 and point to Bullet as the successor network: `https://docs.zeta.markets/`
- Bullet documentation indicates mainnet REST is not yet the primary mature path for this grant MVP: `https://docs.bullet.xyz/bullet-network/build-on-bullet/rest-ws-apis`
- Keep this as research lineage, not an MVP adapter target.

## Helius Read-Only Decode Target Plan

The first Helius-backed decode proof should use public Drift targets because Drift has the strongest combination of public account model, SDK/program documentation, and liquidation/oracle mechanics.

Target sequence:

1. Drift market and oracle state decode.
2. Drift user/position account decode for a public account or synthetic account-shaped fixture.
3. Jupiter Perps pool/custody/oracle read-only survey.
4. Phoenix/Rise public market-data pull without transaction-building.

The decode proof must emit:

- data reconstruction envelope
- provider label, commitment, slot range, and query config
- relative public evidence refs
- scrubbed output with no RPC URL, API key, `.env`, wallet, signer, custody, capital, or execution settings

The decode proof must not:

- sign
- submit transactions
- retry transactions
- bid priority fees
- load keypairs
- manage capital
- call order, liquidation, or execution endpoints

Current local discovery command:

```bash
scripts/discover_readonly_targets.py --out target/oprs-readonly-target-discovery/latest.json
```

This first command probes the Drift protocol program account through local `HELIUS_RPC_URL`, records Jupiter and Phoenix as follow-on target lanes, and emits a scrubbed data reconstruction envelope. It intentionally writes to `target/` and does not commit live RPC output.

Current status:

- Local Helius access is confirmed for first target discovery.
- Drift program account metadata is readable without signer or wallet access.
- Jupiter Perps still needs a public pool, custody, oracle, or program-account target resolved from official sources before RPC probing.
- Next proof design is tracked in [Helius read-only proof plan](helius-readonly-proof.md).
