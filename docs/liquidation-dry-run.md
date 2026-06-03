# Liquidation Dry-Run and Replay

This document specifies Liquidator/SDK v0 for the Open Perps Reliability
Stack. The v0 scope is read-only and dry-run only: protocol state decoding,
risk classification, deterministic replay, and non-signing transaction-plan
simulation. It must not sign, custody funds, submit live transactions, or make
production execution decisions.

## Goals

- Define stable SDK interfaces for protocol adapters, oracle/risk inputs,
  liquidation eligibility, replay fixtures, and dry-run simulation.
- Produce deterministic reason codes that explain why a candidate is accepted,
  rejected, unsafe, unavailable, or unsupported.
- Let builders replay known liquidation windows and compare adapter behavior
  across versions.
- Support public-good documentation, sample datasets, and integration tests
  without exposing private execution strategy.

## Non-Goals

- No private-key handling, signer abstraction, wallet loading, or custody.
- No live transaction submission, retry policy, or production execution router.
- No capital allocation, inventory carry, flash-loan execution, or unwind desk.
- No profitability claims against incumbent liquidators.
- No protocol backstop, liquidation auction settlement, or partner-only
  production integration.

## Adapter Interfaces

Adapters normalize venue-specific state into SDK types. Each adapter declares
its capability level so callers cannot accidentally treat a read-only adapter as
an executable strategy.

```ts
export type AdapterCapability = "read_only" | "simulate" | "execute_disabled";

export interface VenueAdapter {
  metadata(): AdapterMetadata;
  capabilities(): AdapterCapability[];
  markets(): Promise<MarketSnapshot[]>;
  oracleFeeds(marketId: string): Promise<OracleFeedRef[]>;
  positions(input: PositionQuery): Promise<PositionSnapshot[]>;
  marginState(position: PositionSnapshot, oracle: OracleSnapshot): MarginState;
  liquidationState(input: LiquidationStateInput): LiquidationState;
  buildDryRunLiquidation(input: LiquidationBuildInput): DryRunTxPlan;
  decodeEvent(input: DecodeEventInput): DecodedVenueEvent[];
  fixtureLoader(): ReplayFixtureLoader;
}
```

```ts
export interface OracleAdapter {
  latest(feed: OracleFeedRef): Promise<OracleSnapshot>;
  validate(snapshot: OracleSnapshot, policy: OraclePolicy): OracleRiskResult;
  confidenceAdjustedPrice(snapshot: OracleSnapshot, side: "bid" | "ask"): Decimal;
  divergence(input: OracleDivergenceInput): OracleDivergenceResult;
}
```

```ts
export interface SimulationAdapter {
  requiredAccounts(plan: DryRunTxPlan): AccountRef[];
  simulate(plan: DryRunTxPlan, fixture?: ReplayFixture): Promise<SimulationResult>;
  classifyFailure(result: SimulationResult): RiskReasonCode[];
}
```

Adapters should be implemented in Rust first for deterministic core logic, with
TypeScript bindings or mirrored types for dashboard/API consumers. TypeScript
can be first for integration scaffolding if Drift or another venue has a faster
SDK path, but replay classification should remain byte-for-byte reproducible.

## Canonical Data Types

