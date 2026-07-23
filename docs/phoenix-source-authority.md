# Phoenix / Rise Source Authority

This note records the current Phoenix/Rise source-authority position for OPRS. It supports read-only market telemetry, source-pinned program-address planning, and future Hawkeye view simulation design. It does not authorize order placement, trader onboarding, instruction submission, signing, custody, capital deployment, or production execution.

## Current Source Anchor

| Item | Value |
| --- | --- |
| Public repository | `Ellipsis-Labs/rise-public` |
| Repository URL | `https://github.com/Ellipsis-Labs/rise-public` |
| Default branch | `master` |
| Current reviewed commit | `09f59aaf06037ecff395a6c47eea7440f9eef7c2` |
| Commit message | `sync: Rise Rust v0.3.4 from phoenix 6051225fb045 (#71)` |
| Commit verification | GitHub reports valid verified signature |
| Rust release | `rise-rust-v0.3.4`, published 2026-07-08 |
| TypeScript release | `rise-ts-v0.4.66`, published 2026-07-08 |
| Source Phoenix commit named by releases | `6051225fb045fbb5b6a454bd445e7fc2e31e5722` |

The current public repo is a stronger source anchor than the prior third-party-only program-ID note because it is published under Ellipsis Labs and the official Phoenix docs link to the Rise public source.

## Program And View Constants

Pinned file: `rust/ix/src/constants.rs` at commit `09f59aaf06037ecff395a6c47eea7440f9eef7c2`.

| Constant | Value | OPRS use |
| --- | --- | --- |
| `PROD_PHOENIX_PROGRAM_ID` | `EtrnLzgbS7nMMy5fbD42kXiUzGg8XQzJ972Xtk1cjWih` | Production Phoenix/Rise program address for source-pinned planning. |
| `BETA_PHOENIX_PROGRAM_ID` | `phDEVv4w6BcfkLrLNeXr8HhhgQxnxziVGXpGPcaadMf` | Beta address only; do not cite as production. |
| `PROD_PHOENIX_LOG_AUTHORITY` | `GdxfTLSsdSY37G6fZoYtdGDSfgFnbT2EmRpuePZxWShS` | Required account for future instruction/account-map review only. |
| `PROD_PHOENIX_GLOBAL_CONFIGURATION` | `2zskx2iyCvb6Stg7RBZkt1f6MrF4dpYtMG3yMvKwqtUZ` | Required account for future read-only account-map review only. |
| `EMBER_PROGRAM_ID` | `EMBERpYNE6ehWmXymZZS2skiFmCa9V5dp14e1iduM5qy` | Collateral conversion dependency; outside grant execution scope. |
| `FLIGHT_PROGRAM_ID` | `F1ightu9cujFYo34k9CabifLrJT8qzfDVM2Q7BqhJn2W` | Routing/builder dependency; outside grant execution scope. |

Pinned files: `rust/ix/src/hawkeye.rs` and `ts/src/hawkeye.ts` at commit `09f59aaf06037ecff395a6c47eea7440f9eef7c2`.

| Constant / Surface | Value | OPRS use |
| --- | --- | --- |
| `HAWKEYE_PROGRAM_ID` / `HAWKEYE_PROGRAM_ADDRESS` | `RiSeVw3ZjNfsaXPRb4mgaqYaEEt41pNNJoDvVh7pgQj` | Read-only simulation/view design for margin, asset, liquidation-price, BBO, and funding return data. |
| Hawkeye return version | `1` | Version gate for future return-data decoder. |
| Hawkeye views | margin, asset, liquidation price, BBO, funding | Candidate future read-only diagnostic surfaces only. |

## Live Public API Corroboration

A live public exchange snapshot may corroborate source constants for local research, but OPRS must not commit raw live responses into public packages. The current public API lane is bounded to scrubbed shape summaries under `target/`.

The Phoenix source-authority sidecar observed `https://perp-api.phoenix.trade/v1/exchange/snapshot` returning these public metadata fields on 2026-07-23:

| Field | Value |
| --- | --- |
| `programId` | `EtrnLzgbS7nMMy5fbD42kXiUzGg8XQzJ972Xtk1cjWih` |
| `globalConfig` | `2zskx2iyCvb6Stg7RBZkt1f6MrF4dpYtMG3yMvKwqtUZ` |
| `canonicalMint` | `PhUsd11YkbjSaWjFncfAAmatntsjx3MgDR9B6g1ks3A` |
| `usdcMint` | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |
| `perpAssetMap` | `2nHGAaEw3D5dd4hVueaUNoygkQFmoeKqRQWnSPqSMFUC` |
| `globalTraderIndex` | `HCrPXLByGqRh2szQi3gj7oRdRVBNi1gccAyn4CQCT3HK` |
| `activeTraderBuffer` | `2U32rSzzrQS3eVmGHsnbw5kcqKF3wQXpHGd3hMq5YJok` |

Observed GOLD market metadata from the same public snapshot:

| Field | Value |
| --- | --- |
| `assetId` | `65556` |
| `marketPubkey` | `7B7hDscDNBGFpNGypFygoiANCpdM3JR2PY3JbvPvQtmk` |
| `splinePubkey` | `4Xf7mkyTyWfiWnRo4oHjfwopSF46aLk8XciWotfG8voB` |
| `isolatedOnly` | `true` |

## Current Decision

Status: `source_pinned_for_program_and_hawkeye_view_planning`.

Allowed:

- Cite the production Phoenix/Rise program ID from the pinned Ellipsis Labs Rise source.
- Cite the beta program ID only as beta.
- Keep Phoenix/Rise in scope as a read-only market-quality, orderbook, BBO, funding, and Hawkeye-view research lane.
- Use official HTTP/WS market-data surfaces for source-backed telemetry planning.
- Design a local Hawkeye simulation/view decoder only after source-review records, local validation, and public scrub checks pass.

Blocked:

- Order placement, order cancellation, trader registration, referral activation, invite activation, builder onboarding, transaction building for submission, signing, fee-payer use, custody, capital movement, or live execution.
- Claims that Phoenix account-level decode, liquidation replay, trader monitoring, or historical reconstruction is ready.
- Claims that the beta address is the production program.
- Claims that source constants alone prove deployed bytecode equivalence, audit coverage, oracle composition, or live market correctness.
- Claims that Flight routing, builder registration, referral activation, or invite activation are part of the grant MVP.

## Next Implementation Step

Add a Phoenix/Hawkeye read-only source-review validator path before any account-level example is promoted. That validator should require:

- pinned Rise repo commit and release tag
- production program ID, log authority, global configuration, and Hawkeye program ID
- Hawkeye return-data layout version
- local-only simulation or fixture validation
- scrubbed output under `target/`
- all forbidden execution, signing, custody, and capital claims set to false
