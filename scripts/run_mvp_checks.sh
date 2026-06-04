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
rg -q "OpenPerp" apps/dashboard/index.html
rg -q "No live execution" apps/dashboard/index.html
rg -q "ExecutionDisabledDryRun" apps/dashboard/index.html
rg -q "AdapterVersionMismatch" apps/dashboard/index.html

echo "== Deployment config =="
python3 -m json.tool railway.json >/dev/null
test -f Dockerfile
test -f deploy/railway/nginx.conf.template
rg -q 'try_files \$uri \$uri/ =404;' deploy/railway/nginx.conf.template
test -x scripts/run_hosted_smoke_checks.sh

echo "== Local Helius configuration =="
if [ -f .env ] && grep -Eq '^HELIUS_RPC_URL="?[^"]+"?$' .env; then
  echo "HELIUS_RPC_URL present in local .env"
else
  echo "HELIUS_RPC_URL not configured locally; read-only decode proof will be skipped"
fi

echo "== MVP checks passed =="
