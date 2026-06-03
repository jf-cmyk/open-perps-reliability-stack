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

    require_contains(
        case.manifest_json,
        &format!("\"dataset_name\": \"{}\"", case.fixture_set_id),
        "manifest dataset_name must match fixture_set_id",
        &mut failures,
    );
    require_contains(
        case.manifest_json,
        "\"source_window\": \"synthetic-fixture\"",
        "manifest must disclose synthetic source_window",
        &mut failures,
    );
    require_contains(
        case.manifest_json,
        "\"dq_status\": \"Warn\"",
        "synthetic fixture manifest should warn, not pass as historical data",
        &mut failures,
    );
    require_contains(
        case.dry_run_output_json,
        &format!("\"run_id\": \"{}\"", case.fixture_set_id),
        "dry-run run_id must match fixture_set_id",
        &mut failures,
    );
    require_contains(
        case.dry_run_output_json,
        "\"mode\": \"Fixture\"",
        "dry-run output must declare Fixture mode",
        &mut failures,
    );
    require_contains(
        case.dry_run_output_json,
        &format!(
            "\"status\": \"{}\"",
            dry_run_status_name(case.expected_status)
        ),
        "dry-run output must include expected status",
        &mut failures,
    );
    require_contains(
        case.dry_run_output_json,
        "\"ExecutionDisabledDryRun\"",
        "dry-run output must include execution-disabled guardrail",
        &mut failures,
    );

    for code in case.expected_reason_codes {
        require_contains(
            case.dry_run_output_json,
            &format!("\"{}\"", risk_reason_code_name(*code)),
            "dry-run output missing expected reason code",
            &mut failures,
        );
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
    require_contains(
        catalog_json,
        "\"schema_version\": \"0.1.0\"",
        "fixture catalog must declare schema_version",
        &mut failures,
    );

    for fixture_set_id in fixture_set_ids {
        require_contains(
            catalog_json,
            &format!("\"fixture_set_id\": \"{}\"", fixture_set_id),
            "fixture catalog missing fixture_set_id",
            &mut failures,
        );
    }

    FixtureValidationReport {
        fixture_set_id: "fixture_catalog".to_string(),
        passed: failures.is_empty(),
        failures,
    }
}

fn require_contains(haystack: &str, needle: &str, message: &str, failures: &mut Vec<String>) {
    if !haystack.contains(needle) {
        failures.push(format!("{message}: expected `{needle}`"));
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
