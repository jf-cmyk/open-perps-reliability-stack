//! Deterministic replay fixture contracts.

use oprs_core::{DryRunStatus, OracleSnapshot, RiskReasonCode, Slot};
use serde::Deserialize;

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

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FixtureValidationCase<'a> {
    pub fixture_set_id: &'a str,
    pub manifest_json: &'a str,
    pub dry_run_output_json: &'a str,
    pub expected_status: DryRunStatus,
    pub expected_reason_codes: &'a [RiskReasonCode],
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FixtureValidationReport {
    pub fixture_set_id: String,
    pub passed: bool,
    pub failures: Vec<String>,
}

impl FixtureValidationReport {
    pub fn assert_passed(&self) {
        assert!(
            self.passed,
            "fixture {} failed validation: {:?}",
            self.fixture_set_id, self.failures
        );
    }
}

pub fn validate_fixture_case(case: FixtureValidationCase<'_>) -> FixtureValidationReport {
    let mut failures = Vec::new();

    let manifest = match serde_json::from_str::<SampleDatasetManifest>(case.manifest_json) {
        Ok(manifest) => Some(manifest),
        Err(error) => {
            failures.push(format!("manifest JSON failed to parse: {error}"));
            None
        }
    };

    if let Some(manifest) = manifest {
        if manifest.dataset_name != case.fixture_set_id {
            failures.push(format!(
                "manifest dataset_name `{}` must match fixture_set_id `{}`",
                manifest.dataset_name, case.fixture_set_id
            ));
        }
        if manifest.source_window != "synthetic-fixture" {
            failures.push(format!(
                "manifest source_window `{}` must disclose synthetic-fixture",
                manifest.source_window
            ));
        }
        if manifest.dq_status != "Warn" {
            failures.push(format!(
                "synthetic fixture manifest should warn, found `{}`",
                manifest.dq_status
            ));
        }
    }

    let dry_run = match serde_json::from_str::<SampleDryRunOutput>(case.dry_run_output_json) {
        Ok(dry_run) => Some(dry_run),
        Err(error) => {
            failures.push(format!("dry-run JSON failed to parse: {error}"));
            None
        }
    };

    if let Some(dry_run) = dry_run {
        if dry_run.summary.run_id != case.fixture_set_id {
            failures.push(format!(
                "dry-run run_id `{}` must match fixture_set_id `{}`",
                dry_run.summary.run_id, case.fixture_set_id
            ));
        }
        if dry_run.summary.mode != "Fixture" {
            failures.push(format!(
                "dry-run mode `{}` must declare Fixture mode",
                dry_run.summary.mode
            ));
        }

        let expected_status = dry_run_status_name(case.expected_status);
        if !dry_run.has_status(expected_status) {
            failures.push(format!(
                "dry-run output missing expected status `{expected_status}`"
            ));
        }

        if !dry_run.has_reason_code("ExecutionDisabledDryRun") {
            failures.push("dry-run output must include execution-disabled guardrail".to_string());
        }

        for code in case.expected_reason_codes {
            let code_name = risk_reason_code_name(*code);
            if !dry_run.has_reason_code(code_name) {
                failures.push(format!(
                    "dry-run output missing expected reason code `{code_name}`"
                ));
            }
        }

        for opportunity in &dry_run.opportunities {
            if let Some(plan) = &opportunity.tx_plan {
                if plan.requires_signer {
                    failures.push(format!(
                        "opportunity `{}` has requires_signer=true",
                        opportunity.id
                    ));
                }
                if !plan.submission_disabled {
                    failures.push(format!(
                        "opportunity `{}` has submission_disabled=false",
                        opportunity.id
                    ));
                }
            }
        }
    }

    FixtureValidationReport {
        fixture_set_id: case.fixture_set_id.to_string(),
        passed: failures.is_empty(),
        failures,
    }
}

