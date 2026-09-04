#!/usr/bin/env bash
set -euo pipefail

base_url="${1:-${RAILWAY_PUBLIC_URL:-https://refreshing-art-production-86de.up.railway.app}}"
base_url="${base_url%/}"

workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

fetch() {
  local path="$1"
  local out="$2"
  curl --retry 1 --connect-timeout 10 --max-time 30 -fsSL "$base_url$path" -o "$out"
}

assert_contains() {
  local pattern="$1"
  shift
  if command -v rg >/dev/null 2>&1; then
    rg -q "$pattern" "$@"
  else
    grep -Eq "$pattern" "$@"
  fi
}

status_code() {
  local path="$1"
  curl --retry 1 --connect-timeout 10 --max-time 30 -sS -o /dev/null -w "%{http_code}" "$base_url$path"
}

header_value() {
  local path="$1"
  local header="$2"
  curl --retry 1 --connect-timeout 10 --max-time 30 -fsSI "$base_url$path" \
    | awk -F': *' -v header="$header" 'tolower($1) == tolower(header) {print tolower($2)}' \
    | tr -d '\r' \
    | tail -n 1
}

echo "== Hosted proof-pack smoke checks =="
echo "Target: $base_url"

echo "== Fetch proof pack =="
fetch "/" "$workdir/index.html"
assert_contains "Open Perps Reliability Stack Proof Pack" "$workdir/index.html"
assert_contains "Read-only" "$workdir/index.html"
assert_contains "Dry-run" "$workdir/index.html"
assert_contains "docs/drift-liquidation-scan-boundary.md" "$workdir/index.html"
assert_contains "docs/proof-pack-changelog.md" "$workdir/index.html"
assert_contains "docs/live-readiness-path.md" "$workdir/index.html"
assert_contains "docs/railway-readonly-worker-service-plan.md" "$workdir/index.html"
assert_contains "docs/access-ops-setup.md" "$workdir/index.html"
assert_contains "docs/slack-alerting.md" "$workdir/index.html"
assert_contains "docs/read-only-soak-runbook.md" "$workdir/index.html"
assert_contains "docs/commercial-diagnostics-brief.md" "$workdir/index.html"
assert_contains "docs/commercial-diagnostics-pricing.md" "$workdir/index.html"
assert_contains "docs/execution-pilot-scope.md" "$workdir/index.html"
assert_contains "docs/jupiter-verified-pairing-validator.md" "$workdir/index.html"
assert_contains "examples/datasets/readonly_soak_summary_example.json" "$workdir/index.html"
assert_contains "docs/phoenix-hawkeye-validator-plan.md" "$workdir/index.html"

echo "== Fetch dashboard =="
fetch "/apps/dashboard/" "$workdir/dashboard.html"
assert_contains "Open Perps" "$workdir/dashboard.html"
assert_contains "No live execution" "$workdir/dashboard.html"
assert_contains "Protocol Gates" "$workdir/dashboard.html"
assert_contains "ExecutionDisabledDryRun" "$workdir/dashboard.html"
assert_contains "AdapterVersionMismatch" "$workdir/dashboard.html"
assert_contains "../../docs/drift-liquidation-scan-boundary.md" "$workdir/dashboard.html"
assert_contains "../../docs/proof-pack-changelog.md" "$workdir/dashboard.html"
assert_contains "../../docs/live-readiness-path.md" "$workdir/dashboard.html"
assert_contains "../../docs/railway-readonly-worker-service-plan.md" "$workdir/dashboard.html"
assert_contains "../../docs/access-ops-setup.md" "$workdir/dashboard.html"
assert_contains "../../docs/slack-alerting.md" "$workdir/dashboard.html"
assert_contains "../../docs/read-only-soak-runbook.md" "$workdir/dashboard.html"
assert_contains "../../docs/commercial-diagnostics-brief.md" "$workdir/dashboard.html"
assert_contains "../../docs/commercial-diagnostics-pricing.md" "$workdir/dashboard.html"
assert_contains "../../docs/execution-pilot-scope.md" "$workdir/dashboard.html"
assert_contains "../../docs/jupiter-verified-pairing-validator.md" "$workdir/dashboard.html"
assert_contains "../../docs/phoenix-hawkeye-validator-plan.md" "$workdir/dashboard.html"

