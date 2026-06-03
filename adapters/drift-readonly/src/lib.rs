//! Fixture-backed Drift read-only adapter spike.
//!
//! This adapter is a shape test for the first real perps adapter. It exposes
//! metadata and deterministic fixture data only. It does not fetch live state,
//! sign, submit, custody funds, or model capital deployment.

use oprs_adapter::{AdapterResult, VenueAdapter};
use oprs_core::{
    AdapterCapability, AdapterMetadata, DataQuality, LiquidationState, LiquidationStateInput,
    MarginState, MarketSnapshot, MarketType, OracleFeedRef, OracleSnapshot, OracleSource,
    PositionQuery, PositionSide, PositionSnapshot, RiskReasonCode, VenueKind,
};

pub const DRIFT_PROTOCOL: &str = "drift";
pub const DRIFT_V2_PROGRAM_ID: &str = "dRiftyHA39MWEi3m9aunc5MzRF1JYuBsbn6VPcn33UH";

#[derive(Debug, Clone, Default)]
pub struct DriftReadOnlyAdapter;

impl DriftReadOnlyAdapter {
    pub fn new() -> Self {
        Self
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use oprs_adapter::requires_execute_disabled;

    fn oracle() -> OracleSnapshot {
        OracleSnapshot {
            feed_id: "SOL-PERP:pyth".to_string(),
            price: 150_000_000,
            confidence: 150_000,
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

    #[test]
    fn metadata_marks_adapter_as_read_only_fixture_spike() {
        let metadata = DriftReadOnlyAdapter::new().metadata();

        assert_eq!(metadata.adapter_name, "drift-readonly");
        assert_eq!(metadata.protocol, DRIFT_PROTOCOL);
        assert_eq!(metadata.program_ids, vec![DRIFT_V2_PROGRAM_ID.to_string()]);
        assert_eq!(metadata.data_quality, DataQuality::Unknown);
        assert!(!metadata.caveats.is_empty());
    }

    #[test]
    fn capabilities_require_execute_disabled() {
        let capabilities = DriftReadOnlyAdapter::new().capabilities();

        assert!(capabilities.contains(&AdapterCapability::ReadOnly));
        assert!(capabilities.contains(&AdapterCapability::Simulate));
        assert!(requires_execute_disabled(&capabilities));
    }

    #[test]
    fn fixture_liquidation_state_never_implies_execution() {
        let adapter = DriftReadOnlyAdapter::new();
        let position = adapter
            .positions(PositionQuery {
                market_id: Some("SOL-PERP".to_string()),
                owner: Some("fixture-owner".to_string()),
            })
            .expect("fixture position")
            .remove(0);

        let state = adapter
            .liquidation_state(LiquidationStateInput {
                position,
                oracle: oracle(),
            })
            .expect("fixture liquidation state");

        assert!(state.is_candidate);
        assert!(state
            .reason_codes
            .contains(&RiskReasonCode::ExecutionDisabledDryRun));
    }
}

impl VenueAdapter for DriftReadOnlyAdapter {
    fn metadata(&self) -> AdapterMetadata {
        AdapterMetadata {
            adapter_name: "drift-readonly".to_string(),
            adapter_version: env!("CARGO_PKG_VERSION").to_string(),
            protocol: DRIFT_PROTOCOL.to_string(),
            network: "solana-mainnet-beta".to_string(),
            venue_kind: VenueKind::Perps,
            program_ids: vec![DRIFT_V2_PROGRAM_ID.to_string()],
            account_schema_version: "drift-v2-idl-pending-fixture-decode".to_string(),
            supported_account_schema_versions: vec![
                "drift-v2-idl-pending-fixture-decode".to_string()
            ],
            idl_hash: None,
            source_updated_at_unix: None,
            docs_url: Some("https://drift-labs-protocol-v2.mintlify.app/".to_string()),
            data_quality: DataQuality::Unknown,
            caveats: vec![
                "Fixture-backed spike only; no live RPC reads.".to_string(),
                "Perps liquidation replay fixtures still need to be built.".to_string(),
                "Execution capability is intentionally disabled.".to_string(),
            ],
        }
    }

    fn capabilities(&self) -> Vec<AdapterCapability> {
        vec![
            AdapterCapability::ReadOnly,
            AdapterCapability::Simulate,
            AdapterCapability::ExecuteDisabled,
        ]
    }

    fn markets(&self) -> AdapterResult<Vec<MarketSnapshot>> {
        Ok(vec![MarketSnapshot {
            venue: DRIFT_PROTOCOL.to_string(),
            market_id: "SOL-PERP".to_string(),
            base_asset: "SOL".to_string(),
            quote_asset: "USD".to_string(),
            market_type: MarketType::Perp,
            observed_slot: 0,
        }])
    }

    fn oracle_feeds(&self, market_id: &str) -> AdapterResult<Vec<OracleFeedRef>> {
        Ok(vec![OracleFeedRef {
            feed_id: format!("{market_id}:pyth"),
            source: OracleSource::Pyth,
        }])
    }

    fn positions(&self, query: PositionQuery) -> AdapterResult<Vec<PositionSnapshot>> {
        let market_id = query.market_id.unwrap_or_else(|| "SOL-PERP".to_string());
        Ok(vec![PositionSnapshot {
            venue: DRIFT_PROTOCOL.to_string(),
            market_id,
            position_id: "fixture-position-001".to_string(),
            owner: query.owner,
            side: PositionSide::Long,
            base_amount: Some(10_000_000_000),
            quote_notional_usd: Some(1_500_000_000),
            collateral_usd: Some(75_000_000),
            observed_slot: 0,
        }])
    }

    fn margin_state(
        &self,
        position: &PositionSnapshot,
        _oracle: &OracleSnapshot,
    ) -> AdapterResult<MarginState> {
        let collateral_usd = position.collateral_usd.unwrap_or_default();
        let maintenance_margin_usd = 100_000_000;
        Ok(MarginState {
            maintenance_margin_usd,
            collateral_usd,
            initial_margin_usd: Some(150_000_000),
            unrealized_pnl_usd: None,
            health_ratio_bps: Some(if maintenance_margin_usd == 0 {
                0
            } else {
                (collateral_usd * 10_000 / maintenance_margin_usd) as i64
            }),
            liquidation_price: None,
            is_liquidatable: collateral_usd < maintenance_margin_usd,
        })
    }

    fn liquidation_state(&self, input: LiquidationStateInput) -> AdapterResult<LiquidationState> {
        let margin = self.margin_state(&input.position, &input.oracle)?;
        Ok(LiquidationState {
            is_candidate: margin.is_liquidatable,
            margin,
            reason_codes: if input.position.collateral_usd.unwrap_or_default() < 100_000_000 {
                vec![
                    RiskReasonCode::Eligible,
                    RiskReasonCode::ExecutionDisabledDryRun,
                ]
            } else {
                vec![RiskReasonCode::NotLiquidatable]
            },
        })
    }
}
