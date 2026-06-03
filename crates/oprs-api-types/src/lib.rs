//! Shared API-facing type re-exports.

pub use oprs_core::*;
pub use oprs_data::*;
pub use oprs_dry_run::*;
use serde_json::Value;

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

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ApiExampleValidationReport {
    pub example_id: String,
    pub passed: bool,
    pub failures: Vec<String>,
}

impl ApiExampleValidationReport {
    pub fn assert_passed(&self) {
        assert!(
            self.passed,
            "API example {} failed validation: {:?}",
            self.example_id, self.failures
        );
    }
}

pub fn validate_api_example(example_id: &str, response_json: &str) -> ApiExampleValidationReport {
    let mut failures = Vec::new();

    let response = match serde_json::from_str::<Value>(response_json) {
        Ok(response) => Some(response),
        Err(error) => {
            failures.push(format!("API example JSON failed to parse: {error}"));
            None
        }
    };

    if let Some(response) = response {
        if response.get("schema_version").and_then(Value::as_str) != Some("0.1.0") {
            failures.push("schema_version must be `0.1.0`".to_string());
        }
        if response.get("data").is_none() || response.get("data") == Some(&Value::Null) {
            failures.push("data must be present and non-null".to_string());
        }

        validate_meta(example_id, &response, &mut failures);
        validate_no_blocked_execution_surface("$", &response, &mut failures);

        match example_id {
            "protocols_response" => validate_protocols_response(&response, &mut failures),
            "dry_run_response" => validate_dry_run_response(&response, &mut failures),
            "liquidation_health_response" => {
                validate_reason_code_response(&response, &mut failures)
            }
            _ => {}
        }
    }

    ApiExampleValidationReport {
        example_id: example_id.to_string(),
        passed: failures.is_empty(),
        failures,
    }
}

fn validate_meta(example_id: &str, response: &Value, failures: &mut Vec<String>) {
    let Some(meta) = response.get("meta") else {
        failures.push("meta must be present".to_string());
        return;
    };

    let dataset_name = meta.get("dataset_name").and_then(Value::as_str);
    if dataset_name.is_none_or(str::is_empty) {
        failures.push("meta.dataset_name must be present".to_string());
    }

    let manifest_ref = meta.get("manifest_ref").and_then(Value::as_str);
    match manifest_ref {
        Some(path) if path.starts_with("datasets/sample/") => {}
        Some(path) => failures.push(format!(
            "meta.manifest_ref `{path}` must be a datasets/sample relative path"
        )),
        None => failures.push("meta.manifest_ref must be present".to_string()),
    }

    if meta
        .get("generated_at_unix")
        .and_then(Value::as_i64)
        .is_none()
    {
        failures.push("meta.generated_at_unix must be present".to_string());
    }

    if !is_non_empty_string_array(meta.get("known_gaps")) {
        failures.push("meta.known_gaps must disclose at least one limitation".to_string());
    }

    if example_id != "protocols_response"
        && meta
            .get("adapter_version")
            .and_then(Value::as_str)
            .is_none()
    {
        failures
            .push("meta.adapter_version must be present for adapter-backed responses".to_string());
    }
}

fn validate_protocols_response(response: &Value, failures: &mut Vec<String>) {
    let Some(protocols) = response.get("data").and_then(Value::as_array) else {
        failures.push("protocols_response data must be an array".to_string());
        return;
    };

    if protocols.is_empty() {
        failures.push("protocols_response must include at least one protocol".to_string());
    }

    for protocol in protocols {
        let capabilities = protocol.get("capabilities");
        if !string_array_contains(capabilities, "ReadOnly") {
            failures.push("protocol capabilities must include ReadOnly".to_string());
        }
        if !string_array_contains(capabilities, "ExecuteDisabled") {
            failures.push("protocol capabilities must include ExecuteDisabled".to_string());
        }
    }
}