echo "== Fetch live readiness path =="
fetch "/docs/live-readiness-path.md" "$workdir/live-readiness-path.md"
assert_contains "Live Readiness Path" "$workdir/live-readiness-path.md"
assert_contains "Live Read-Only Service" "$workdir/live-readiness-path.md"
assert_contains "7 days" "$workdir/live-readiness-path.md"
assert_contains "Execution Readiness Candidate" "$workdir/live-readiness-path.md"

echo "== Fetch worker service plan =="
fetch "/docs/railway-readonly-worker-service-plan.md" "$workdir/railway-readonly-worker-service-plan.md"
assert_contains "Railway Read-Only Worker Service Plan" "$workdir/railway-readonly-worker-service-plan.md"
assert_contains "OPRS_WORKER_MODE" "$workdir/railway-readonly-worker-service-plan.md"
assert_contains "oprs-readonly-worker" "$workdir/railway-readonly-worker-service-plan.md"
assert_contains "It must never sign" "$workdir/railway-readonly-worker-service-plan.md"

echo "== Fetch access ops setup =="
fetch "/docs/access-ops-setup.md" "$workdir/access-ops-setup.md"
assert_contains "Access And Operations Setup" "$workdir/access-ops-setup.md"
assert_contains "oprs-readonly-worker" "$workdir/access-ops-setup.md"
assert_contains "OPRS_ALERT_WEBHOOK_URL" "$workdir/access-ops-setup.md"
assert_contains "railway domain YOUR_DOMAIN_HERE" "$workdir/access-ops-setup.md"

echo "== Fetch Slack alerting contract =="
fetch "/docs/slack-alerting.md" "$workdir/slack-alerting.md"
fetch "/examples/datasets/slack_alert_payload_example.json" "$workdir/slack_alert_payload_example.json"
fetch "/schemas/datasets/slack-alert-payload-v0.json" "$workdir/slack-alert-payload-v0.json"
assert_contains "Slack Alerting" "$workdir/slack-alerting.md"
assert_contains "OPRS_ALERT_WEBHOOK_URL" "$workdir/slack-alerting.md"
assert_contains "oprs.slack_alert_payload.v0" "$workdir/slack_alert_payload_example.json"
assert_contains "webhook_url_committed" "$workdir/slack_alert_payload_example.json"

echo "== Fetch read-only soak runbook =="
fetch "/docs/read-only-soak-runbook.md" "$workdir/read-only-soak-runbook.md"
assert_contains "Read-Only Soak Runbook" "$workdir/read-only-soak-runbook.md"
assert_contains "7 consecutive days" "$workdir/read-only-soak-runbook.md"
assert_contains "secret leakage" "$workdir/read-only-soak-runbook.md"
assert_contains "readonly-soak-summary-v0" "$workdir/read-only-soak-runbook.md"
assert_contains "Exit Decision" "$workdir/read-only-soak-runbook.md"

echo "== Fetch read-only soak summary example =="
fetch "/examples/datasets/readonly_soak_summary_example.json" "$workdir/readonly_soak_summary_example.json"
assert_contains "oprs.readonly_soak_summary.v0" "$workdir/readonly_soak_summary_example.json"
assert_contains "oprs-readonly-worker" "$workdir/readonly_soak_summary_example.json"
assert_contains '"execution_pilot_authorized": false' "$workdir/readonly_soak_summary_example.json"

echo "== Fetch worker run envelope example =="
fetch "/schemas/datasets/readonly-worker-run-envelope-v0.json" "$workdir/readonly-worker-run-envelope-v0.json"
fetch "/examples/datasets/readonly_worker_run_envelope_example.json" "$workdir/readonly_worker_run_envelope_example.json"
fetch "/schemas/datasets/readonly-worker-public-candidate-v0.json" "$workdir/readonly-worker-public-candidate-v0.json"
fetch "/examples/datasets/readonly_worker_public_candidate_example.json" "$workdir/readonly_worker_public_candidate_example.json"
fetch "/examples/public/readonly-worker-candidate-template-v0/README.md" "$workdir/readonly_worker_candidate_template_README.md"
fetch "/examples/public/readonly-worker-candidate-template-v0/manifest.template.json" "$workdir/readonly_worker_candidate_manifest_template.json"
fetch "/examples/public/readonly-worker-candidate-template-v0/dq.template.json" "$workdir/readonly_worker_candidate_dq_template.json"
assert_contains "oprs.readonly_worker_run_envelope.v0" "$workdir/readonly-worker-run-envelope-v0.json"
assert_contains "oprs.readonly_worker_run_envelope.v0" "$workdir/readonly_worker_run_envelope_example.json"
assert_contains "oprs.readonly_worker_public_candidate.v0" "$workdir/readonly-worker-public-candidate-v0.json"
assert_contains "blocked_pending_founder_review" "$workdir/readonly_worker_public_candidate_example.json"
assert_contains "public promotion template" "$workdir/readonly_worker_candidate_template_README.md"
assert_contains "oprs.readonly_worker_public_package_manifest_template.v0" "$workdir/readonly_worker_candidate_manifest_template.json"
assert_contains "founder_review_recorded" "$workdir/readonly_worker_candidate_dq_template.json"
assert_contains '"public_output_published": false' "$workdir/readonly_worker_run_envelope_example.json"
assert_contains '"private_payload_bodies_committed": false' "$workdir/readonly_worker_public_candidate_example.json"
assert_contains "target/oprs-worker-runs/" "$workdir/readonly_worker_run_envelope_example.json"