pub fn validate_fixture_catalog(
    catalog_json: &str,
    fixture_set_ids: &[&str],
) -> FixtureValidationReport {
    let mut failures = Vec::new();

    match serde_json::from_str::<SampleFixtureCatalog>(catalog_json) {
        Ok(catalog) => {
            if catalog.schema_version != "0.1.0" {
                failures.push(format!(
                    "fixture catalog schema_version `{}` must be `0.1.0`",
                    catalog.schema_version
                ));
            }

            for fixture_set_id in fixture_set_ids {
                if !catalog
                    .fixtures
                    .iter()
                    .any(|fixture| fixture.fixture_set_id == *fixture_set_id)
                {
                    failures.push(format!(
                        "fixture catalog missing fixture_set_id `{fixture_set_id}`"
                    ));
                }
            }
        }
        Err(error) => failures.push(format!("fixture catalog JSON failed to parse: {error}")),
    }

    FixtureValidationReport {
        fixture_set_id: "fixture_catalog".to_string(),
        passed: failures.is_empty(),
        failures,
    }
}

fn dry_run_status_name(status: DryRunStatus) -> &'static str {
    match status {
        DryRunStatus::Accepted => "Accepted",
        DryRunStatus::Rejected => "Rejected",
        DryRunStatus::Unsafe => "Unsafe",
        DryRunStatus::Unsupported => "Unsupported",
        DryRunStatus::SimulationFailed => "SimulationFailed",
    }
}

#[derive(Debug, Deserialize)]
struct SampleDatasetManifest {
    dataset_name: String,
    source_window: String,
    dq_status: String,
}

#[derive(Debug, Deserialize)]
struct SampleFixtureCatalog {
    schema_version: String,
    fixtures: Vec<SampleFixtureCatalogEntry>,
}

#[derive(Debug, Deserialize)]
struct SampleFixtureCatalogEntry {
    fixture_set_id: String,
}

#[derive(Debug, Deserialize)]
struct SampleDryRunOutput {
    summary: SampleDryRunSummary,
    opportunities: Vec<SampleOpportunity>,
    gate_results: Vec<SampleGateResult>,
    simulation_results: Vec<SampleSimulationResult>,
}

impl SampleDryRunOutput {
    fn has_status(&self, status: &str) -> bool {
        self.opportunities
            .iter()
            .any(|opportunity| opportunity.decision.status == status)
            || self
                .simulation_results
                .iter()
                .any(|result| result.status == status)
    }

    fn has_reason_code(&self, reason_code: &str) -> bool {
        self.summary
            .reason_codes
            .iter()
            .any(|code| code == reason_code)
            || self
                .opportunities
                .iter()
                .any(|opportunity| opportunity.decision.has_reason_code(reason_code))
            || self
                .gate_results
                .iter()
                .any(|gate| gate.reason_codes.iter().any(|code| code == reason_code))
            || self
                .simulation_results
                .iter()
                .any(|result| result.reason_codes.iter().any(|code| code == reason_code))
    }
}

#[derive(Debug, Deserialize)]
struct SampleDryRunSummary {
    run_id: String,
    mode: String,
    reason_codes: Vec<String>,
}

#[derive(Debug, Deserialize)]
struct SampleOpportunity {
    id: String,
    tx_plan: Option<SampleTxPlan>,
    decision: SampleDecision,
}

#[derive(Debug, Deserialize)]
struct SampleTxPlan {
    requires_signer: bool,
    submission_disabled: bool,
}

#[derive(Debug, Deserialize)]
struct SampleDecision {
    status: String,
    reason_codes: Vec<String>,
}

impl SampleDecision {
    fn has_reason_code(&self, reason_code: &str) -> bool {
        self.reason_codes.iter().any(|code| code == reason_code)
    }
}

#[derive(Debug, Deserialize)]
struct SampleGateResult {
    reason_codes: Vec<String>,
}

