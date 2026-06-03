//! Deterministic replay fixture contracts.

use oprs_core::{DryRunStatus, OracleSnapshot, RiskReasonCode, Slot};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FixtureSource {
    Historical,
    Synthetic,
    ResearchCsv,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FixtureManifest {
    pub manifest_version: String,
    pub fixture_set_id: String,
    pub adapter_version: String,
    pub fixtures: Vec<FixtureRef>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FixtureRef {
    pub id: String,
    pub source: FixtureSource,
    pub path: String,
    pub checksum: String,
    pub expected_status: DryRunStatus,
    pub expected_reason_codes: Vec<RiskReasonCode>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ReplayFixture {
    pub id: String,
    pub venue: String,
    pub source: FixtureSource,
    pub slot: Option<Slot>,
    pub time_unix: Option<i64>,
    pub adapter_version: String,
    pub oracle_snapshots: Vec<OracleSnapshot>,
    pub expected: ExpectedDryRunResult,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ExpectedDryRunResult {
    pub status: DryRunStatus,
    pub reason_codes: Vec<RiskReasonCode>,
}