echo "== Fetch Jupiter pairing validator contract =="
fetch "/docs/jupiter-verified-pairing-validator.md" "$workdir/jupiter-verified-pairing-validator.md"
assert_contains "Jupiter Verified Pairing Validator Contract" "$workdir/jupiter-verified-pairing-validator.md"
assert_contains "candidate_pair" "$workdir/jupiter-verified-pairing-validator.md"
assert_contains "verified_pair" "$workdir/jupiter-verified-pairing-validator.md"
assert_contains "It should not fetch more data by default" "$workdir/jupiter-verified-pairing-validator.md"

echo "== Fetch commercial diagnostics brief =="
fetch "/docs/commercial-diagnostics-brief.md" "$workdir/commercial-diagnostics-brief.md"
assert_contains "Commercial Diagnostics Brief" "$workdir/commercial-diagnostics-brief.md"
assert_contains "Protocol proof-pack support" "$workdir/commercial-diagnostics-brief.md"
assert_contains "Read-Only Diagnostics API" "$workdir/commercial-diagnostics-brief.md"
assert_contains "not a trading" "$workdir/commercial-diagnostics-brief.md"

echo "== Fetch commercial diagnostics pricing =="
fetch "/docs/commercial-diagnostics-pricing.md" "$workdir/commercial-diagnostics-pricing.md"
assert_contains "Commercial Diagnostics Pricing" "$workdir/commercial-diagnostics-pricing.md"
assert_contains "Private Dashboard And Read-Only API Lane" "$workdir/commercial-diagnostics-pricing.md"
assert_contains "Public Proof-Pack And API Lane" "$workdir/commercial-diagnostics-pricing.md"
assert_contains "Protocol Reliability Pack" "$workdir/commercial-diagnostics-pricing.md"

echo "== Fetch execution pilot scope =="
fetch "/docs/execution-pilot-scope.md" "$workdir/execution-pilot-scope.md"
assert_contains "Execution Pilot Scope" "$workdir/execution-pilot-scope.md"
assert_contains "does not authorize execution" "$workdir/execution-pilot-scope.md"
assert_contains "selected wallet or signer" "$workdir/execution-pilot-scope.md"
assert_contains "Current status: execution pilot is future-scope only" "$workdir/execution-pilot-scope.md"

echo "== Fetch proof-pack changelog =="
fetch "/docs/proof-pack-changelog.md" "$workdir/proof-pack-changelog.md"
assert_contains "Proof-Pack Changelog" "$workdir/proof-pack-changelog.md"
assert_contains "318,000 finalized transactions" "$workdir/proof-pack-changelog.md"
assert_contains "JUPITER_API_KEY" "$workdir/proof-pack-changelog.md"
assert_contains "production execution readiness" "$workdir/proof-pack-changelog.md"

echo "== Fetch reconstruction envelope =="
fetch "/examples/datasets/data_reconstruction_envelope.json" "$workdir/data_reconstruction_envelope.json"
assert_contains "reconstruction_type" "$workdir/data_reconstruction_envelope.json"
assert_contains "synthetic_fixture" "$workdir/data_reconstruction_envelope.json"

echo "== Fetch target discovery example =="
fetch "/examples/datasets/readonly_target_discovery_example.json" "$workdir/readonly_target_discovery_example.json"
assert_contains "drift_protocol_program" "$workdir/readonly_target_discovery_example.json"
assert_contains "jupiter_perps" "$workdir/readonly_target_discovery_example.json"

