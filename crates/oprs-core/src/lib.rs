//! Canonical public types for the Open Perps Reliability Stack.
//!
//! This crate is intentionally read-only and dry-run oriented. It must not grow
//! signer, custody, wallet, capital allocation, or live transaction submission
//! surfaces.

pub type Decimal = i128;
pub type Slot = u64;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AdapterCapability {
    ReadOnly,
    Simulate,
    ExecuteDisabled,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum VenueKind {
    Perps,
    Lending,
    Swap,
    Orderbook,
    Unknown,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OracleSource {
    Pyth,
    PythLazer,
    Switchboard,
    Chainlink,
    Fixture,
    Adapter,
    Unknown,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MarketType {
    Perp,
    Spot,
    Prediction,
    Unknown,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PositionSide {
    Long,
    Short,
    CollateralizedDebt,
    Unknown,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DryRunStatus {
    Accepted,
    Rejected,
    Unsafe,
    Unsupported,
    SimulationFailed,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RiskReasonCode {
    Eligible,
    NotLiquidatable,
    StaleOracle,
    WideOracleConfidence,
    MissingOracle,
    OracleMarkDivergence,
    MissingPositionState,
    AccountStateMismatch,
    InvalidAccountSet,
    AdapterDecodeFailed,
    AdapterVersionMismatch,
    DataQualityLow,
    InsufficientLiquidity,
    UnwindRouteUnavailable,
    NegativeExpectedEdge,
    PriorityFeeTooHigh,
    JitoTipUnknown,
    CapitalRequired,
    FlashLoanRequired,
    TxBuildUnsupported,
    SimulationFailed,
    ComputeBudgetExceeded,
    BlockhashExpired,
    AccountLockContention,
    PriorityFeeUnderbid,
    TransactionDroppedUnknown,
    AccountLockRisk,
    ComputeLimitRisk,
    ProtocolReject,
    ExecutionDisabledDryRun,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AdapterMetadata {
    pub adapter_name: String,
    pub adapter_version: String,
    pub protocol: String,
    pub network: String,
    pub venue_kind: VenueKind,
    pub program_ids: Vec<String>,
    pub account_schema_version: String,
    pub supported_account_schema_versions: Vec<String>,
    pub idl_hash: Option<String>,
    pub source_updated_at_unix: Option<i64>,
    pub docs_url: Option<String>,
    pub data_quality: DataQuality,
    pub caveats: Vec<String>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DataQuality {
    High,
    Medium,
    Low,
    Unknown,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MarketSnapshot {
    pub venue: String,
    pub market_id: String,
    pub base_asset: String,
    pub quote_asset: String,
    pub market_type: MarketType,
    pub observed_slot: Slot,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OracleFeedRef {
    pub feed_id: String,
    pub source: OracleSource,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OracleSnapshot {
    pub feed_id: String,
    pub price: Decimal,
    pub confidence: Decimal,
    pub exponent: i32,
    pub publish_time_unix: i64,
    pub received_at_unix: Option<i64>,
    pub slot: Option<Slot>,
    pub source: OracleSource,
    pub raw_ref: Option<String>,
    pub raw_hash: Option<String>,
    pub quality_flags: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OracleRiskSnapshot {
    pub feed_id: String,
    pub stale: bool,
    pub confidence_bps: Option<i64>,
    pub divergence_bps: Option<i64>,
    pub reason_codes: Vec<RiskReasonCode>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PositionQuery {
    pub market_id: Option<String>,
    pub owner: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PositionSnapshot {
    pub venue: String,
    pub market_id: String,
    pub position_id: String,
    pub owner: Option<String>,
    pub side: PositionSide,
    pub base_amount: Option<Decimal>,
    pub quote_notional_usd: Option<Decimal>,
    pub collateral_usd: Option<Decimal>,
    pub observed_slot: Slot,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MarginState {
    pub maintenance_margin_usd: Decimal,
    pub collateral_usd: Decimal,
    pub initial_margin_usd: Option<Decimal>,
    pub unrealized_pnl_usd: Option<Decimal>,
    pub health_ratio_bps: Option<i64>,
    pub liquidation_price: Option<Decimal>,
    pub is_liquidatable: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LiquidationStateInput {
    pub position: PositionSnapshot,
    pub oracle: OracleSnapshot,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LiquidationState {
    pub is_candidate: bool,
    pub margin: MarginState,
    pub reason_codes: Vec<RiskReasonCode>,
}
