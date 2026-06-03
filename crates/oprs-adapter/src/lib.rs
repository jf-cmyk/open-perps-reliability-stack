//! Adapter traits for read-only protocol integrations.

use oprs_core::{
    AdapterCapability, AdapterMetadata, MarginState, MarketSnapshot, OracleFeedRef,
    OracleSnapshot, PositionQuery, PositionSnapshot, RiskReasonCode,
};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AdapterError {
    pub reason: RiskReasonCode,
    pub message: String,
}

pub type AdapterResult<T> = Result<T, AdapterError>;

pub trait VenueAdapter {
    fn metadata(&self) -> AdapterMetadata;
    fn capabilities(&self) -> Vec<AdapterCapability>;
    fn markets(&self) -> AdapterResult<Vec<MarketSnapshot>>;
    fn oracle_feeds(&self, market_id: &str) -> AdapterResult<Vec<OracleFeedRef>>;
    fn positions(&self, query: PositionQuery) -> AdapterResult<Vec<PositionSnapshot>>;
    fn margin_state(
        &self,
        position: &PositionSnapshot,
        oracle: &OracleSnapshot,
    ) -> AdapterResult<MarginState>;
}

pub fn requires_execute_disabled(capabilities: &[AdapterCapability]) -> bool {
    capabilities
        .iter()
        .any(|capability| matches!(capability, AdapterCapability::ExecuteDisabled))
}