echo "== Fetch Drift state discovery example =="
fetch "/examples/datasets/drift_readonly_state_example.json" "$workdir/drift_readonly_state_example.json"
assert_contains "drift_readonly_state_discovery" "$workdir/drift_readonly_state_example.json"
assert_contains "drift_perp_market_0_sol_perp" "$workdir/drift_readonly_state_example.json"
assert_contains "drift_spot_market_0_usdc" "$workdir/drift_readonly_state_example.json"
assert_contains "0ae3e3b1db782a6765c3525b3dec38ad4d9d3a62" "$workdir/drift_readonly_state_example.json"

echo "== Fetch Drift decoder provenance =="
fetch "/docs/drift-decoder-provenance.md" "$workdir/drift-decoder-provenance.md"
assert_contains "Drift Decoder Provenance" "$workdir/drift-decoder-provenance.md"
assert_contains "2.163.0-beta.0" "$workdir/drift-decoder-provenance.md"
assert_contains "9646dd6a893568d85d8dc47507e047010bf7e945" "$workdir/drift-decoder-provenance.md"
assert_contains "Shape Snapshot Scope" "$workdir/drift-decoder-provenance.md"

echo "== Fetch Drift liquidation scan boundary =="
fetch "/docs/drift-liquidation-scan-boundary.md" "$workdir/drift-liquidation-scan-boundary.md"
assert_contains "Drift Liquidation Scan Boundary" "$workdir/drift-liquidation-scan-boundary.md"
assert_contains "318,000 finalized transactions" "$workdir/drift-liquidation-scan-boundary.md"
assert_contains "415091952" "$workdir/drift-liquidation-scan-boundary.md"
assert_contains "does not prove" "$workdir/drift-liquidation-scan-boundary.md"
assert_contains "Until then, the scan is source-governance progress only" "$workdir/drift-liquidation-scan-boundary.md"

echo "== Fetch Drift shape snapshot example =="
fetch "/examples/datasets/drift_shape_snapshot_example.json" "$workdir/drift_shape_snapshot_example.json"
assert_contains "public_fields_decoded" "$workdir/drift_shape_snapshot_example.json"
assert_contains "expected_account_type" "$workdir/drift_shape_snapshot_example.json"
assert_contains "public_field_decode" "$workdir/drift_shape_snapshot_example.json"
assert_contains "market_economics_decoded" "$workdir/drift_shape_snapshot_example.json"
assert_contains '"field": "decimals"' "$workdir/drift_shape_snapshot_example.json"
assert_contains '"field": "market_index"' "$workdir/drift_shape_snapshot_example.json"
assert_contains '"field": "orders_enabled"' "$workdir/drift_shape_snapshot_example.json"
assert_contains '"field": "status"' "$workdir/drift_shape_snapshot_example.json"
assert_contains '"semantic_value": "Active"' "$workdir/drift_shape_snapshot_example.json"
assert_contains '"semantic_value": "Collateral"' "$workdir/drift_shape_snapshot_example.json"
assert_contains '"semantic_encoding": "bitset"' "$workdir/drift_shape_snapshot_example.json"
assert_contains '"field": "paused_operations"' "$workdir/drift_shape_snapshot_example.json"
assert_contains '"field": "pool_id"' "$workdir/drift_shape_snapshot_example.json"
assert_contains "raw_account_data_committed" "$workdir/drift_shape_snapshot_example.json"
assert_contains "field_decode_claimed" "$workdir/drift_shape_snapshot_example.json"
assert_contains '"field": "contract_type"' "$workdir/drift_shape_snapshot_example.json"
assert_contains '"field": "contract_tier"' "$workdir/drift_shape_snapshot_example.json"
assert_contains '"field": "amm_oracle"' "$workdir/drift_shape_snapshot_example.json"
assert_contains '"semantic_value": "Perpetual"' "$workdir/drift_shape_snapshot_example.json"

echo "== Fetch read-only decode worker example =="
fetch "/docs/read-only-decode-worker.md" "$workdir/read-only-decode-worker.md"
fetch "/examples/datasets/drift_readonly_decode_worker_run_example.json" "$workdir/drift_readonly_decode_worker_run_example.json"
assert_contains "Read-Only Decode Worker" "$workdir/read-only-decode-worker.md"
assert_contains "Private Run Envelope" "$workdir/read-only-decode-worker.md"
assert_contains "build_readonly_worker_run_envelope.py" "$workdir/read-only-decode-worker.md"
assert_contains "oprs.readonly_decode_worker_run.v0" "$workdir/drift_readonly_decode_worker_run_example.json"
assert_contains "one_shot_local_read_only" "$workdir/drift_readonly_decode_worker_run_example.json"
assert_contains '"transaction_submission_enabled": false' "$workdir/drift_readonly_decode_worker_run_example.json"

