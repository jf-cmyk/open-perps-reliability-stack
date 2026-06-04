#!/usr/bin/env bash
set -euo pipefail

base_url="${1:-${RAILWAY_PUBLIC_URL:-https://refreshing-art-production-86de.up.railway.app}}"
base_url="${base_url%/}"

workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

fetch() {
  local path="$1"
  local out="$2"
  curl -fsSL "$base_url$path" -o "$out"
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
  curl -sS -o /dev/null -w "%{http_code}" "$base_url$path"
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
assert_contains "OpenPerp" "$workdir/dashboard.html"
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

echo "== Static 404 behavior =="
missing_status="$(status_code "/does-not-exist-oprs-smoke")"
env_status="$(status_code "/.env")"
checkpoint_status="$(status_code "/docs/checkpoints/")"
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

echo "== Public secret marker check =="
if assert_contains "HELIUS_RPC_URL|private_key|seed phrase|bearer token|wallet key" "$workdir/index.html" "$workdir/dashboard.html"; then
  echo "Public proof pack/dashboard contains a forbidden secret marker" >&2
  exit 1
fi

echo "== Hosted smoke checks passed =="
