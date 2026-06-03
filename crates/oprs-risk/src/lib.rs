//! Pyth-aware risk policy primitives.

use oprs_core::{OracleSnapshot, RiskReasonCode};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OraclePolicy {
    pub max_staleness_secs: i64,
    pub max_confidence_bps: i64,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OracleRiskResult {
    pub accepted: bool,
    pub reason_codes: Vec<RiskReasonCode>,
}

pub fn validate_oracle(
    snapshot: &OracleSnapshot,
    policy: &OraclePolicy,
    now_unix: i64,
) -> OracleRiskResult {
    let mut reason_codes = Vec::new();
    let staleness = now_unix.saturating_sub(snapshot.publish_time_unix);
    if staleness > policy.max_staleness_secs {
        reason_codes.push(RiskReasonCode::StaleOracle);
    }

    if snapshot.price != 0 {
        let confidence_bps = snapshot.confidence.saturating_mul(10_000) / snapshot.price.abs();
        if confidence_bps > policy.max_confidence_bps as i128 {
            reason_codes.push(RiskReasonCode::WideOracleConfidence);
        }
    }

    OracleRiskResult {
        accepted: reason_codes.is_empty(),
        reason_codes,
    }
}