echo "== Fetch public Drift guardrail package =="
fetch "/examples/public/contract-index.json" "$workdir/public_contract_index.json"
fetch "/examples/public/drift-guardrails-v0/spot_guardrails.json" "$workdir/drift_spot_guardrails.json"
fetch "/examples/public/drift-guardrails-v0/perp_guardrails.json" "$workdir/drift_perp_guardrails.json"
fetch "/examples/public/drift-guardrails-v0/manifest.json" "$workdir/drift_guardrail_manifest.json"
fetch "/examples/public/drift-guardrails-v0/dq.json" "$workdir/drift_guardrail_dq.json"
assert_contains "oprs.spot_guardrail_snapshot.v0" "$workdir/drift_spot_guardrails.json"
assert_contains "oprs.perp_guardrail_snapshot.v0" "$workdir/drift_perp_guardrails.json"
assert_contains "SettleRevPool" "$workdir/drift_perp_guardrails.json"
assert_contains "drift_guardrails_v0_example" "$workdir/drift_guardrail_manifest.json"
assert_contains "no_user_state_claims" "$workdir/drift_guardrail_dq.json"
assert_contains "jupiter-authority-gap-v0" "$workdir/public_contract_index.json"
assert_contains "jupiter-onchain-decode-v0" "$workdir/public_contract_index.json"
assert_contains "phoenix-market-telemetry-v0" "$workdir/public_contract_index.json"
assert_contains "slot-regime-benchmark-v0" "$workdir/public_contract_index.json"

echo "== Fetch Jupiter Perps target discovery example =="
fetch "/examples/datasets/jupiter_perps_readonly_targets_example.json" "$workdir/jupiter_perps_readonly_targets_example.json"
assert_contains "jupiter_perps_readonly_target_discovery" "$workdir/jupiter_perps_readonly_targets_example.json"
assert_contains "PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu" "$workdir/jupiter_perps_readonly_targets_example.json"
assert_contains "jupiter_perps_custody_sol" "$workdir/jupiter_perps_readonly_targets_example.json"
assert_contains "jupiter_perps_oracle_sol" "$workdir/jupiter_perps_readonly_targets_example.json"

echo "== Fetch Jupiter Perps provenance =="
fetch "/docs/jupiter-perps-provenance.md" "$workdir/jupiter-perps-provenance.md"
assert_contains "Jupiter Perps Provenance" "$workdir/jupiter-perps-provenance.md"
assert_contains "630cfd72cad499f45453a53383d7ac6d3e09e022" "$workdir/jupiter-perps-provenance.md"
assert_contains "e7f21c9c44b077d0d10116305b97bbc152081b77" "$workdir/jupiter-perps-provenance.md"
assert_contains "8a150cee26dc07c040ca7c1640dc7ec36ba9a0f063923ec50b2438e306b19cab" "$workdir/jupiter-perps-provenance.md"
assert_contains "transaction-history sample" "$workdir/jupiter-perps-provenance.md"

echo "== Fetch Jupiter source authority audit =="
fetch "/docs/jupiter-source-authority-audit.md" "$workdir/jupiter-source-authority-audit.md"
assert_contains "Jupiter Source Authority Audit" "$workdir/jupiter-source-authority-audit.md"
assert_contains "onchain_anchor_idl_hashable" "$workdir/jupiter-source-authority-audit.md"
assert_contains "verified lifecycle pairing" "$workdir/jupiter-source-authority-audit.md"

echo "== Fetch Jupiter Perps transaction history example =="
fetch "/examples/datasets/jupiter_perps_transaction_history_example.json" "$workdir/jupiter_perps_transaction_history_example.json"
assert_contains "jupiter_perps_transaction_history_sample" "$workdir/jupiter_perps_transaction_history_example.json"
assert_contains "transaction_history_sample_only" "$workdir/jupiter_perps_transaction_history_example.json"
assert_contains "candidate_pair_unverified" "$workdir/jupiter_perps_transaction_history_example.json"
assert_contains "verified_request_fulfillment_pair_claimed" "$workdir/jupiter_perps_transaction_history_example.json"
assert_contains "shared_account_metadata_probe" "$workdir/jupiter_perps_transaction_history_example.json"
assert_contains "shared_perps_owned_non_executable_count" "$workdir/jupiter_perps_transaction_history_example.json"
assert_contains "candidate_strength" "$workdir/jupiter_perps_transaction_history_example.json"
assert_contains "stronger_candidate_count" "$workdir/jupiter_perps_transaction_history_example.json"
assert_contains "request_fulfillment_pair_claimed" "$workdir/jupiter_perps_transaction_history_example.json"
assert_contains "raw_transaction_committed" "$workdir/jupiter_perps_transaction_history_example.json"