```ts
export interface AdapterMetadata {
  adapterName: string;
  adapterVersion: string;
  protocol: string;
  network: string;
  venueKind: "perps" | "lending" | "swap" | "unknown";
  programIds: string[];
  accountSchemaVersion: string;
  supportedAccountSchemaVersions: string[];
  idlHash?: string;
  sourceUpdatedAt?: string;
  docsUrl?: string;
  dataQuality: "high" | "medium" | "low" | "unknown";
  caveats: string[];
}

export interface OracleSnapshot {
  feedId: string;
  price: Decimal;
  confidence: Decimal;
  exponent: number;
  publishTime: string;
  receivedAt?: string;
  slot?: number;
  source: "pyth" | "pyth_lazer" | "fixture" | "adapter";
  rawRef?: string;
  rawHash?: string;
  qualityFlags: string[];
}

export interface PositionSnapshot {
  venue: string;
  marketId: string;
  positionId: string;
  owner?: string;
  side: "long" | "short" | "collateralized_debt" | "unknown";
  baseAmount?: Decimal;
  quoteNotionalUsd?: Decimal;
  collateralUsd?: Decimal;
  rawAccounts: AccountRef[];
  observedSlot: number;
}

export interface MarginState {
  initialMarginUsd?: Decimal;
  maintenanceMarginUsd: Decimal;
  collateralUsd: Decimal;
  unrealizedPnlUsd?: Decimal;
  healthRatio?: Decimal;
  liquidationPrice?: Decimal;
  isLiquidatable: boolean;
}
```

## Liquidation Opportunity Model

The dry-run engine emits a `LiquidationOpportunity` for every candidate that
passes basic decode and account-shape checks, even if it is rejected later by
risk or simulation gates.

```ts
export interface LiquidationOpportunity {
  id: string;
  venue: string;
  venueKind: "perps" | "lending" | "swap" | "unknown";
  marketId: string;
  positionId: string;
  observedSlot: number;
  observedAt: string;
  adapterVersion: string;
  oracle: OracleSnapshot;
  position: PositionSnapshot;
  margin: MarginState;
  terms: LiquidationTerms;
  costs: EstimatedLiquidationCosts;
  edge: EstimatedLiquidationEdge;
  requiredCapital: RequiredCapital;
  txPlan?: DryRunTxPlan;
  decision: DryRunDecision;
  simulation?: SimulationResult;
  traceId: string;
}

export interface LiquidationTerms {
  closeSizeUsd?: Decimal;
  repayAsset?: string;
  receiveAsset?: string;
  penaltyBps?: number;
  protocolFeeBps?: number;
  maxCloseFraction?: Decimal;
}

export interface EstimatedLiquidationCosts {
  priorityFeeUsd?: Decimal;
  jitoTipUsd?: Decimal;
  slippageUsd?: Decimal;
  unwindUsd?: Decimal;
  borrowOrFundingUsd?: Decimal;
  failureHaircutUsd?: Decimal;
}

export interface EstimatedLiquidationEdge {
  grossBonusUsd?: Decimal;
  netAfterCostsUsd?: Decimal;
  confidence: "high" | "medium" | "low" | "unknown";
  assumptions: string[];
}

export interface DryRunDecision {
  status: "accepted" | "rejected" | "unsafe" | "unsupported" | "sim_failed";
  reasonCodes: RiskReasonCode[];
  humanSummary: string;
}
```

## Risk Reason Codes

Reason codes are stable API values. They should be lower-case in JSON and
upper snake case in Rust/TypeScript enums.

| Code | Meaning |
| --- | --- |
| `eligible` | Candidate is liquidatable under adapter math and policy. |
| `not_liquidatable` | Position is healthy or below liquidation threshold. |
| `stale_oracle` | Oracle publish time or slot is outside policy. |
| `wide_oracle_confidence` | Confidence interval exceeds policy threshold. |
| `missing_oracle` | Required oracle snapshot is unavailable. |
| `oracle_mark_divergence` | Oracle and executable venue price diverge too far. |
| `missing_position_state` | Required position or margin account is unavailable. |
| `adapter_decode_failed` | Adapter could not decode required state. |
| `adapter_version_mismatch` | Fixture or state uses an unsupported schema version. |
| `data_quality_low` | Inputs are proxy-only, incomplete, or not reproducible. |
| `insufficient_liquidity` | Repay/receive asset route or depth is inadequate. |
| `unwind_route_unavailable` | No modeled route exists for received collateral. |
| `negative_expected_edge` | Net estimated edge is non-positive after costs. |
| `priority_fee_too_high` | Required fee consumes too much expected edge. |
| `jito_tip_unknown` | Tip burden cannot be estimated from current data. |
| `capital_required` | Opportunity requires capital not modeled in OSS dry-run. |
| `flash_loan_required` | Viability depends on flash-loan execution. |
| `tx_build_unsupported` | Adapter cannot produce a dry-run transaction plan. |
| `simulation_failed` | Local or fixture simulation failed. |
| `account_lock_risk` | Writable account set is likely contested. |
| `compute_limit_risk` | Compute budget estimate is above policy. |
| `protocol_reject` | Venue program rejects the constructed plan. |
| `execution_disabled_dry_run` | Candidate is blocked because v0 cannot execute. |