fn validate_dry_run_response(response: &Value, failures: &mut Vec<String>) {
    let Some(data) = response.get("data") else {
        return;
    };

    if data.get("mode").and_then(Value::as_str) != Some("Fixture") {
        failures.push("dry_run_response data.mode must be Fixture".to_string());
    }
    if !string_array_contains(data.get("reason_codes"), "ExecutionDisabledDryRun") {
        failures
            .push("dry_run_response reason_codes must include ExecutionDisabledDryRun".to_string());
    }
    if data
        .get("opportunities_accepted")
        .and_then(Value::as_u64)
        .unwrap_or_default()
        != 0
    {
        failures.push("dry_run_response must not accept synthetic opportunities".to_string());
    }
}

fn validate_reason_code_response(response: &Value, failures: &mut Vec<String>) {
    let Some(data) = response.get("data") else {
        return;
    };

    if !string_array_contains(data.get("reason_codes"), "ExecutionDisabledDryRun") {
        failures.push("reason_codes must include ExecutionDisabledDryRun".to_string());
    }
}

fn validate_no_blocked_execution_surface(path: &str, value: &Value, failures: &mut Vec<String>) {
    match value {
        Value::Object(object) => {
            for (key, nested) in object {
                let next_path = format!("{path}.{key}");
                if is_blocked_execution_key(key) {
                    failures.push(format!(
                        "blocked execution/signer field `{key}` appears at `{next_path}`"
                    ));
                }
                validate_no_blocked_execution_surface(&next_path, nested, failures);
            }
        }
        Value::Array(values) => {
            for (index, nested) in values.iter().enumerate() {
                validate_no_blocked_execution_surface(
                    &format!("{path}[{index}]"),
                    nested,
                    failures,
                );
            }
        }
        Value::String(text) => {
            if text.starts_with('/') || text.starts_with("http://") || text.starts_with("https://")
            {
                failures.push(format!(
                    "public API example contains non-relative or remote value `{text}` at `{path}`"
                ));
            }
        }
        _ => {}
    }
}

fn is_blocked_execution_key(key: &str) -> bool {
    matches!(
        key,
        "signer"
            | "signer_id"
            | "private_key"
            | "keypair"
            | "wallet_json"
            | "submit_url"
            | "send_transaction"
            | "submission_endpoint"
            | "capital_limit"
            | "execution_policy"
    )
}

fn is_non_empty_string_array(value: Option<&Value>) -> bool {
    value
        .and_then(Value::as_array)
        .is_some_and(|values| !values.is_empty() && values.iter().all(Value::is_string))
}

fn string_array_contains(value: Option<&Value>, needle: &str) -> bool {
    value
        .and_then(Value::as_array)
        .is_some_and(|values| values.iter().any(|value| value.as_str() == Some(needle)))
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

    #[test]
    fn validates_checked_in_api_examples() {
        const EXAMPLES: &[(&str, &str)] = &[
            (
                "adapter_health_response",
                include_str!("../../../examples/api/adapter_health_response.json"),
            ),
            (
                "dry_run_response",
                include_str!("../../../examples/api/dry_run_response.json"),
            ),
            (
                "liquidation_health_response",
                include_str!("../../../examples/api/liquidation_health_response.json"),
            ),
            (
                "market_quality_response",
                include_str!("../../../examples/api/market_quality_response.json"),
            ),
            (
                "oracle_risk_response",
                include_str!("../../../examples/api/oracle_risk_response.json"),
            ),
            (
                "protocols_response",
                include_str!("../../../examples/api/protocols_response.json"),
            ),
        ];

        for (example_id, response_json) in EXAMPLES {
            validate_api_example(example_id, response_json).assert_passed();
        }
    }

    #[test]
    fn rejects_signer_shaped_api_examples() {
        let report = validate_api_example(
            "dry_run_response",
            r#"{
                "schema_version": "0.1.0",
                "data": {
                    "mode": "Fixture",
                    "reason_codes": ["ExecutionDisabledDryRun"],
                    "signer": "fixture_signer"
                },
                "meta": {
                    "adapter_version": "0.1.0",
                    "dataset_name": "fixture_catalog",
                    "manifest_ref": "datasets/sample/fixture_catalog.json",
                    "generated_at_unix": 1780535300,
                    "known_gaps": ["test"]
                }
            }"#,
        );

        assert!(!report.passed);
        assert!(report
            .failures
            .iter()
            .any(|failure| failure.contains("blocked execution/signer field `signer`")));
    }
}