echo "== Fetch Jupiter authority-gap package =="
fetch "/examples/public/jupiter-authority-gap-v0/gap_report.json" "$workdir/jupiter_authority_gap.json"
fetch "/examples/public/jupiter-authority-gap-v0/manifest.json" "$workdir/jupiter_authority_gap_manifest.json"
fetch "/examples/public/jupiter-authority-gap-v0/dq.json" "$workdir/jupiter_authority_gap_dq.json"
fetch "/datasets/sample/jupiter_synthetic_lifecycle_candidate_unverified_001/dry_run_output.json" "$workdir/jupiter_lifecycle_fixture.json"
fetch "/datasets/sample/jupiter_synthetic_lifecycle_weak_no_shared_jupiter_account_001/dry_run_output.json" "$workdir/jupiter_weak_lifecycle_fixture.json"
fetch "/datasets/sample/jupiter_synthetic_malformed_source_authority_001/dry_run_output.json" "$workdir/jupiter_malformed_source_fixture.json"
assert_contains "oprs.jupiter_authority_gap.v0" "$workdir/jupiter_authority_gap.json"
assert_contains "canonical_idl_or_source" "$workdir/jupiter_authority_gap.json"
assert_contains "candidate_pair_unverified" "$workdir/jupiter_authority_gap.json"
assert_contains "weak candidates" "$workdir/jupiter_authority_gap.json"
assert_contains "source_authority_resolved_for_layout_decode" "$workdir/jupiter_authority_gap.json"
assert_contains '"verified_pairing_claimed": false' "$workdir/jupiter_authority_gap.json"
assert_contains "jupiter_authority_gap_v0_example" "$workdir/jupiter_authority_gap_manifest.json"
assert_contains "no_verified_pairing_claim" "$workdir/jupiter_authority_gap_dq.json"
assert_contains "jupiter_synthetic_lifecycle_candidate_unverified_001" "$workdir/jupiter_lifecycle_fixture.json"
assert_contains '"canonical_decode_authorized": false' "$workdir/jupiter_lifecycle_fixture.json"
assert_contains '"verified_request_fulfillment_pair_claimed": false' "$workdir/jupiter_lifecycle_fixture.json"
assert_contains "jupiter_synthetic_lifecycle_weak_no_shared_jupiter_account_001" "$workdir/jupiter_weak_lifecycle_fixture.json"
assert_contains '"candidate_strength": "weak_candidate"' "$workdir/jupiter_weak_lifecycle_fixture.json"
assert_contains '"shared_jupiter_owned_non_executable_account_observed": false' "$workdir/jupiter_weak_lifecycle_fixture.json"
assert_contains "jupiter_synthetic_malformed_source_authority_001" "$workdir/jupiter_malformed_source_fixture.json"
assert_contains '"source_authority_status": "invalid_source_authority"' "$workdir/jupiter_malformed_source_fixture.json"
assert_contains '"candidate_strength": "source_authority_invalid"' "$workdir/jupiter_malformed_source_fixture.json"
assert_contains '"docs_linked_idl_canonical": false' "$workdir/jupiter_malformed_source_fixture.json"

echo "== Fetch Jupiter onchain decode package =="
fetch "/examples/public/jupiter-onchain-decode-v0/decode_report.json" "$workdir/jupiter_onchain_decode.json"
fetch "/examples/public/jupiter-onchain-decode-v0/manifest.json" "$workdir/jupiter_onchain_decode_manifest.json"
fetch "/examples/public/jupiter-onchain-decode-v0/dq.json" "$workdir/jupiter_onchain_decode_dq.json"
assert_contains "oprs.jupiter_onchain_decode.v0" "$workdir/jupiter_onchain_decode.json"
assert_contains "onchain_anchor_idl_hashable" "$workdir/jupiter_onchain_decode.json"
assert_contains "611de36592f4508438df16ebee2ff73b9789eda105ec712575d515b432d1ebaa" "$workdir/jupiter_onchain_decode.json"
assert_contains "PositionRequest" "$workdir/jupiter_onchain_decode.json"
assert_contains '"verified_pairing_claimed": false' "$workdir/jupiter_onchain_decode.json"
assert_contains "jupiter_onchain_decode_v0_example" "$workdir/jupiter_onchain_decode_manifest.json"
assert_contains "fresh_active_identifier_scrubbed" "$workdir/jupiter_onchain_decode_dq.json"

