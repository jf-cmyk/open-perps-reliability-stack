//! Pyth-aware risk policy primitives.

use oprs_core::{Decimal, OracleRiskSnapshot, OracleSnapshot, OracleSource, RiskReasonCode};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OraclePolicy {
    pub policy_id: String,
    pub schema_version: String,
    pub max_staleness_secs: i64,
    pub max_confidence_bps: i64,
    pub max_oracle_mark_divergence_bps: Option<i64>,
    pub min_publisher_count: Option<u16>,
    pub allowed_sources: Vec<OracleSource>,
    pub fail_open: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OracleRiskResult {
    pub accepted: bool,
    pub confidence_bps: Option<i64>,
    pub reason_codes: Vec<RiskReasonCode>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OracleDivergencePolicy {
    pub max_divergence_bps: i64,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OracleDivergenceInput {
    pub oracle_price: Decimal,
    pub reference_price: Decimal,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OracleDivergenceResult {
    pub accepted: bool,
    pub divergence_bps: Option<i64>,
    pub reason_codes: Vec<RiskReasonCode>,
}

pub fn validate_oracle(
    snapshot: &OracleSnapshot,
    policy: &OraclePolicy,
    now_unix: i64,
) -> OracleRiskResult {
    let mut reason_codes = Vec::new();
    let mut confidence_bps = None;
    let staleness = now_unix.saturating_sub(snapshot.publish_time_unix);
    if staleness > policy.max_staleness_secs {
        reason_codes.push(RiskReasonCode::StaleOracle);
    }

    if !policy.allowed_sources.is_empty() && !policy.allowed_sources.contains(&snapshot.source) {
        reason_codes.push(RiskReasonCode::MissingOracle);
    }

    if snapshot.price != 0 {
        let computed = snapshot.confidence.saturating_mul(10_000) / snapshot.price.abs();
        confidence_bps = i64::try_from(computed).ok();
        if computed > policy.max_confidence_bps as i128 {
            reason_codes.push(RiskReasonCode::WideOracleConfidence);
        }
    } else {
        reason_codes.push(RiskReasonCode::MissingOracle);
    }

    OracleRiskResult {
        accepted: reason_codes.is_empty() || policy.fail_open,
        confidence_bps,
        reason_codes,
    }
}

pub fn validate_divergence(
    input: &OracleDivergenceInput,
    policy: &OracleDivergencePolicy,
) -> OracleDivergenceResult {
    if input.oracle_price == 0 || input.reference_price == 0 {
        return OracleDivergenceResult {
            accepted: false,
            divergence_bps: None,
            reason_codes: vec![RiskReasonCode::MissingOracle],
        };
    }

    let diff = (input.oracle_price - input.reference_price).abs();
    let base = input.oracle_price.abs().max(input.reference_price.abs());
    let computed = diff.saturating_mul(10_000) / base;
    let divergence_bps = i64::try_from(computed).ok();
    let rejected = computed > policy.max_divergence_bps as i128;

    OracleDivergenceResult {
        accepted: !rejected,
        divergence_bps,
        reason_codes: if rejected {
            vec![RiskReasonCode::OracleMarkDivergence]
        } else {
            Vec::new()
        },
    }
}

pub fn oracle_risk_snapshot(
    snapshot: &OracleSnapshot,
    policy: &OraclePolicy,
    now_unix: i64,
) -> OracleRiskSnapshot {
    let result = validate_oracle(snapshot, policy, now_unix);
    OracleRiskSnapshot {
        feed_id: snapshot.feed_id.clone(),
        stale: result
            .reason_codes
            .iter()
            .any(|code| matches!(code, RiskReasonCode::StaleOracle)),
        confidence_bps: result.confidence_bps,
        divergence_bps: None,
        reason_codes: result.reason_codes,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use oprs_core::OracleSource;

    fn snapshot(price: Decimal, confidence: Decimal) -> OracleSnapshot {
        OracleSnapshot {
            feed_id: "SOL-PERP:pyth".to_string(),
            price,
            confidence,
            exponent: -6,
            publish_time_unix: 100,
            received_at_unix: Some(101),
            slot: Some(1),
            source: OracleSource::Pyth,
            raw_ref: None,
            raw_hash: None,
            quality_flags: Vec::new(),
        }
    }

    fn policy(fail_open: bool) -> OraclePolicy {
        OraclePolicy {
            policy_id: "pyth-mainnet-v0".to_string(),
            schema_version: "0.1.0".to_string(),
            max_staleness_secs: 10,
            max_confidence_bps: 100,
            max_oracle_mark_divergence_bps: Some(250),
            min_publisher_count: None,
            allowed_sources: vec![OracleSource::Pyth],
            fail_open,
        }
    }

    #[test]
    fn stale_oracle_is_rejected_by_default() {
        let result = validate_oracle(&snapshot(100_000_000, 100_000), &policy(false), 200);

        assert!(!result.accepted);
        assert!(result.reason_codes.contains(&RiskReasonCode::StaleOracle));
    }

    #[test]
    fn fail_open_is_explicit_and_visible_in_reasons() {
        let result = validate_oracle(&snapshot(100_000_000, 100_000), &policy(true), 200);

        assert!(result.accepted);
        assert!(result.reason_codes.contains(&RiskReasonCode::StaleOracle));
    }

    #[test]
    fn wide_confidence_is_rejected() {
        let result = validate_oracle(&snapshot(100_000_000, 2_000_000), &policy(false), 101);

        assert!(!result.accepted);
        assert!(result
            .reason_codes
            .contains(&RiskReasonCode::WideOracleConfidence));
    }

    #[test]
    fn divergence_policy_rejects_large_mark_gap() {
        let result = validate_divergence(
            &OracleDivergenceInput {
                oracle_price: 100_000_000,
                reference_price: 110_000_000,
            },
            &OracleDivergencePolicy {
                max_divergence_bps: 250,
            },
        );

        assert!(!result.accepted);
        assert!(result
            .reason_codes
            .contains(&RiskReasonCode::OracleMarkDivergence));
    }
}
