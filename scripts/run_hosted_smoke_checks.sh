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

echo "== Fetch dashboard =="
fetch "/apps/dashboard/" "$workdir/dashboard.html"
assert_contains "Open Perps" "$workdir/dashboard.html"
assert_contains "No live execution" "$workdir/dashboard.html"
assert_contains "ExecutionDisabledDryRun" "$workdir/dashboard.html"
assert_contains "AdapterVersionMismatch" "$workdir/dashboard.html"

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

echo "== Static 404 behavior =="
missing_status="$(status_code "/does-not-exist-oprs-smoke")"
env_status="$(status_code "/.env")"
checkpoint_status="$(status_code "/docs/checkpoints/")"
checkpoint_file_status="$(status_code "/docs/checkpoints/2026-06-04-hosted-monitoring-checkpoint.md")"
env_example_status="$(status_code "/.env.example")"
dockerfile_status="$(status_code "/Dockerfile")"
railway_json_status="$(status_code "/railway.json")"
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
if [ "$railway_json_status" != "404" ]; then
  echo "Expected 404 for /railway.json, got $railway_json_status" >&2
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
if assert_contains "HELIUS_RPC_URL|private_key|seed phrase|bearer token|wallet key" "$workdir/index.html" "$workdir/dashboard.html" "$workdir/data_reconstruction_envelope.json" "$workdir/readonly_target_discovery_example.json" "$workdir/drift_readonly_state_example.json" "$workdir/drift-decoder-provenance.md"; then
  echo "Public proof pack/dashboard contains a forbidden secret marker" >&2
  exit 1
fi

echo "== Hosted smoke checks passed =="