echo "== Fetch Phoenix market telemetry package =="
fetch "/examples/public/phoenix-market-telemetry-v0/telemetry_surfaces.json" "$workdir/phoenix_market_telemetry.json"
fetch "/examples/public/phoenix-market-telemetry-v0/manifest.json" "$workdir/phoenix_market_telemetry_manifest.json"
fetch "/examples/public/phoenix-market-telemetry-v0/dq.json" "$workdir/phoenix_market_telemetry_dq.json"
assert_contains "oprs.phoenix_market_telemetry.v0" "$workdir/phoenix_market_telemetry.json"
assert_contains "phoenix_http_l2_orderbook" "$workdir/phoenix_market_telemetry.json"
assert_contains "phoenix_funding_rate_history" "$workdir/phoenix_market_telemetry.json"
assert_contains "phoenix_ws_l2_stream" "$workdir/phoenix_market_telemetry.json"
assert_contains '"instruction_builder_claimed": false' "$workdir/phoenix_market_telemetry.json"
assert_contains '"execution_claimed": false' "$workdir/phoenix_market_telemetry.json"
assert_contains '"replay_ready": false' "$workdir/phoenix_market_telemetry.json"
assert_contains "phoenix_market_telemetry_v0_example" "$workdir/phoenix_market_telemetry_manifest.json"
assert_contains "no_execution_surface_claim" "$workdir/phoenix_market_telemetry_dq.json"
assert_contains "read_only_surfaces_only" "$workdir/phoenix_market_telemetry_dq.json"

echo "== Fetch Slot regime benchmark package =="
fetch "/docs/slot-regime-benchmark.md" "$workdir/slot-regime-benchmark.md"
fetch "/examples/public/slot-regime-benchmark-v0/benchmark_windows.json" "$workdir/slot_regime_benchmark.json"
fetch "/examples/public/slot-regime-benchmark-v0/manifest.json" "$workdir/slot_regime_benchmark_manifest.json"
fetch "/examples/public/slot-regime-benchmark-v0/dq.json" "$workdir/slot_regime_benchmark_dq.json"
assert_contains "Slot Regime Benchmark Boundary" "$workdir/slot-regime-benchmark.md"
assert_contains "oprs.slot_regime_benchmark.v0" "$workdir/slot_regime_benchmark.json"
assert_contains "440208000" "$workdir/slot_regime_benchmark.json"
assert_contains "2026-08-19T05:50:49Z" "$workdir/slot_regime_benchmark.json"
assert_contains '"performance_improvement_claimed": false' "$workdir/slot_regime_benchmark.json"
assert_contains '"validator_performance_claimed": false' "$workdir/slot_regime_benchmark.json"
assert_contains '"execution_claimed": false' "$workdir/slot_regime_benchmark.json"
assert_contains "slot_regime_benchmark_v0_example" "$workdir/slot_regime_benchmark_manifest.json"
assert_contains "no_performance_claim" "$workdir/slot_regime_benchmark_dq.json"

echo "== Fetch Phoenix Hawkeye validator plan =="
fetch "/docs/phoenix-hawkeye-validator-plan.md" "$workdir/phoenix-hawkeye-validator-plan.md"
fetch "/examples/datasets/phoenix_hawkeye_validator_plan_example.json" "$workdir/phoenix_hawkeye_validator_plan_example.json"
assert_contains "Phoenix / Hawkeye Validator Plan" "$workdir/phoenix-hawkeye-validator-plan.md"
assert_contains "oprs.phoenix_hawkeye_validator_plan.v0" "$workdir/phoenix_hawkeye_validator_plan_example.json"
assert_contains '"account_decode_ready": false' "$workdir/phoenix_hawkeye_validator_plan_example.json"
assert_contains '"replay_ready": false' "$workdir/phoenix_hawkeye_validator_plan_example.json"

