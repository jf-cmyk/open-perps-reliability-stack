//! Canonical data envelope and public dataset metadata.

use oprs_core::Slot;

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
