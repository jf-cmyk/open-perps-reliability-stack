//! Deterministic replay fixture contracts.

use oprs_core::{DryRunStatus, OracleSnapshot, RiskReasonCode, Slot};
use oprs_data::{validate_public_dataset_scrub_text, ScrubViolation};
use serde::Deserialize;
use sha2::{Digest, Sha256};

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
    pub content_files: &'a [FixtureContent<'a>],
    pub expected_status: DryRunStatus,
    pub expected_reason_codes: &'a [RiskReasonCode],
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FixtureContent<'a> {
    pub path: &'a str,
    pub bytes: &'a [u8],
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
        validate_manifest_checksums(&manifest, case.content_files, &mut failures);
    }

    validate_fixture_scrub_policy(&case, &mut failures);

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
    checksum: String,
    content_checksums: Vec<String>,
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

fn validate_manifest_checksums(
    manifest: &SampleDatasetManifest,
    content_files: &[FixtureContent<'_>],
    failures: &mut Vec<String>,
) {
    if !manifest.checksum.starts_with("sha256:") {
        failures.push("manifest checksum must use sha256 prefix".to_string());
    }
    if manifest.checksum.contains("synthetic-") {
        failures.push("manifest checksum must not be a placeholder synthetic label".to_string());
    }
    if manifest.content_checksums.is_empty() {
        failures.push("manifest content_checksums must list at least one file".to_string());
    }

    for entry in &manifest.content_checksums {
        let Some((expected_hash, path)) = parse_checksum_entry(entry) else {
            failures.push(format!("invalid content checksum entry `{entry}`"));
            continue;
        };

        if !path.starts_with("datasets/sample/") {
            failures.push(format!(
                "content checksum path `{path}` must be repo-relative under datasets/sample"
            ));
        }
        if path.contains("/manifest.json") {
            failures.push(format!(
                "content checksum path `{path}` must not include the self-referential manifest"
            ));
        }

        match content_files.iter().find(|file| file.path == path) {
            Some(file) => {
                let actual_hash = sha256_hex(file.bytes);
                if actual_hash != expected_hash {
                    failures.push(format!(
                        "content checksum mismatch for `{path}`: expected `{expected_hash}`, got `{actual_hash}`"
                    ));
                }
            }
            None => failures.push(format!(
                "manifest content checksum references missing validation file `{path}`"
            )),
        }
    }
}

fn validate_fixture_scrub_policy(case: &FixtureValidationCase<'_>, failures: &mut Vec<String>) {
    let manifest_path = format!("datasets/sample/{}/manifest.json", case.fixture_set_id);
    append_scrub_failures(
        validate_public_dataset_scrub_text(&manifest_path, case.manifest_json),
        failures,
    );

    let dry_run_path = format!(
        "datasets/sample/{}/dry_run_output.json",
        case.fixture_set_id
    );
    append_scrub_failures(
        validate_public_dataset_scrub_text(&dry_run_path, case.dry_run_output_json),
        failures,
    );

    for file in case.content_files {
        match std::str::from_utf8(file.bytes) {
            Ok(text) => append_scrub_failures(
                validate_public_dataset_scrub_text(file.path, text),
                failures,
            ),
            Err(error) => failures.push(format!(
                "fixture content `{}` must be UTF-8 for scrub validation: {error}",
                file.path
            )),
        }
    }
}

fn append_scrub_failures(violations: Vec<ScrubViolation>, failures: &mut Vec<String>) {
    for violation in violations {
        failures.push(format!(
            "scrub policy violation in `{}`: {} ({})",
            violation.path,
            violation.kind.label(),
            violation.evidence
        ));
    }
}

fn parse_checksum_entry(entry: &str) -> Option<(&str, &str)> {
    let (hash, path) = entry.split_once(' ')?;
    let hash = hash.strip_prefix("sha256:")?;
    if hash.len() != 64 || !hash.bytes().all(|byte| byte.is_ascii_hexdigit()) {
        return None;
    }
    if path.is_empty() {
        return None;
    }
    Some((hash, path))
}

fn sha256_hex(bytes: &[u8]) -> String {
    let digest = Sha256::digest(bytes);
    let mut output = String::with_capacity(64);
    for byte in digest {
        output.push_str(&format!("{byte:02x}"));
    }
    output
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
            content_files: margin_content_files(),
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
            content_files: stale_content_files(),
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
            content_files: wide_content_files(),
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
            content_files: missing_content_files(),
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
            content_files: divergence_content_files(),
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
            content_files: version_content_files(),
            expected_status: DryRunStatus::Rejected,
            expected_reason_codes: &[
                RiskReasonCode::AdapterVersionMismatch,
                RiskReasonCode::ExecutionDisabledDryRun,
            ],
        })
        .assert_passed();
    }

    #[test]
    fn rejects_fixture_content_checksum_mismatch() {
        let report = validate_fixture_case(FixtureValidationCase {
            fixture_set_id: "drift_synthetic_stale_oracle_001",
            manifest_json: STALE_MANIFEST,
            dry_run_output_json: STALE_DRY_RUN,
            content_files: &[FixtureContent {
                path: "datasets/sample/drift_synthetic_stale_oracle_001/dry_run_output.json",
                bytes: MISSING_DRY_RUN.as_bytes(),
            }],
            expected_status: DryRunStatus::Rejected,
            expected_reason_codes: &[
                RiskReasonCode::StaleOracle,
                RiskReasonCode::ExecutionDisabledDryRun,
            ],
        });

        assert!(!report.passed);
        assert!(report
            .failures
            .iter()
            .any(|failure| failure.contains("content checksum mismatch")));
    }

    #[test]
    fn rejects_dataset_scrub_policy_failures() {
        let report = validate_fixture_case(FixtureValidationCase {
            fixture_set_id: "drift_synthetic_margin_001",
            manifest_json: r#"{
                "dataset_name": "drift_synthetic_margin_001",
                "source_window": "synthetic-fixture",
                "dq_status": "Warn",
                "checksum": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
                "content_checksums": [
                  "sha256:0000000000000000000000000000000000000000000000000000000000000000 datasets/sample/drift_synthetic_margin_001/dry_run_output.json"
                ],
                "source_ref": "https://mainnet.helius-rpc.com/?api-key=secret"
            }"#,
            dry_run_output_json: r#"{
                "summary": {
                  "run_id": "drift_synthetic_margin_001",
                  "mode": "Fixture",
                  "reason_codes": ["ExecutionDisabledDryRun"]
                },
                "opportunities": [{
                  "id": "invalid_scrub_case",
                  "wallet_inventory": {"USDC": "1000"},
                  "execution_policy": {"max_slippage_bps": 5},
                  "tx_plan": {"requires_signer": false, "submission_disabled": true},
                  "decision": {
                    "status": "Unsupported",
                    "reason_codes": ["ExecutionDisabledDryRun"]
                  }
                }],
                "gate_results": [{"reason_codes": ["ExecutionDisabledDryRun"]}],
                "simulation_results": [{
                  "status": "Unsupported",
                  "reason_codes": ["ExecutionDisabledDryRun"]
                }]
            }"#,
            content_files: &[FixtureContent {
                path: "datasets/sample/drift_synthetic_margin_001/dry_run_output.json",
                bytes: br#"{
                  "raw_path": "/Users/founder/private/snapshot.json",
                  "auth": "Bearer abc123",
                  "note": "load .env before replay",
                  "private_key": "redacted-but-invalid"
                }"#,
            }],
            expected_status: DryRunStatus::Unsupported,
            expected_reason_codes: &[RiskReasonCode::ExecutionDisabledDryRun],
        });

        assert!(!report.passed);
        for expected in [
            "rpc_url_with_api_key",
            "bearer_token",
            "local_absolute_path",
            "env_reference",
            "private_key_material",
            "signer_or_wallet_metadata",
            "capital_or_execution_policy",
        ] {
            assert!(
                report
                    .failures
                    .iter()
                    .any(|failure| failure.contains(expected)),
                "missing {expected} in {:?}",
                report.failures
            );
        }
    }

    #[test]
    fn validates_expanded_dry_run_reason_code_fixture_coverage() {
        let cases = [
            (RiskReasonCode::NotLiquidatable, DryRunStatus::Rejected),
            (RiskReasonCode::MissingPositionState, DryRunStatus::Rejected),
            (RiskReasonCode::AdapterDecodeFailed, DryRunStatus::Rejected),
            (RiskReasonCode::DataQualityLow, DryRunStatus::Rejected),
            (
                RiskReasonCode::InsufficientLiquidity,
                DryRunStatus::Rejected,
            ),
            (RiskReasonCode::NegativeExpectedEdge, DryRunStatus::Rejected),
            (
                RiskReasonCode::TxBuildUnsupported,
                DryRunStatus::Unsupported,
            ),
            (
                RiskReasonCode::SimulationFailed,
                DryRunStatus::SimulationFailed,
            ),
            (RiskReasonCode::ComputeLimitRisk, DryRunStatus::Rejected),
            (RiskReasonCode::ProtocolReject, DryRunStatus::Rejected),
        ];

        for (reason_code, status) in cases {
            let reason_code_name = risk_reason_code_name(reason_code);
            let dry_run_output_json = dry_run_fixture_with_reason(reason_code_name, status);
            validate_fixture_case(FixtureValidationCase {
                fixture_set_id: "drift_synthetic_margin_001",
                manifest_json: MARGIN_MANIFEST,
                dry_run_output_json: &dry_run_output_json,
                content_files: margin_content_files(),
                expected_status: status,
                expected_reason_codes: &[reason_code, RiskReasonCode::ExecutionDisabledDryRun],
            })
            .assert_passed();
        }
    }

    fn dry_run_fixture_with_reason(reason_code: &str, status: DryRunStatus) -> String {
        let status_name = dry_run_status_name(status);
        format!(
            r#"{{
                "summary": {{
                  "run_id": "drift_synthetic_margin_001",
                  "mode": "Fixture",
                  "reason_codes": ["{reason_code}", "ExecutionDisabledDryRun"]
                }},
                "opportunities": [{{
                  "id": "expanded_reason_{reason_code}",
                  "tx_plan": {{"requires_signer": false, "submission_disabled": true}},
                  "decision": {{
                    "status": "{status_name}",
                    "reason_codes": ["{reason_code}", "ExecutionDisabledDryRun"]
                  }}
                }}],
                "gate_results": [{{
                  "reason_codes": ["{reason_code}", "ExecutionDisabledDryRun"]
                }}],
                "simulation_results": [{{
                  "status": "{status_name}",
                  "reason_codes": ["{reason_code}", "ExecutionDisabledDryRun"]
                }}]
            }}"#
        )
    }

    fn margin_content_files() -> &'static [FixtureContent<'static>] {
        &[
            FixtureContent {
                path: "datasets/sample/drift_synthetic_margin_001/README.md",
                bytes: include_bytes!(
                    "../../../datasets/sample/drift_synthetic_margin_001/README.md"
                ),
            },
            FixtureContent {
                path: "datasets/sample/drift_synthetic_margin_001/canonical_event.json",
                bytes: include_bytes!(
                    "../../../datasets/sample/drift_synthetic_margin_001/canonical_event.json"
                ),
            },
            FixtureContent {
                path: "datasets/sample/drift_synthetic_margin_001/dry_run_output.json",
                bytes: include_bytes!(
                    "../../../datasets/sample/drift_synthetic_margin_001/dry_run_output.json"
                ),
            },
            FixtureContent {
                path: "datasets/sample/drift_synthetic_margin_001/oracle_snapshot.json",
                bytes: include_bytes!(
                    "../../../datasets/sample/drift_synthetic_margin_001/oracle_snapshot.json"
                ),
            },
            FixtureContent {
                path: "datasets/sample/drift_synthetic_margin_001/position_snapshot.json",
                bytes: include_bytes!(
                    "../../../datasets/sample/drift_synthetic_margin_001/position_snapshot.json"
                ),
            },
            FixtureContent {
                path: "datasets/sample/drift_synthetic_margin_001/publish_gate.json",
                bytes: include_bytes!(
                    "../../../datasets/sample/drift_synthetic_margin_001/publish_gate.json"
                ),
            },
        ]
    }

    fn stale_content_files() -> &'static [FixtureContent<'static>] {
        &[FixtureContent {
            path: "datasets/sample/drift_synthetic_stale_oracle_001/dry_run_output.json",
            bytes: include_bytes!(
                "../../../datasets/sample/drift_synthetic_stale_oracle_001/dry_run_output.json"
            ),
        }]
    }

    fn wide_content_files() -> &'static [FixtureContent<'static>] {
        &[FixtureContent {
            path: "datasets/sample/drift_synthetic_wide_confidence_001/dry_run_output.json",
            bytes: include_bytes!(
                "../../../datasets/sample/drift_synthetic_wide_confidence_001/dry_run_output.json"
            ),
        }]
    }

    fn missing_content_files() -> &'static [FixtureContent<'static>] {
        &[FixtureContent {
            path: "datasets/sample/drift_synthetic_missing_oracle_001/dry_run_output.json",
            bytes: include_bytes!(
                "../../../datasets/sample/drift_synthetic_missing_oracle_001/dry_run_output.json"
            ),
        }]
    }

    fn divergence_content_files() -> &'static [FixtureContent<'static>] {
        &[FixtureContent {
            path: "datasets/sample/drift_synthetic_oracle_divergence_001/dry_run_output.json",
            bytes: include_bytes!("../../../datasets/sample/drift_synthetic_oracle_divergence_001/dry_run_output.json"),
        }]
    }

    fn version_content_files() -> &'static [FixtureContent<'static>] {
        &[FixtureContent {
            path: "datasets/sample/drift_synthetic_adapter_version_mismatch_001/dry_run_output.json",
            bytes: include_bytes!("../../../datasets/sample/drift_synthetic_adapter_version_mismatch_001/dry_run_output.json"),
        }]
    }
}