## Replay Fixtures

Replay fixtures should be small, deterministic, and versioned. A fixture can be
backed by CSV/JSONL research rows, raw transaction/account snapshots, or a
synthetic state vector. Each fixture must include expected reason codes.

The `oprs-replay` crate includes a dependency-light fixture validator for the
current JSON sample set. It checks that fixture manifests disclose synthetic
source windows, carry warning-level DQ status, and that dry-run outputs include
the expected status, reason codes, fixture mode, and `execution_disabled_dry_run`
guardrail.

Run the current sample validation suite with:

```bash
cargo run -p oprs-replay --example validate_fixtures
```

```ts
export interface ReplayFixture {
  id: string;
  venue: string;
  source: "historical" | "synthetic" | "research_csv";
  slot?: number;
  timeUtc?: string;
  adapterVersion: string;
  accounts?: AccountFixture[];
  oracleSnapshots: OracleSnapshot[];
  events?: DecodedVenueEvent[];
  expected: ExpectedDryRunResult;
}

export interface ExpectedDryRunResult {
  status: DryRunDecision["status"];
  reasonCodes: RiskReasonCode[];
  netAfterCostsUsdRange?: [Decimal, Decimal];
}
```

Initial fixture set:

- Kamino historical lending liquidation rows for model calibration and
  regression tests.
- Kamino top positive and top negative event slices for edge classification.
- Save corrected liquidation rows only; older negative proxy views should be
  excluded from acceptance tests.
- Jupiter Lend authority summaries for observed-window sanity checks.
- Phase 0 gate CSV/JSON summaries for dry-run decision gates, especially Jito
  tip unknowns, latency unknowns, and shadow-mode edge constraints.
- Drift v2 IDL-derived synthetic fixtures for perps adapter shape tests until
  decoded Drift historical perps liquidation fixtures are available.
- Current validated Drift synthetic fixtures: margin candidate execution
  disabled, stale oracle rejected, wide confidence rejected, missing oracle
  rejected, oracle/mark divergence rejected, and adapter version mismatch
  rejected.

Fixture labels must distinguish `perps` from `lending` so public outputs do not
overclaim that lending liquidation economics prove perps execution readiness.

## Simulation Gates

The dry-run engine evaluates gates in order and records every gate result.
Failure at any gate prevents later production-style actions, but later dry-run
analysis may still run if it is read-only and useful.

1. Adapter metadata gate: protocol, program IDs, schema version, and capability
   level are known.
2. Decode gate: required accounts/events decode without lossy parsing.
3. Oracle gate: price, confidence, exponent, and freshness satisfy policy.
4. Margin gate: liquidation eligibility can be reproduced deterministically.
5. Liquidity gate: repay/receive assets have modeled liquidity or are marked
   unavailable.
6. Cost gate: fees, slippage, unwind, capital, and failure haircut assumptions
   are explicit.
7. Edge gate: expected net edge is positive under policy, or rejected with
   `negative_expected_edge`.
8. Transaction-plan gate: adapter can build an unsigned dry-run plan with
   allowlisted programs only.
9. Local simulation gate: LiteSVM or fixture simulation succeeds and classifies
   failures.
10. Replay parity gate: fixture outputs match expected status and reason codes.
11. Shadow-readiness gate: live shadow reports have sufficient positive-edge
    streak and data quality before any production review.