#[derive(Debug, Deserialize)]
struct SampleSimulationResult {
    status: String,
    reason_codes: Vec<String>,
}

fn risk_reason_code_name(code: RiskReasonCode) -> &'static str {
    match code {
        RiskReasonCode::Eligible => "Eligible",
        RiskReasonCode::NotLiquidatable => "NotLiquidatable",
        RiskReasonCode::StaleOracle => "StaleOracle",
        RiskReasonCode::WideOracleConfidence => "WideOracleConfidence",
        RiskReasonCode::MissingOracle => "MissingOracle",
        RiskReasonCode::OracleMarkDivergence => "OracleMarkDivergence",
        RiskReasonCode::MissingPositionState => "MissingPositionState",
        RiskReasonCode::AdapterDecodeFailed => "AdapterDecodeFailed",
        RiskReasonCode::AdapterVersionMismatch => "AdapterVersionMismatch",
        RiskReasonCode::DataQualityLow => "DataQualityLow",
        RiskReasonCode::InsufficientLiquidity => "InsufficientLiquidity",
        RiskReasonCode::UnwindRouteUnavailable => "UnwindRouteUnavailable",
        RiskReasonCode::NegativeExpectedEdge => "NegativeExpectedEdge",
        RiskReasonCode::PriorityFeeTooHigh => "PriorityFeeTooHigh",
        RiskReasonCode::JitoTipUnknown => "JitoTipUnknown",
        RiskReasonCode::CapitalRequired => "CapitalRequired",
        RiskReasonCode::FlashLoanRequired => "FlashLoanRequired",
        RiskReasonCode::TxBuildUnsupported => "TxBuildUnsupported",
        RiskReasonCode::SimulationFailed => "SimulationFailed",
        RiskReasonCode::AccountLockRisk => "AccountLockRisk",
        RiskReasonCode::ComputeLimitRisk => "ComputeLimitRisk",
        RiskReasonCode::ProtocolReject => "ProtocolReject",
        RiskReasonCode::ExecutionDisabledDryRun => "ExecutionDisabledDryRun",
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const MARGIN_MANIFEST: &str =
        include_str!("../../../datasets/sample/drift_synthetic_margin_001/manifest.json");
    const MARGIN_DRY_RUN: &str =
        include_str!("../../../datasets/sample/drift_synthetic_margin_001/dry_run_output.json");
    const STALE_MANIFEST: &str =
        include_str!("../../../datasets/sample/drift_synthetic_stale_oracle_001/manifest.json");
    const STALE_DRY_RUN: &str = include_str!(
        "../../../datasets/sample/drift_synthetic_stale_oracle_001/dry_run_output.json"
    );
    const WIDE_MANIFEST: &str =
        include_str!("../../../datasets/sample/drift_synthetic_wide_confidence_001/manifest.json");
    const WIDE_DRY_RUN: &str = include_str!(
        "../../../datasets/sample/drift_synthetic_wide_confidence_001/dry_run_output.json"
    );
    const MISSING_MANIFEST: &str =
        include_str!("../../../datasets/sample/drift_synthetic_missing_oracle_001/manifest.json");
    const MISSING_DRY_RUN: &str = include_str!(
        "../../../datasets/sample/drift_synthetic_missing_oracle_001/dry_run_output.json"
    );
    const DIVERGENCE_MANIFEST: &str = include_str!(
        "../../../datasets/sample/drift_synthetic_oracle_divergence_001/manifest.json"
    );
    const DIVERGENCE_DRY_RUN: &str = include_str!(
        "../../../datasets/sample/drift_synthetic_oracle_divergence_001/dry_run_output.json"
    );
    const VERSION_MANIFEST: &str = include_str!(
        "../../../datasets/sample/drift_synthetic_adapter_version_mismatch_001/manifest.json"
    );
    const VERSION_DRY_RUN: &str = include_str!(
        "../../../datasets/sample/drift_synthetic_adapter_version_mismatch_001/dry_run_output.json"
    );
    const CATALOG: &str = include_str!("../../../datasets/sample/fixture_catalog.json");

    #[test]
    fn validates_fixture_catalog_membership() {
        validate_fixture_catalog(
            CATALOG,
            &[
                "drift_synthetic_margin_001",
                "drift_synthetic_stale_oracle_001",
                "drift_synthetic_wide_confidence_001",
                "drift_synthetic_missing_oracle_001",
                "drift_synthetic_oracle_divergence_001",
                "drift_synthetic_adapter_version_mismatch_001",
            ],
        )
        .assert_passed();
    }

    #[test]
    fn validates_margin_fixture_guardrails() {
        validate_fixture_case(FixtureValidationCase {
            fixture_set_id: "drift_synthetic_margin_001",
            manifest_json: MARGIN_MANIFEST,
            dry_run_output_json: MARGIN_DRY_RUN,
            expected_status: DryRunStatus::Unsupported,
            expected_reason_codes: &[RiskReasonCode::ExecutionDisabledDryRun],
        })
        .assert_passed();
    }

    #[test]
    fn validates_stale_oracle_fixture_guardrails() {
        validate_fixture_case(FixtureValidationCase {
            fixture_set_id: "drift_synthetic_stale_oracle_001",
            manifest_json: STALE_MANIFEST,
            dry_run_output_json: STALE_DRY_RUN,
            expected_status: DryRunStatus::Rejected,
            expected_reason_codes: &[
                RiskReasonCode::StaleOracle,
                RiskReasonCode::ExecutionDisabledDryRun,
            ],
        })
        .assert_passed();
    }

    #[test]
    fn validates_wide_confidence_fixture_guardrails() {
        validate_fixture_case(FixtureValidationCase {
            fixture_set_id: "drift_synthetic_wide_confidence_001",
            manifest_json: WIDE_MANIFEST,
            dry_run_output_json: WIDE_DRY_RUN,
            expected_status: DryRunStatus::Rejected,
            expected_reason_codes: &[
                RiskReasonCode::WideOracleConfidence,
                RiskReasonCode::ExecutionDisabledDryRun,
            ],
        })
        .assert_passed();
    }

    #[test]
    fn validates_missing_oracle_fixture_guardrails() {
        validate_fixture_case(FixtureValidationCase {
            fixture_set_id: "drift_synthetic_missing_oracle_001",
            manifest_json: MISSING_MANIFEST,
            dry_run_output_json: MISSING_DRY_RUN,
            expected_status: DryRunStatus::Rejected,
            expected_reason_codes: &[
                RiskReasonCode::MissingOracle,
                RiskReasonCode::ExecutionDisabledDryRun,
            ],
        })
        .assert_passed();
    }

    #[test]
    fn validates_oracle_divergence_fixture_guardrails() {
        validate_fixture_case(FixtureValidationCase {
            fixture_set_id: "drift_synthetic_oracle_divergence_001",
            manifest_json: DIVERGENCE_MANIFEST,
            dry_run_output_json: DIVERGENCE_DRY_RUN,
            expected_status: DryRunStatus::Rejected,
            expected_reason_codes: &[
                RiskReasonCode::OracleMarkDivergence,
                RiskReasonCode::ExecutionDisabledDryRun,
            ],
        })
        .assert_passed();
    }

    #[test]
    fn validates_adapter_version_mismatch_fixture_guardrails() {
        validate_fixture_case(FixtureValidationCase {
            fixture_set_id: "drift_synthetic_adapter_version_mismatch_001",
            manifest_json: VERSION_MANIFEST,
            dry_run_output_json: VERSION_DRY_RUN,
            expected_status: DryRunStatus::Rejected,
            expected_reason_codes: &[
                RiskReasonCode::AdapterVersionMismatch,
                RiskReasonCode::ExecutionDisabledDryRun,
            ],
        })
        .assert_passed();
    }
}
