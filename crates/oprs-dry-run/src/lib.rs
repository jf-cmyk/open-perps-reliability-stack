//! Dry-run liquidation contracts.

use oprs_core::{
    Decimal, DryRunStatus, MarginState, OracleSnapshot, PositionSnapshot, RiskReasonCode, Slot,
};
use oprs_replay::FixtureManifest;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DryRunMode {
    Replay,
    LiveShadow,
    Fixture,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum GateStatus {
    Pass,
    Warn,
    Fail,
    Skipped,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GateResult {
    pub gate_id: String,
    pub status: GateStatus,
    pub reason_codes: Vec<RiskReasonCode>,
    pub message: String,
}

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
    pub address_lookup_tables: Vec<String>,
    pub estimated_compute_units: Option<u64>,
    pub requires_signer: bool,
    pub submission_disabled: bool,
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

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SimulationResult {
    pub status: DryRunStatus,
    pub reason_codes: Vec<RiskReasonCode>,
    pub error: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DryRunSummary {
    pub run_id: String,
    pub schema_version: String,
    pub mode: DryRunMode,
    pub adapter: String,
    pub adapter_version: String,
    pub policy_id: Option<String>,
    pub started_at_unix: i64,
    pub completed_at_unix: i64,
    pub opportunities_scanned: u64,
    pub opportunities_accepted: u64,
    pub opportunities_rejected: u64,
    pub reason_codes: Vec<RiskReasonCode>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DryRunOutputBundle {
    pub summary: DryRunSummary,
    pub opportunities: Vec<LiquidationOpportunity>,
    pub gate_results: Vec<GateResult>,
    pub simulation_results: Vec<SimulationResult>,
    pub fixture_manifest: Option<FixtureManifest>,
}

pub fn execution_disabled_decision() -> DryRunDecision {
    DryRunDecision {
        status: DryRunStatus::Unsupported,
        reason_codes: vec![RiskReasonCode::ExecutionDisabledDryRun],
        human_summary: "Production execution is disabled in read-only/dry-run scope.".to_string(),
    }
}
