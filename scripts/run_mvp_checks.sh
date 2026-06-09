#!/usr/bin/env bash
set -euo pipefail

echo "== Open Perps Reliability Stack MVP checks =="

echo "== Fixture replay validation =="
cargo run -p oprs-replay --example validate_fixtures

echo "== Public API example validation =="
cargo run -p oprs-api-types --example validate_api_examples

echo "== Rust tests =="
cargo test

echo "== Static proof-pack markers =="
rg -q "Open Perps Reliability Stack Proof Pack" index.html
rg -q "Read-only" index.html
rg -q "Dry-run" index.html
rg -q "Open Perps" apps/dashboard/index.html
rg -q "No live execution" apps/dashboard/index.html
rg -q "ExecutionDisabledDryRun" apps/dashboard/index.html
rg -q "AdapterVersionMismatch" apps/dashboard/index.html

echo "== Deployment config =="
python3 -m json.tool railway.json >/dev/null
python3 -m json.tool schemas/datasets/data-reconstruction-envelope-v0.json >/dev/null
python3 -m json.tool examples/datasets/data_reconstruction_envelope.json >/dev/null
python3 -m json.tool examples/datasets/readonly_target_discovery_example.json >/dev/null
python3 -m json.tool examples/datasets/drift_readonly_state_example.json >/dev/null
python3 -m json.tool examples/datasets/drift_shape_snapshot_example.json >/dev/null
python3 -m json.tool schemas/datasets/readonly-decode-worker-run-v0.json >/dev/null
python3 -m json.tool schemas/datasets/public-contract-index-v0.json >/dev/null
python3 -m json.tool schemas/datasets/spot-guardrail-snapshot-v0.json >/dev/null
python3 -m json.tool schemas/datasets/perp-guardrail-snapshot-v0.json >/dev/null
python3 -m json.tool schemas/datasets/jupiter-authority-gap-v0.json >/dev/null
python3 -m json.tool examples/datasets/drift_readonly_decode_worker_run_example.json >/dev/null
python3 -m json.tool examples/public/contract-index.json >/dev/null
python3 -m json.tool examples/public/drift-guardrails-v0/spot_guardrails.json >/dev/null
python3 -m json.tool examples/public/drift-guardrails-v0/perp_guardrails.json >/dev/null
python3 -m json.tool examples/public/drift-guardrails-v0/manifest.json >/dev/null
python3 -m json.tool examples/public/drift-guardrails-v0/dq.json >/dev/null
python3 -m json.tool examples/public/jupiter-authority-gap-v0/gap_report.json >/dev/null
python3 -m json.tool examples/public/jupiter-authority-gap-v0/manifest.json >/dev/null
python3 -m json.tool examples/public/jupiter-authority-gap-v0/dq.json >/dev/null
python3 -m json.tool examples/datasets/jupiter_perps_readonly_targets_example.json >/dev/null
python3 -m json.tool examples/datasets/jupiter_perps_transaction_history_example.json >/dev/null
PYTHONPYCACHEPREFIX=target/pycache python3 -m py_compile scripts/discover_readonly_targets.py
PYTHONPYCACHEPREFIX=target/pycache python3 -m py_compile scripts/discover_drift_readonly_state.py
PYTHONPYCACHEPREFIX=target/pycache python3 -m py_compile scripts/discover_jupiter_perps_readonly_targets.py
PYTHONPYCACHEPREFIX=target/pycache python3 -m py_compile scripts/discover_jupiter_perps_transaction_history.py
PYTHONPYCACHEPREFIX=target/pycache python3 -m py_compile scripts/audit_jupiter_source_authority.py
PYTHONPYCACHEPREFIX=target/pycache python3 -m py_compile scripts/validate_public_contract_index.py
PYTHONPYCACHEPREFIX=target/pycache python3 -m py_compile scripts/validate_public_guardrail_package.py
PYTHONPYCACHEPREFIX=target/pycache python3 -m py_compile scripts/validate_public_jupiter_authority_gap.py
scripts/validate_public_contract_index.py
scripts/validate_public_guardrail_package.py
scripts/validate_public_jupiter_authority_gap.py
test -f Dockerfile
test -f deploy/railway/nginx.conf.template
rg -q 'try_files \$uri \$uri/ =404;' deploy/railway/nginx.conf.template
rg -q '^docs/checkpoints$' .dockerignore
test -f docs/service-boundaries.md
test -f docs/public-artifact-boundary.md
test -f docs/drift-decoder-provenance.md
test -f docs/jupiter-perps-provenance.md
test -f docs/jupiter-source-authority-audit.md
test -f docs/read-only-decode-worker.md
test -f schemas/datasets/data-reconstruction-envelope-v0.json
test -f schemas/datasets/readonly-decode-worker-run-v0.json
test -f schemas/datasets/public-contract-index-v0.json
test -f schemas/datasets/spot-guardrail-snapshot-v0.json
test -f schemas/datasets/perp-guardrail-snapshot-v0.json
test -f schemas/datasets/jupiter-authority-gap-v0.json
test -f examples/datasets/data_reconstruction_envelope.json
test -f examples/datasets/readonly_target_discovery_example.json
test -f examples/datasets/drift_readonly_state_example.json
test -f examples/datasets/drift_shape_snapshot_example.json
test -f examples/datasets/drift_readonly_decode_worker_run_example.json
test -f examples/public/contract-index.json
test -f examples/public/drift-guardrails-v0/spot_guardrails.json
test -f examples/public/drift-guardrails-v0/perp_guardrails.json
test -f examples/public/drift-guardrails-v0/manifest.json
test -f examples/public/drift-guardrails-v0/dq.json
test -f examples/public/jupiter-authority-gap-v0/gap_report.json
test -f examples/public/jupiter-authority-gap-v0/manifest.json
test -f examples/public/jupiter-authority-gap-v0/dq.json
test -f examples/datasets/jupiter_perps_readonly_targets_example.json
test -f examples/datasets/jupiter_perps_transaction_history_example.json
test -x scripts/build_public_artifact.sh
test -x scripts/run_hosted_smoke_checks.sh
test -x scripts/discover_drift_readonly_state.py
test -x scripts/discover_jupiter_perps_readonly_targets.py
test -x scripts/discover_jupiter_perps_transaction_history.py
test -x scripts/audit_jupiter_source_authority.py
test -x scripts/validate_public_contract_index.py
test -x scripts/validate_public_guardrail_package.py
test -x scripts/validate_public_jupiter_authority_gap.py

echo "== Public artifact boundary =="
artifact_dir="target/public-proof-pack-mvp-check-$$"
trap 'rm -rf "$artifact_dir"' EXIT
scripts/build_public_artifact.sh "$artifact_dir" >/dev/null
test -f "$artifact_dir/index.html"
test -f "$artifact_dir/apps/dashboard/index.html"
test -f "$artifact_dir/docs/deployment-railway.md"
test ! -e "$artifact_dir/docs/checkpoints"
test ! -e "$artifact_dir/.env.example"
test ! -e "$artifact_dir/Dockerfile"
test ! -e "$artifact_dir/railway.json"
test ! -e "$artifact_dir/deploy/railway/nginx.conf.template"
if find "$artifact_dir" -name '~$*' | rg -q .; then
  echo "Public artifact contains a Word lock file" >&2
  exit 1
fi

echo "== Local Helius configuration =="
if [ -f .env ] && grep -Eq '^HELIUS_RPC_URL="?[^"]+"?$' .env; then
  echo "HELIUS_RPC_URL present in local .env"
else
  echo "HELIUS_RPC_URL not configured locally; read-only decode proof will be skipped"
fi

echo "== MVP checks passed =="
