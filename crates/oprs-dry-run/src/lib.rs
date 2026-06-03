//! Dry-run liquidation contracts.

use oprs_core::{
    Decimal, DryRunStatus, MarginState, OracleSnapshot, PositionSnapshot, RiskReasonCode, Slot,
};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DryRunDecision {
    pub status: DryRunStatus,
    pub reason_codes: Vec<RiskReasonCode>,
    pub human_summary: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DryRunTxPlan {
    pub unsigned_plan_id: String,
    pub allowed_programs: Vec<String>,
    pub writable_accounts: Vec<String>,
    pub estimated_compute_units: Option<u64>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LiquidationOpportunity {
    pub id: String,
    pub venue: String,
    pub market_id: String,
    pub position_id: String,
    pub observed_slot: Slot,
    pub adapter_version: String,
    pub oracle: OracleSnapshot,
    pub position: PositionSnapshot,
    pub margin: MarginState,
    pub estimated_net_usd: Option<Decimal>,
    pub tx_plan: Option<DryRunTxPlan>,
    pub decision: DryRunDecision,
    pub trace_id: String,
}

pub fn execution_disabled_decision() -> DryRunDecision {
    DryRunDecision {
        status: DryRunStatus::Unsupported,
        reason_codes: vec![RiskReasonCode::ExecutionDisabledDryRun],
        human_summary: "Production execution is disabled in read-only/dry-run scope.".to_string(),
    }
}
