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

        validate_dry_run_invariants(&dry_run, &mut failures);
        validate_jupiter_lifecycle_boundary(&dry_run, &mut failures);

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
    evidence_boundary: Option<SampleEvidenceBoundary>,
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
struct SampleEvidenceBoundary {
    protocol: String,
    source_authority_status: String,
    canonical_decode_authorized: bool,
    verified_request_fulfillment_pair_claimed: bool,
    request_account_decoded: bool,
    position_account_decoded: bool,
    raw_transaction_committed: bool,
    raw_instruction_data_committed: bool,
    raw_logs_committed: bool,
    candidate_strength: String,
    shared_jupiter_owned_non_executable_account_observed: bool,
    shared_account_count: u64,
    public_evidence_refs: Vec<String>,
}

#[derive(Debug, Deserialize)]
struct SampleDryRunSummary {
    run_id: String,
    schema_version: Option<String>,
    mode: String,
    started_at_unix: Option<i64>,
    completed_at_unix: Option<i64>,
    opportunities_scanned: Option<u64>,
    opportunities_accepted: Option<u64>,
    opportunities_rejected: Option<u64>,
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
    gate_id: Option<String>,
    status: Option<String>,
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

fn validate_dry_run_invariants(dry_run: &SampleDryRunOutput, failures: &mut Vec<String>) {
    if dry_run.summary.schema_version.as_deref() != Some("0.1.0") {
        failures.push("dry-run summary schema_version must be `0.1.0`".to_string());
    }

    match (
        dry_run.summary.started_at_unix,
        dry_run.summary.completed_at_unix,
    ) {
        (Some(started), Some(completed)) if completed < started => {
            failures.push(format!(
                "dry-run completed_at_unix `{completed}` must be >= started_at_unix `{started}`"
            ));
        }
        (Some(_), Some(_)) => {}
        _ => failures
            .push("dry-run summary must include started_at_unix and completed_at_unix".to_string()),
    }

    let accepted_opportunities = dry_run
        .opportunities
        .iter()
        .filter(|opportunity| opportunity.decision.status == "Accepted")
        .count() as u64;
    let rejected_opportunities = dry_run
        .opportunities
        .iter()
        .filter(|opportunity| is_rejected_status(&opportunity.decision.status))
        .count() as u64;
    let accepted_simulations = dry_run
        .simulation_results
        .iter()
        .filter(|result| result.status == "Accepted")
        .count() as u64;
    let rejected_simulations = dry_run
        .simulation_results
        .iter()
        .filter(|result| is_rejected_status(&result.status))
        .count() as u64;

    let observed_accepted = accepted_opportunities.max(accepted_simulations);
    let observed_rejected = rejected_opportunities.max(rejected_simulations);

    if let Some(summary_accepted) = dry_run.summary.opportunities_accepted {
        if summary_accepted != observed_accepted {
            failures.push(format!(
                "dry-run opportunities_accepted `{summary_accepted}` must match observed accepted `{observed_accepted}`"
            ));
        }
    } else {
        failures.push("dry-run summary must include opportunities_accepted".to_string());
    }

    if let Some(summary_rejected) = dry_run.summary.opportunities_rejected {
        if summary_rejected != observed_rejected {
            failures.push(format!(
                "dry-run opportunities_rejected `{summary_rejected}` must match observed rejected `{observed_rejected}`"
            ));
        }
    } else {
        failures.push("dry-run summary must include opportunities_rejected".to_string());
    }

    if let Some(scanned) = dry_run.summary.opportunities_scanned {
        let observed_total = observed_accepted + observed_rejected;
        if scanned != observed_total {
            failures.push(format!(
                "dry-run opportunities_scanned `{scanned}` must equal accepted + rejected `{observed_total}`"
            ));
        }
    } else {
        failures.push("dry-run summary must include opportunities_scanned".to_string());
    }

    validate_reason_code_union(dry_run, failures);
    validate_gate_invariants(dry_run, failures);
}

fn validate_reason_code_union(dry_run: &SampleDryRunOutput, failures: &mut Vec<String>) {
    let mut observed = Vec::new();
    for opportunity in &dry_run.opportunities {
        observed.extend(opportunity.decision.reason_codes.iter().cloned());
    }
    for gate in &dry_run.gate_results {
        observed.extend(gate.reason_codes.iter().cloned());
    }
    for result in &dry_run.simulation_results {
        observed.extend(result.reason_codes.iter().cloned());
    }

    observed.sort();
    observed.dedup();

    let mut summary = dry_run.summary.reason_codes.clone();
    summary.sort();
    summary.dedup();

    if observed != summary {
        failures.push(format!(
            "dry-run summary reason_codes {:?} must match observed reason-code union {:?}",
            summary, observed
        ));
    }
}

fn validate_gate_invariants(dry_run: &SampleDryRunOutput, failures: &mut Vec<String>) {
    let mut gate_ids = Vec::new();
    let mut non_pass_gate_seen = false;

    for (index, gate) in dry_run.gate_results.iter().enumerate() {
        match gate.gate_id.as_deref() {
            Some("") | None => failures.push(format!(
                "dry-run gate at index `{index}` must include a non-empty gate_id"
            )),
            Some(gate_id) => {
                if gate_ids.iter().any(|seen| seen == gate_id) {
                    failures.push(format!("dry-run gate_id `{gate_id}` must be unique"));
                }
                gate_ids.push(gate_id.to_string());
            }
        }

        match gate.status.as_deref() {
            Some("Pass") => {}
            Some("Warn" | "Fail" | "Skipped") => non_pass_gate_seen = true,
            Some(status) => failures.push(format!(
                "dry-run gate `{}` has unsupported status `{status}`",
                gate.gate_id.as_deref().unwrap_or("<missing>")
            )),
            None => failures.push(format!(
                "dry-run gate `{}` must include status",
                gate.gate_id.as_deref().unwrap_or("<missing>")
            )),
        }
    }

    if has_rejected_status(dry_run) && !non_pass_gate_seen {
        failures
            .push("rejected dry-run outputs must include at least one non-pass gate".to_string());
    }
}

fn has_rejected_status(dry_run: &SampleDryRunOutput) -> bool {
    dry_run
        .opportunities
        .iter()
        .any(|opportunity| opportunity.decision.status == "Rejected")
        || dry_run
            .simulation_results
            .iter()
            .any(|result| result.status == "Rejected")
}

fn is_rejected_status(status: &str) -> bool {
    matches!(
        status,
        "Rejected" | "Unsafe" | "Unsupported" | "SimulationFailed"
    )
}

fn validate_jupiter_lifecycle_boundary(
    dry_run: &SampleDryRunOutput,
    failures: &mut Vec<String>,
) {
    let is_jupiter_fixture = dry_run.summary.run_id.starts_with("jupiter_");
    let Some(boundary) = &dry_run.evidence_boundary else {
        if is_jupiter_fixture {
            failures.push("Jupiter fixtures must include evidence_boundary".to_string());
        }
        return;
    };

    if boundary.protocol != "jupiter_perps" {
        failures.push(format!(
            "Jupiter evidence_boundary.protocol `{}` must be jupiter_perps",
            boundary.protocol
        ));
    }
    if boundary.source_authority_status == "canonical_confirmed" {
        failures.push("Jupiter fixture must not claim canonical source authority yet".to_string());
    }
    if boundary.canonical_decode_authorized {
        failures.push("Jupiter fixture must keep canonical_decode_authorized=false".to_string());
    }
    if boundary.verified_request_fulfillment_pair_claimed {
        failures.push(
            "Jupiter fixture must keep verified_request_fulfillment_pair_claimed=false"
                .to_string(),
        );
    }
    if boundary.request_account_decoded {
        failures.push("Jupiter fixture must keep request_account_decoded=false".to_string());
    }
    if boundary.position_account_decoded {
        failures.push("Jupiter fixture must keep position_account_decoded=false".to_string());
    }
    if boundary.raw_transaction_committed
        || boundary.raw_instruction_data_committed
        || boundary.raw_logs_committed
    {
        failures
            .push("Jupiter fixture must not commit raw transaction, instruction, or log data".to_string());
    }
    if !boundary.candidate_strength.ends_with("_unverified") {
        failures.push(format!(
            "Jupiter candidate_strength `{}` must stay explicitly unverified",
            boundary.candidate_strength
        ));
    }
    if boundary.shared_jupiter_owned_non_executable_account_observed
        && boundary.shared_account_count == 0
    {
        failures.push(
            "Jupiter shared-account evidence must include shared_account_count > 0".to_string(),
        );
    }
    for evidence_ref in &boundary.public_evidence_refs {
        if evidence_ref.is_empty()
            || evidence_ref.starts_with('/')
            || evidence_ref.contains("..")
            || evidence_ref.starts_with("http://")
            || evidence_ref.starts_with("https://")
        {
            failures.push(format!(
                "Jupiter public evidence ref `{evidence_ref}` must be repo-relative"
            ));
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
        RiskReasonCode::AccountStateMismatch => "AccountStateMismatch",
        RiskReasonCode::InvalidAccountSet => "InvalidAccountSet",
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
        RiskReasonCode::ComputeBudgetExceeded => "ComputeBudgetExceeded",
        RiskReasonCode::BlockhashExpired => "BlockhashExpired",
        RiskReasonCode::AccountLockContention => "AccountLockContention",
        RiskReasonCode::PriorityFeeUnderbid => "PriorityFeeUnderbid",
        RiskReasonCode::TransactionDroppedUnknown => "TransactionDroppedUnknown",
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
    const GUARDRAIL_UNKNOWN_MANIFEST: &str = include_str!(
        "../../../datasets/sample/drift_synthetic_guardrail_unknown_pause_bit_001/manifest.json"
    );
    const GUARDRAIL_UNKNOWN_DRY_RUN: &str = include_str!(
        "../../../datasets/sample/drift_synthetic_guardrail_unknown_pause_bit_001/dry_run_output.json"
    );
    const PERP_PAUSE_MANIFEST: &str =
        include_str!("../../../datasets/sample/drift_synthetic_perp_pause_flag_001/manifest.json");
    const PERP_PAUSE_DRY_RUN: &str = include_str!(
        "../../../datasets/sample/drift_synthetic_perp_pause_flag_001/dry_run_output.json"
    );
    const JUPITER_LIFECYCLE_MANIFEST: &str = include_str!(
        "../../../datasets/sample/jupiter_synthetic_lifecycle_candidate_unverified_001/manifest.json"
    );
    const JUPITER_LIFECYCLE_DRY_RUN: &str = include_str!(
        "../../../datasets/sample/jupiter_synthetic_lifecycle_candidate_unverified_001/dry_run_output.json"
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
                "drift_synthetic_guardrail_unknown_pause_bit_001",
                "drift_synthetic_perp_pause_flag_001",
                "jupiter_synthetic_lifecycle_candidate_unverified_001",
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
    fn validates_unknown_guardrail_pause_bit_fixture_guardrails() {
        validate_fixture_case(FixtureValidationCase {
            fixture_set_id: "drift_synthetic_guardrail_unknown_pause_bit_001",
            manifest_json: GUARDRAIL_UNKNOWN_MANIFEST,
            dry_run_output_json: GUARDRAIL_UNKNOWN_DRY_RUN,
            content_files: guardrail_unknown_content_files(),
            expected_status: DryRunStatus::Rejected,
            expected_reason_codes: &[
                RiskReasonCode::DataQualityLow,
                RiskReasonCode::ExecutionDisabledDryRun,
            ],
        })
        .assert_passed();
    }

    #[test]
    fn validates_perp_pause_flag_fixture_guardrails() {
        validate_fixture_case(FixtureValidationCase {
            fixture_set_id: "drift_synthetic_perp_pause_flag_001",
            manifest_json: PERP_PAUSE_MANIFEST,
            dry_run_output_json: PERP_PAUSE_DRY_RUN,
            content_files: perp_pause_content_files(),
            expected_status: DryRunStatus::Rejected,
            expected_reason_codes: &[
                RiskReasonCode::DataQualityLow,
                RiskReasonCode::ExecutionDisabledDryRun,
            ],
        })
        .assert_passed();
    }

    #[test]
    fn validates_jupiter_lifecycle_candidate_fixture_guardrails() {
        validate_fixture_case(FixtureValidationCase {
            fixture_set_id: "jupiter_synthetic_lifecycle_candidate_unverified_001",
            manifest_json: JUPITER_LIFECYCLE_MANIFEST,
            dry_run_output_json: JUPITER_LIFECYCLE_DRY_RUN,
            content_files: jupiter_lifecycle_content_files(),
            expected_status: DryRunStatus::Rejected,
            expected_reason_codes: &[
                RiskReasonCode::AdapterDecodeFailed,
                RiskReasonCode::DataQualityLow,
                RiskReasonCode::ExecutionDisabledDryRun,
            ],
        })
        .assert_passed();
    }

    #[test]
    fn rejects_jupiter_lifecycle_overclaims() {
        let overclaim = JUPITER_LIFECYCLE_DRY_RUN
            .replace(
                r#""canonical_decode_authorized": false"#,
                r#""canonical_decode_authorized": true"#,
            )
            .replace(
                r#""verified_request_fulfillment_pair_claimed": false"#,
                r#""verified_request_fulfillment_pair_claimed": true"#,
            );

        let report = validate_fixture_case(FixtureValidationCase {
            fixture_set_id: "jupiter_synthetic_lifecycle_candidate_unverified_001",
            manifest_json: JUPITER_LIFECYCLE_MANIFEST,
            dry_run_output_json: &overclaim,
            content_files: jupiter_lifecycle_content_files(),
            expected_status: DryRunStatus::Rejected,
            expected_reason_codes: &[
                RiskReasonCode::AdapterDecodeFailed,
                RiskReasonCode::DataQualityLow,
                RiskReasonCode::ExecutionDisabledDryRun,
            ],
        });

        assert!(!report.passed);
        for expected in [
            "canonical_decode_authorized=false",
            "verified_request_fulfillment_pair_claimed=false",
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
                  "schema_version": "0.1.0",
                  "mode": "Fixture",
                  "started_at_unix": 1780447600,
                  "completed_at_unix": 1780447601,
                  "opportunities_scanned": 1,
                  "opportunities_accepted": 0,
                  "opportunities_rejected": 1,
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
                "gate_results": [{
                  "gate_id": "invalid_scrub_guardrail",
                  "status": "Pass",
                  "reason_codes": ["ExecutionDisabledDryRun"]
                }],
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
            (RiskReasonCode::AccountStateMismatch, DryRunStatus::Rejected),
            (RiskReasonCode::InvalidAccountSet, DryRunStatus::Rejected),
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
            (
                RiskReasonCode::ComputeBudgetExceeded,
                DryRunStatus::SimulationFailed,
            ),
            (
                RiskReasonCode::BlockhashExpired,
                DryRunStatus::SimulationFailed,
            ),
            (
                RiskReasonCode::AccountLockContention,
                DryRunStatus::SimulationFailed,
            ),
            (
                RiskReasonCode::PriorityFeeUnderbid,
                DryRunStatus::SimulationFailed,
            ),
            (
                RiskReasonCode::TransactionDroppedUnknown,
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

    #[test]
    fn rejects_dry_run_summary_and_gate_invariant_failures() {
        let report = validate_fixture_case(FixtureValidationCase {
            fixture_set_id: "drift_synthetic_margin_001",
            manifest_json: MARGIN_MANIFEST,
            dry_run_output_json: r#"{
                "summary": {
                  "run_id": "drift_synthetic_margin_001",
                  "schema_version": "0.1.0",
                  "mode": "Fixture",
                  "started_at_unix": 1780447600,
                  "completed_at_unix": 1780447601,
                  "opportunities_scanned": 1,
                  "opportunities_accepted": 0,
                  "opportunities_rejected": 1,
                  "reason_codes": ["ExecutionDisabledDryRun"]
                },
                "opportunities": [{
                  "id": "bad_invariant_case",
                  "tx_plan": {"requires_signer": false, "submission_disabled": true},
                  "decision": {
                    "status": "Rejected",
                    "reason_codes": ["StaleOracle", "ExecutionDisabledDryRun"]
                  }
                }],
                "gate_results": [
                  {
                    "gate_id": "oracle_freshness",
                    "status": "Pass",
                    "reason_codes": ["StaleOracle"]
                  },
                  {
                    "gate_id": "oracle_freshness",
                    "status": "Pass",
                    "reason_codes": ["ExecutionDisabledDryRun"]
                  }
                ],
                "simulation_results": []
            }"#,
            content_files: margin_content_files(),
            expected_status: DryRunStatus::Rejected,
            expected_reason_codes: &[
                RiskReasonCode::StaleOracle,
                RiskReasonCode::ExecutionDisabledDryRun,
            ],
        });

        assert!(!report.passed);
        for expected in [
            "must match observed reason-code union",
            "gate_id `oracle_freshness` must be unique",
            "rejected dry-run outputs must include at least one non-pass gate",
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

    fn dry_run_fixture_with_reason(reason_code: &str, status: DryRunStatus) -> String {
        let status_name = dry_run_status_name(status);
        format!(
            r#"{{
                "summary": {{
                  "run_id": "drift_synthetic_margin_001",
                  "schema_version": "0.1.0",
                  "mode": "Fixture",
                  "started_at_unix": 1780447600,
                  "completed_at_unix": 1780447601,
                  "opportunities_scanned": 1,
                  "opportunities_accepted": 0,
                  "opportunities_rejected": 1,
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
                  "gate_id": "expanded_reason_gate",
                  "status": "Fail",
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

    fn guardrail_unknown_content_files() -> &'static [FixtureContent<'static>] {
        &[FixtureContent {
            path: "datasets/sample/drift_synthetic_guardrail_unknown_pause_bit_001/dry_run_output.json",
            bytes: include_bytes!("../../../datasets/sample/drift_synthetic_guardrail_unknown_pause_bit_001/dry_run_output.json"),
        }]
    }

    fn perp_pause_content_files() -> &'static [FixtureContent<'static>] {
        &[FixtureContent {
            path: "datasets/sample/drift_synthetic_perp_pause_flag_001/dry_run_output.json",
            bytes: include_bytes!(
                "../../../datasets/sample/drift_synthetic_perp_pause_flag_001/dry_run_output.json"
            ),
        }]
    }

    fn jupiter_lifecycle_content_files() -> &'static [FixtureContent<'static>] {
        &[FixtureContent {
            path: "datasets/sample/jupiter_synthetic_lifecycle_candidate_unverified_001/dry_run_output.json",
            bytes: include_bytes!(
                "../../../datasets/sample/jupiter_synthetic_lifecycle_candidate_unverified_001/dry_run_output.json"
            ),
        }]
    }
}
