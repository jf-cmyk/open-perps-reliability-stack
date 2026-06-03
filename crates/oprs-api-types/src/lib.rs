//! Shared API-facing type re-exports.

pub use oprs_core::*;
pub use oprs_data::*;
pub use oprs_dry_run::*;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ApiEnvelope<T> {
    pub schema_version: String,
    pub data: T,
    pub meta: ApiMeta,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ApiMeta {
    pub adapter_version: Option<String>,
    pub dataset_name: Option<String>,
    pub manifest_ref: Option<String>,
    pub generated_at_unix: i64,
    pub known_gaps: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MarketQualityResponse {
    pub protocol: String,
    pub market_id: String,
    pub observed_slot: Slot,
    pub spread_bps: Option<i64>,
    pub depth_usd: Option<Decimal>,
    pub open_interest_usd: Option<Decimal>,
    pub funding_rate_bps: Option<i64>,
    pub quality_flags: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OracleRiskResponse {
    pub protocol: String,
    pub market_id: String,
    pub observed_slot: Slot,
    pub snapshots: Vec<OracleRiskSnapshot>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AdapterHealthResponse {
    pub adapter_name: String,
    pub adapter_version: String,
    pub protocol: String,
    pub decode_success_rate_bps: Option<u16>,
    pub missing_account_count: u64,
    pub schema_mismatch_count: u64,
    pub quality_flags: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LiquidationHealthResponse {
    pub protocol: String,
    pub market_id: String,
    pub candidate_count: u64,
    pub accepted_count: u64,
    pub rejected_count: u64,
    pub reason_codes: Vec<RiskReasonCode>,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn api_envelope_carries_dataset_lineage() {
        let response = ApiEnvelope {
            schema_version: "0.1.0".to_string(),
            data: AdapterHealthResponse {
                adapter_name: "drift-readonly".to_string(),
                adapter_version: "0.1.0".to_string(),
                protocol: "drift".to_string(),
                decode_success_rate_bps: Some(10_000),
                missing_account_count: 0,
                schema_mismatch_count: 0,
                quality_flags: Vec::new(),
            },
            meta: ApiMeta {
                adapter_version: Some("0.1.0".to_string()),
                dataset_name: Some("drift_synthetic_margin_001".to_string()),
                manifest_ref: Some(
                    "datasets/sample/drift_synthetic_margin_001/manifest.json".to_string(),
                ),
                generated_at_unix: 1_780_448_600,
                known_gaps: vec!["synthetic fixture only".to_string()],
            },
        };

        assert_eq!(response.schema_version, "0.1.0");
        assert_eq!(response.data.adapter_name, "drift-readonly");
        assert_eq!(
            response.meta.dataset_name.as_deref(),
            Some("drift_synthetic_margin_001")
        );
    }
}