echo "== Static 404 behavior =="
missing_status="$(status_code "/does-not-exist-oprs-smoke")"
env_status="$(status_code "/.env")"
checkpoint_status="$(status_code "/docs/checkpoints/")"
checkpoint_file_status="$(status_code "/docs/checkpoints/2026-06-04-hosted-monitoring-checkpoint.md")"
env_example_status="$(status_code "/.env.example")"
dockerfile_status="$(status_code "/Dockerfile")"
railway_iac_status="$(status_code "/.railway/railway.ts")"
package_json_status="$(status_code "/package.json")"
package_lock_status="$(status_code "/package-lock.json")"
railway_nginx_status="$(status_code "/deploy/railway/nginx.conf.template")"
if [ "$missing_status" != "404" ]; then
  echo "Expected 404 for missing path, got $missing_status" >&2
  exit 1
fi
if [ "$env_status" != "404" ]; then
  echo "Expected 404 for /.env, got $env_status" >&2
  exit 1
fi
if [ "$checkpoint_status" != "404" ]; then
  echo "Expected 404 for /docs/checkpoints/, got $checkpoint_status" >&2
  exit 1
fi
if [ "$checkpoint_file_status" != "404" ]; then
  echo "Expected 404 for checkpoint file, got $checkpoint_file_status" >&2
  exit 1
fi
if [ "$env_example_status" != "404" ]; then
  echo "Expected 404 for /.env.example, got $env_example_status" >&2
  exit 1
fi
if [ "$dockerfile_status" != "404" ]; then
  echo "Expected 404 for /Dockerfile, got $dockerfile_status" >&2
  exit 1
fi
if [ "$railway_iac_status" != "404" ]; then
  echo "Expected 404 for /.railway/railway.ts, got $railway_iac_status" >&2
  exit 1
fi
if [ "$package_json_status" != "404" ]; then
  echo "Expected 404 for /package.json, got $package_json_status" >&2
  exit 1
fi
if [ "$package_lock_status" != "404" ]; then
  echo "Expected 404 for /package-lock.json, got $package_lock_status" >&2
  exit 1
fi
if [ "$railway_nginx_status" != "404" ]; then
  echo "Expected 404 for /deploy/railway/nginx.conf.template, got $railway_nginx_status" >&2
  exit 1
fi

if [ "$base_url" = "https://refreshing-art-production-86de.up.railway.app" ]; then
  nosniff="$(header_value "/" "X-Content-Type-Options")"
  if [ "$nosniff" != "nosniff" ]; then
    echo "Expected Railway X-Content-Type-Options: nosniff, got ${nosniff:-missing}" >&2
    exit 1
  fi
fi

echo "== Public secret marker check =="
if assert_contains "HELIUS_RPC_URL|private_key|seed phrase|bearer token|wallet key" "$workdir/index.html" "$workdir/dashboard.html" "$workdir/proof-pack-changelog.md" "$workdir/data_reconstruction_envelope.json" "$workdir/readonly_target_discovery_example.json" "$workdir/drift_readonly_state_example.json" "$workdir/drift_shape_snapshot_example.json" "$workdir/drift_readonly_decode_worker_run_example.json" "$workdir/public_contract_index.json" "$workdir/drift_spot_guardrails.json" "$workdir/drift_perp_guardrails.json" "$workdir/drift_guardrail_manifest.json" "$workdir/drift_guardrail_dq.json" "$workdir/drift-decoder-provenance.md" "$workdir/drift-liquidation-scan-boundary.md" "$workdir/jupiter_perps_readonly_targets_example.json" "$workdir/jupiter_perps_transaction_history_example.json" "$workdir/jupiter-perps-provenance.md" "$workdir/jupiter_authority_gap.json" "$workdir/jupiter_authority_gap_manifest.json" "$workdir/jupiter_authority_gap_dq.json" "$workdir/jupiter_lifecycle_fixture.json" "$workdir/jupiter_weak_lifecycle_fixture.json" "$workdir/jupiter_malformed_source_fixture.json" "$workdir/phoenix_market_telemetry.json" "$workdir/phoenix_market_telemetry_manifest.json" "$workdir/phoenix_market_telemetry_dq.json" "$workdir/slot-regime-benchmark.md" "$workdir/slot_regime_benchmark.json" "$workdir/slot_regime_benchmark_manifest.json" "$workdir/slot_regime_benchmark_dq.json" "$workdir/phoenix-hawkeye-validator-plan.md" "$workdir/phoenix_hawkeye_validator_plan_example.json"; then
  echo "Public proof pack/dashboard contains a forbidden secret marker" >&2
  exit 1
fi

echo "== Hosted smoke checks passed =="