12. Execution boundary gate: v0 always emits `execution_disabled_dry_run`.

## Dry-Run Outputs

The CLI/API should support JSONL for machines and Markdown summaries for
humans.

```json
{
  "run_id": "dryrun_2026_06_02T000000Z",
  "mode": "dry_run",
  "adapter": "drift_v2",
  "fixture_id": "drift_v2_synthetic_margin_001",
  "observed_slot": 0,
  "opportunities_scanned": 1,
  "opportunities": [
    {
      "id": "opp_001",
      "decision": {
        "status": "unsupported",
        "reason_codes": ["tx_build_unsupported", "execution_disabled_dry_run"],
        "human_summary": "Candidate decoded, but adapter cannot build a dry-run liquidation plan yet."
      }
    }
  ]
}
```

Required artifacts per run:

- `dryrun-summary.json`: counts by adapter, status, and reason code.
- `opportunities.jsonl`: one canonical `LiquidationOpportunity` per candidate.
- `gate-results.jsonl`: ordered gate outcomes for traceability.
- `simulation-results.jsonl`: simulation output and classified failures.
- `fixtures-used.json`: fixture IDs, versions, checksums, and source notes.
- `dryrun-report.md`: human-readable summary with caveats and next actions.

Public reports must redact wallet labels where source confidence is low and
must avoid firm/entity attribution unless separately validated.

## Production Execution Boundary

The v0 SDK must make production execution impossible by construction:

- No signer interface.
- No private-key parameters.
- No wallet JSON loading.
- No RPC `sendTransaction` wrapper.
- No custody, balances, treasury, or capital-limit module.
- No retry loop, route selector, Jito bidding policy, or block-engine submitter.
- No hot-wallet operations.
- No live liquidation automation.

Any future production track requires a separate approval package with signer
isolation, protocol allowlists, capital limits, loss limits, kill switches,
runbooks, security review, and explicit founder approval. Until that package is
approved, every opportunity must end with `execution_disabled_dry_run`.

## SDK Implementation Issues

Recommended v0 issue breakdown:

1. Define canonical SDK types for adapters, oracle snapshots, positions, margin
   state, liquidation opportunities, dry-run decisions, and reason codes.
2. Implement `VenueAdapter`, `OracleAdapter`, `SimulationAdapter`, and
   `ReplayFixtureLoader` interfaces.
3. Add fixture manifest schema with checksums, adapter version, source label,
   and expected reason codes.
4. Add fixture loaders for Kamino top positive/negative rows and Phase 0 gate
   summaries as calibration fixtures.
5. Add Drift v2 IDL-derived synthetic perps fixtures for adapter shape tests.
6. Implement oracle policy checks for stale price, wide confidence, missing
   feed, and oracle/mark divergence.
7. Implement dry-run gate runner with ordered gate results and trace IDs.
8. Add non-signing transaction-plan type and enforce `execute_disabled` at the
   type/API boundary.
9. Add simulation result classifier for account lock, compute, protocol reject,
   rent/funds, stale blockhash, and unknown failures.
10. Add CLI output: `dryrun-summary.json`, `opportunities.jsonl`,
    `gate-results.jsonl`, `simulation-results.jsonl`, and `dryrun-report.md`.
11. Add unit tests for every reason code and snapshot tests for fixture replay.
12. Add documentation examples showing accepted, rejected, unsafe, unsupported,
    and simulation-failed candidates.

## Acceptance Criteria

- No exported API accepts a private key, signer, wallet, or submit endpoint.
- All adapters declare capabilities and default to `execute_disabled`.
- Every dry-run opportunity includes a decision status, reason codes, and trace
  ID.
- Fixture replay is deterministic across repeated runs.
- At least one perps adapter fixture and one historical liquidation calibration
  fixture run through the same gate runner.
- Public docs clearly separate OSS dry-run infrastructure from future
  commercial or production execution services.
