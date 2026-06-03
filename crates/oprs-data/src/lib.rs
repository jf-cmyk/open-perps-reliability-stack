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

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CanonicalEvent {
    pub event_id: String,
    pub schema_version: String,
    pub adapter_version: String,
    pub chain_id: String,
    pub protocol: String,
    pub market_id: String,
    pub event_type: String,
    pub slot: Slot,
    pub block_time_unix: i64,
    pub signature: String,
    pub instruction_index: Option<u16>,
    pub inner_index: Option<u16>,
    pub actor: Option<String>,
    pub raw_ref: String,
    pub raw_hash: String,
    pub decode_status: DecodeStatus,
    pub quality_flags: Vec<String>,
    pub attrs_json: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DatasetManifest {
    pub schema_version: String,
    pub adapter_version: String,
    pub source_window: String,
    pub row_count: u64,
    pub checksum: String,
    pub quality_score_bps: u16,
    pub known_gaps: Vec<String>,
    pub scrub_policy_version: String,
}
