//! Canonical data envelope and public dataset metadata.

use oprs_core::Slot;
use serde::Deserialize;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DecodeStatus {
    Ok,
    Partial,
    Failed,
    Inferred,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DataQualitySeverity {
    BlockPublish,
    WarnPublic,
    InternalOnly,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PublishGateStatus {
    Pass,
    Warn,
    Block,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DataQualityCheck {
    pub check_id: String,
    pub gate_id: String,
    pub gate_version: String,
    pub dataset_name: String,
    pub partition: Option<String>,
    pub check_name: String,
    pub severity: DataQualitySeverity,
    pub status: PublishGateStatus,
    pub metric_value: Option<String>,
    pub threshold: Option<String>,
    pub failed_rows_ref: Option<String>,
    pub message: String,
    pub details_json: Option<String>,
    pub evaluated_at_unix: i64,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PublishGateReport {
    pub dataset_id: String,
    pub status: PublishGateStatus,
    pub checks: Vec<DataQualityCheck>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CanonicalEvent {
    pub event_id: String,
    pub schema_version: String,
    pub adapter_name: String,
    pub adapter_version: String,
    pub chain_id: String,
    pub protocol: String,
    pub program_id: String,
    pub market_id: String,
    pub event_type: String,
    pub event_subtype: Option<String>,
    pub slot: Slot,
    pub block_time_unix: i64,
    pub signature: String,
    pub instruction_index: Option<u16>,
    pub inner_index: Option<u16>,
    pub actor: Option<String>,
    pub subject_account: Option<String>,
    pub source_account_keys: Vec<String>,
    pub raw_ref: String,
    pub raw_hash: String,
    pub decode_status: DecodeStatus,
    pub quality_flags: Vec<String>,
    pub attrs_json: String,
    pub created_at_unix: i64,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CanonicalEventEnvelope {
    pub event: CanonicalEvent,
    pub lineage: LineageRef,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LineageRef {
    pub source: String,
    pub raw_ref: String,
    pub raw_hash: String,
    pub adapter_version: String,
    pub schema_version: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DatasetManifest {
    pub manifest_version: String,
    pub dataset_name: String,
    pub schema_version: String,
    pub protocol: String,
    pub chain_id: String,
    pub adapter_version: String,
    pub event_types: Vec<String>,
    pub source_window: String,
    pub source_start_slot: Option<Slot>,
    pub source_end_slot: Option<Slot>,
    pub partition_paths: Vec<String>,
    pub row_count: u64,
    pub distinct_event_count: u64,
    pub raw_refs_count: u64,
    pub raw_hash_algorithm: String,
    pub checksum: String,
    pub content_checksums: Vec<String>,
    pub dq_status: PublishGateStatus,
    pub dq_results_ref: Option<String>,
    pub quality_score_bps: u16,
    pub known_gaps: Vec<String>,
    pub source_limitations: Vec<String>,
    pub scrub_policy_version: String,
    pub generated_at_unix: i64,
    pub generated_by: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Deserialize)]
pub struct DataReconstructionEnvelope {
    pub schema_version: String,
    pub envelope_id: String,
    pub dataset_name: String,
    pub chain_id: String,
    pub protocol: String,
    pub reconstruction_type: ReconstructionType,
    pub sources: Vec<ReconstructionSource>,
    pub slot_range: ReconstructionSlotRange,
    pub query_config: ReconstructionQueryConfig,
    pub evidence_refs: Vec<String>,
    pub known_gaps: Vec<String>,
    pub source_limitations: Vec<String>,
    pub generated_at_unix: i64,
    pub generated_by: String,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ReconstructionType {
    SyntheticFixture,
    HistoricalRpc,
    StreamReplay,
    Mixed,
}

#[derive(Debug, Clone, PartialEq, Eq, Deserialize)]
pub struct ReconstructionSource {
    pub source_id: String,
    pub source_kind: ReconstructionSourceKind,
    pub provider_label: String,
    pub commitment: ReconstructionCommitment,
    pub lifecycle_stage: String,
    pub retention_boundary: Option<String>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ReconstructionSourceKind {
    SyntheticFixture,
    SolanaRpc,
    GeyserStream,
    ArchiveProvider,
    ProtocolDocs,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ReconstructionCommitment {
    Synthetic,
    Processed,
    Confirmed,
    Finalized,
    Unknown,
}

#[derive(Debug, Clone, PartialEq, Eq, Deserialize)]
pub struct ReconstructionSlotRange {
    pub start_slot: Option<Slot>,
    pub end_slot: Option<Slot>,
    pub coverage: ReconstructionCoverage,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ReconstructionCoverage {
    SyntheticOnly,
    Complete,
    Partial,
    Unknown,
}

#[derive(Debug, Clone, PartialEq, Eq, Deserialize)]
pub struct ReconstructionQueryConfig {
    pub methods: Vec<String>,
    pub transaction_details: Option<String>,
    pub max_supported_transaction_version: Option<i16>,
    pub address_filter_count: Option<u16>,
    pub stream_gap_count: u64,
    pub unsupported_version_count: u64,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DataReconstructionValidationReport {
    pub envelope_id: String,
    pub passed: bool,
    pub failures: Vec<String>,
}

impl DataReconstructionValidationReport {
    pub fn assert_passed(&self) {
        assert!(
            self.passed,
            "data reconstruction envelope {} failed validation: {:?}",
            self.envelope_id, self.failures
        );
    }
}

pub fn validate_data_reconstruction_envelope_json(
    envelope_json: &str,
) -> DataReconstructionValidationReport {
    let mut failures = Vec::new();

    let scrub_violations =
        validate_public_dataset_scrub_text("data_reconstruction_envelope.json", envelope_json);
    for violation in scrub_violations {
        failures.push(format!(
            "scrub violation at `{}`: {}",
            violation.path,
            violation.kind.label()
        ));
    }

    let envelope = match serde_json::from_str::<DataReconstructionEnvelope>(envelope_json) {
        Ok(envelope) => Some(envelope),
        Err(error) => {
            failures.push(format!("envelope JSON failed to parse: {error}"));
            None
        }
    };

    let envelope_id = envelope
        .as_ref()
        .map(|envelope| envelope.envelope_id.clone())
        .unwrap_or_else(|| "unknown".to_string());

    if let Some(envelope) = envelope {
        if envelope.schema_version != "0.1.0" {
            failures.push(format!(
                "schema_version `{}` must be `0.1.0`",
                envelope.schema_version
            ));
        }
        if envelope.sources.is_empty() {
            failures.push("sources must include at least one source".to_string());
        }
        if envelope.evidence_refs.is_empty() {
            failures.push("evidence_refs must include at least one relative reference".to_string());
        }
        if envelope.known_gaps.is_empty() {
            failures.push("known_gaps must disclose at least one limitation".to_string());
        }
        if envelope.source_limitations.is_empty() {
            failures.push("source_limitations must disclose at least one limitation".to_string());
        }
        if let (Some(start), Some(end)) =
            (envelope.slot_range.start_slot, envelope.slot_range.end_slot)
        {
            if start > end {
                failures.push(format!(
                    "slot_range start_slot `{start}` must be <= end_slot `{end}`"
                ));
            }
        }
        if envelope.query_config.methods.is_empty() {
            failures.push("query_config.methods must include at least one method".to_string());
        }
        if envelope.generated_at_unix <= 0 {
            failures.push("generated_at_unix must be positive".to_string());
        }

        for source in &envelope.sources {
            if source.source_id.trim().is_empty() {
                failures.push("source_id must not be empty".to_string());
            }
            if source.provider_label.starts_with("http://")
                || source.provider_label.starts_with("https://")
            {
                failures.push(format!(
                    "provider_label `{}` must not expose a URL",
                    source.provider_label
                ));
            }
        }

        for evidence_ref in &envelope.evidence_refs {
            if evidence_ref.starts_with('/')
                || evidence_ref.starts_with("http://")
                || evidence_ref.starts_with("https://")
            {
                failures.push(format!(
                    "evidence_ref `{evidence_ref}` must be a relative public artifact path"
                ));
            }
        }
    }

    DataReconstructionValidationReport {
        envelope_id,
        passed: failures.is_empty(),
        failures,
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ScrubPolicy {
    pub version: String,
    pub policy_name: String,
    pub applies_to: Vec<String>,
    pub redact_rpc_urls: bool,
    pub redact_api_keys: bool,
    pub redact_local_paths: bool,
    pub redact_private_route_labels: bool,
    pub redact_strategy_fields: bool,
    pub field_rules_json: String,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ScrubViolationKind {
    RpcUrlWithApiKey,
    BearerToken,
    LocalAbsolutePath,
    EnvReference,
    PrivateKeyMaterial,
    SignerOrWalletMetadata,
    CapitalOrExecutionPolicy,
}

impl ScrubViolationKind {
    pub fn label(self) -> &'static str {
        match self {
            ScrubViolationKind::RpcUrlWithApiKey => "rpc_url_with_api_key",
            ScrubViolationKind::BearerToken => "bearer_token",
            ScrubViolationKind::LocalAbsolutePath => "local_absolute_path",
            ScrubViolationKind::EnvReference => "env_reference",
            ScrubViolationKind::PrivateKeyMaterial => "private_key_material",
            ScrubViolationKind::SignerOrWalletMetadata => "signer_or_wallet_metadata",
            ScrubViolationKind::CapitalOrExecutionPolicy => "capital_or_execution_policy",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ScrubViolation {
    pub path: String,
    pub kind: ScrubViolationKind,
    pub evidence: String,
}

impl ScrubViolation {
    fn new(path: &str, kind: ScrubViolationKind, evidence: &str) -> Self {
        Self {
            path: path.to_string(),
            kind,
            evidence: evidence.to_string(),
        }
    }
}

pub fn validate_public_dataset_scrub_text(path: &str, text: &str) -> Vec<ScrubViolation> {
    let mut violations = Vec::new();
    let lower = text.to_ascii_lowercase();

    if contains_rpc_url_with_api_key(&lower) {
        violations.push(ScrubViolation::new(
            path,
            ScrubViolationKind::RpcUrlWithApiKey,
            "remote RPC URL appears to carry key/token material",
        ));
    }
    if lower.contains("bearer ") || lower.contains("authorization: bearer") {
        violations.push(ScrubViolation::new(
            path,
            ScrubViolationKind::BearerToken,
            "bearer authorization material is present",
        ));
    }
    if contains_local_absolute_path(text) {
        violations.push(ScrubViolation::new(
            path,
            ScrubViolationKind::LocalAbsolutePath,
            "local absolute filesystem path is present",
        ));
    }
    if lower.contains(".env") {
        violations.push(ScrubViolation::new(
            path,
            ScrubViolationKind::EnvReference,
            ".env reference is present",
        ));
    }
    if contains_any_json_key(
        &lower,
        &[
            "private_key",
            "seed_phrase",
            "mnemonic",
            "secret_key",
            "keypair",
        ],
    ) || lower.contains("begin private key")
    {
        violations.push(ScrubViolation::new(
            path,
            ScrubViolationKind::PrivateKeyMaterial,
            "private key, seed phrase, mnemonic, or keypair material is present",
        ));
    }
    if contains_any_json_key(
        &lower,
        &[
            "signer",
            "signer_id",
            "wallet_json",
            "wallet_inventory",
            "wallet_balances",
            "custody_wallet",
        ],
    ) {
        violations.push(ScrubViolation::new(
            path,
            ScrubViolationKind::SignerOrWalletMetadata,
            "signer, wallet inventory, or custody metadata field is present",
        ));
    }
    if contains_any_json_key(
        &lower,
        &[
            "capital_limit",
            "capital_limits",
            "execution_policy",
            "execution_limits",
        ],
    ) {
        violations.push(ScrubViolation::new(
            path,
            ScrubViolationKind::CapitalOrExecutionPolicy,
            "capital limit or execution policy field is present",
        ));
    }

    violations
}

pub fn event_id_preimage(event: &CanonicalEvent) -> String {
    format!(
        "{}|{}|{}|{}|{}|{}|{}|{}|{}",
        event.chain_id,
        event.protocol,
        event.program_id,
        event.signature,
        event.instruction_index.unwrap_or_default(),
        event.inner_index.unwrap_or_default(),
        event.event_type,
        event.event_subtype.as_deref().unwrap_or_default(),
        event.adapter_version
    )
}

fn contains_rpc_url_with_api_key(lower: &str) -> bool {
    let has_remote_url = lower.contains("http://") || lower.contains("https://");
    if !has_remote_url {
        return false;
    }

    lower.contains("api_key=")
        || lower.contains("api-key=")
        || lower.contains("apikey=")
        || lower.contains("x-api-key")
        || lower.contains("access_token=")
        || lower.contains("token=")
        || (lower.contains("rpc") && lower.contains("key="))
        || lower.contains("alchemy.com/v2/")
        || lower.contains("quiknode.pro/")
        || lower.contains("helius-rpc.com/?api-key")
}

fn contains_local_absolute_path(text: &str) -> bool {
    text.contains("/Users/")
        || text.contains("/home/")
        || text.contains("/private/")
        || text.contains("/var/folders/")
        || text.contains("C:\\")
        || text.contains("D:\\")
}

fn contains_any_json_key(lower: &str, keys: &[&str]) -> bool {
    keys.iter().any(|key| {
        lower.contains(&format!("\"{key}\""))
            || lower.contains(&format!("'{key}'"))
            || lower.contains(&format!("{key}:"))
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn accepts_public_fixture_language_without_secret_fields() {
        let violations = validate_public_dataset_scrub_text(
            "datasets/sample/example/manifest.json",
            r#"{
                "scrub_policy_version": "0.1.0",
                "known_gaps": [
                  "No private keys, signing, transaction submission, or capital deployment."
                ],
                "tx_plan": {
                  "requires_signer": false,
                  "submission_disabled": true
                }
            }"#,
        );

        assert!(violations.is_empty(), "{violations:?}");
    }

    #[test]
    fn rejects_secret_and_execution_leak_patterns() {
        let cases = [
            (
                ScrubViolationKind::RpcUrlWithApiKey,
                r#"{"rpc_url":"https://mainnet.helius-rpc.com/?api-key=abc123"}"#,
            ),
            (
                ScrubViolationKind::BearerToken,
                r#"{"authorization":"Bearer abc123"}"#,
            ),
            (
                ScrubViolationKind::LocalAbsolutePath,
                r#"{"raw_ref":"/Users/founder/private/snapshot.json"}"#,
            ),
            (
                ScrubViolationKind::EnvReference,
                r#"{"source":"load .env before running"}"#,
            ),
            (
                ScrubViolationKind::PrivateKeyMaterial,
                r#"{"private_key":"redacted-but-still-invalid"}"#,
            ),
            (
                ScrubViolationKind::SignerOrWalletMetadata,
                r#"{"wallet_inventory":{"USDC":"1000"}}"#,
            ),
            (
                ScrubViolationKind::CapitalOrExecutionPolicy,
                r#"{"execution_policy":{"max_slippage_bps":10}}"#,
            ),
        ];

        for (kind, text) in cases {
            let violations = validate_public_dataset_scrub_text("invalid_fixture.json", text);
            assert!(
                violations.iter().any(|violation| violation.kind == kind),
                "expected {kind:?} in {violations:?}"
            );
        }
    }

    #[test]
    fn validates_public_data_reconstruction_envelope() {
        let report = validate_data_reconstruction_envelope_json(include_str!(
            "../../../examples/datasets/data_reconstruction_envelope.json"
        ));

        report.assert_passed();
    }

    #[test]
    fn rejects_reconstruction_envelope_secret_or_remote_refs() {
        let report = validate_data_reconstruction_envelope_json(
            r#"{
              "schema_version": "0.1.0",
              "envelope_id": "invalid",
              "dataset_name": "bad",
              "chain_id": "solana-mainnet-beta",
              "protocol": "drift",
              "reconstruction_type": "historical_rpc",
              "sources": [{
                "source_id": "bad-rpc",
                "source_kind": "solana_rpc",
                "provider_label": "https://mainnet.helius-rpc.com/?api-key=abc",
                "commitment": "finalized",
                "lifecycle_stage": "historical_rpc",
                "retention_boundary": ".env"
              }],
              "slot_range": {
                "start_slot": 20,
                "end_slot": 10,
                "coverage": "partial"
              },
              "query_config": {
                "methods": ["getBlock"],
                "transaction_details": "full",
                "max_supported_transaction_version": 0,
                "address_filter_count": 1,
                "stream_gap_count": 0,
                "unsupported_version_count": 0
              },
              "evidence_refs": ["https://example.invalid/raw.json"],
              "known_gaps": ["bad"],
              "source_limitations": ["bad"],
              "generated_at_unix": 1780599000,
              "generated_by": "test"
            }"#,
        );

        assert!(!report.passed);
        assert!(
            report
                .failures
                .iter()
                .any(|failure| failure.contains("rpc_url_with_api_key")),
            "{:?}",
            report.failures
        );
        assert!(
            report
                .failures
                .iter()
                .any(|failure| failure.contains("start_slot")),
            "{:?}",
            report.failures
        );
        assert!(
            report
                .failures
                .iter()
                .any(|failure| failure.contains("evidence_ref")),
            "{:?}",
            report.failures
        );
    }
}
