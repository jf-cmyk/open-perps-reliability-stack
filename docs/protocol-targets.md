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
| Phoenix / Rise | Orderbook/perps telemetry | Public HTTP/WS SDK surfaces; some onboarding may be gated | Strong orderbook, market-data, fills, depth, funding, and Hawkeye-view telemetry lane | 3 |
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

Current Phoenix/Rise public package status: `examples/public/phoenix-market-telemetry-v0/` maps source-backed public HTTP and WebSocket market-data surfaces for exchange snapshots, market configuration, L2 orderbook snapshots, market-statistics history, funding-rate history, and live L2 streams. The current source-authority note in [Phoenix / Rise source authority](phoenix-source-authority.md) pins the production Phoenix program ID, log authority, global configuration, and Hawkeye view program ID from the Ellipsis Labs Rise public source. This is still a static market-telemetry and source-planning package only. It does not claim live API capture, trader-state decode, instruction-builder use, order operations, signing, transaction submission, liquidation replay, deployed-bytecode equivalence, oracle-input identity, or historical reconstruction.

Current local Phoenix public HTTP probe command:

```bash
scripts/discover_phoenix_market_telemetry.py --out target/oprs-phoenix-market-telemetry/latest.json
scripts/validate_phoenix_market_telemetry_probe.py target/oprs-phoenix-market-telemetry/latest.json
```

The discovery command calls only the public `GET /v1/exchange/snapshot` endpoint, records capped shape summaries, and does not commit raw response bodies, account addresses, auth material, trader state, instruction-builder output, order routes, signing, transaction submission, or replay evidence. The validator enforces the local probe contract without making CI depend on live external API access.

## Source-Backed Notes: 2026-06-04

Drift:

- Drift docs describe the Solana program account model around state, markets, user accounts, orders, oracle guards, fee structures, and account relationships: `https://docs.drift.trade/developers/concepts/account-model`
- Drift liquidation docs describe liquidation as position transfers between accounts, open-source liquidators/keepers, and oracle-price-based liquidation behavior: `https://docs.drift.trade/liquidations/liquidators`
- Drift liquidation-engine docs emphasize partial liquidation, throttling across slots, and oracle guardrails against bad price prints: `https://docs.drift.trade/protocol/trading/liquidations/liquidation-engine`

Jupiter Perps:

- Jupiter docs describe perps as a trader-to-LP model where traders borrow from the Jupiter Liquidity Pool: `https://docs.jup.ag/user-docs/trade/perps-and-jlp`
- Jupiter is relevant for OPRS because it is a major Solana perps surface, but it should be treated as a distinct pool/custody/oracle model rather than a Drift-style margin-account clone.
- Initial Jupiter target should be read-only market/pool/oracle/account state and public analytics, not execution, order placement, or keeper automation.
- Jupiter `Position` and `PositionRequest` docs support field planning, but canonical source authority remains blocked until the confirmation package in [Jupiter position authority confirmation](jupiter-position-authority-confirmation.md) lands.

Phoenix / Rise:

- Phoenix/Rise docs expose developer-facing SDKs with HTTP/WS data, exchange/market/trader state, orderbook/fill/candle/funding-style data, instruction builders, and Hawkeye view/simulation helpers: `https://docs.phoenix.trade/sdk/rise`
- OPRS should use Phoenix first as a read-only market-quality, orderbook, BBO, funding, and Hawkeye-view telemetry lane. Any invite activation, referral activation, trader onboarding, instruction-builder, order-submission, signing, custody, or capital surface remains out of scope.

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

Current Drift state/market/oracle discovery command:

```bash
scripts/discover_drift_readonly_state.py --out target/oprs-drift-readonly-state/latest.json
scripts/discover_drift_readonly_state.py --include-shape-snapshot --out target/oprs-drift-readonly-state/latest-shape.json
scripts/discover_drift_readonly_state.py --include-public-fields --out target/oprs-drift-readonly-state/latest-public-fields.json
```

This command derives public Drift PDAs from pinned official SDK source and probes the Drift state account, SOL/BTC/ETH perp market accounts, USDC/SOL spot market accounts, and deduplicated oracle accounts through Helius `getAccountInfo` data slices. Its optional public-field mode confirms selected perp/spot identity, oracle identity, spot decimals, market index, pool id, and selected guardrail fields for selected Drift accounts without emitting raw bytes. It emits only scrubbed local output under `target/`, does not print the RPC URL, and does not claim market-economics decoding or historical liquidation replay.

Current Jupiter Perps target discovery command:

```bash
scripts/discover_jupiter_perps_readonly_targets.py --out target/oprs-jupiter-perps-readonly-targets/latest.json
scripts/discover_jupiter_perps_transaction_history.py --limit 10 --transaction-limit 6 --min-shared-keys 2 --out target/oprs-jupiter-perps-transaction-history/latest-pairs.json
scripts/audit_jupiter_source_authority.py --out target/oprs-jupiter-source-authority/latest.json
```

The target command resolves the Jupiter Perpetuals program, documented custody accounts, and documented oracle accounts from current official Jupiter docs and probes public metadata through Helius `getAccountInfo` data slices. The transaction-history command samples public program signatures, structural transaction summaries, shared-account-key lifecycle candidates, and metadata-only shared-account probes through read-only Solana RPC. It labels stronger unverified candidates when shared Jupiter-owned non-executable accounts are seen, but does not claim verified request/fulfillment pairing. The public proof pack now includes `examples/public/jupiter-authority-gap-v0/` and `datasets/sample/jupiter_synthetic_lifecycle_candidate_unverified_001/` to make that blocker explicit. Both live commands emit scrubbed local output under `target/`, do not print the RPC URL, and do not call `/order`, `/execute`, `/build`, `/submit`, auth, keeper, or signing paths.

Current status:

- Local Helius access is confirmed for target discovery.
- Drift program account, state account, selected perp/spot market accounts, and selected oracle account metadata are readable without signer or wallet access.
- Drift decoder/IDL provenance is pinned in [Drift decoder provenance](drift-decoder-provenance.md), and optional Drift public-field decode now confirms selected perp/spot identity, oracle identity, metadata, and guardrail fields without market-economics decode.
- Jupiter Perps program, documented custody accounts, and documented oracle accounts are readable without signer or wallet access.
- Jupiter Perps public program signatures and transaction summaries are sampleable without signer or wallet access, and candidate lifecycle pairs can be produced from shared public account keys plus metadata-only account probes. Wider samples can label stronger candidates when shared Jupiter-owned non-executable accounts are seen. The authority-gap package records the exact blockers, and verified request/fulfillment pairing is not yet claimed.
- Jupiter Perps has a docs-linked IDL candidate recorded in [Jupiter Perps provenance](jupiter-perps-provenance.md) and [Jupiter source authority audit](jupiter-source-authority-audit.md), but still needs canonical IDL/source confirmation before binary decode proof.
- The exact Jupiter `Position` / `PositionRequest` confirmation ask is captured in [Jupiter position authority confirmation](jupiter-position-authority-confirmation.md).
- Phoenix/Rise now has a source-backed public market-telemetry readiness package, a bounded local public HTTP probe, and a pinned source-authority note for production program and Hawkeye view constants. No live Phoenix responses are committed, and Phoenix account decode, trader monitoring, oracle-input identity, liquidation replay, and historical reconstruction are not claimed.
- Next proof design is tracked in [Helius read-only proof plan](helius-readonly-proof.md).
