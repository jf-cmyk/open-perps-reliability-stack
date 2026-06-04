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

status_code() {
  local path="$1"
  curl -sS -o /dev/null -w "%{http_code}" "$base_url$path"
}

echo "== Hosted proof-pack smoke checks =="
echo "Target: $base_url"

echo "== Fetch proof pack =="
fetch "/" "$workdir/index.html"
rg -q "Open Perps Reliability Stack Proof Pack" "$workdir/index.html"
rg -q "Read-only" "$workdir/index.html"
rg -q "Dry-run" "$workdir/index.html"

echo "== Fetch dashboard =="
fetch "/apps/dashboard/" "$workdir/dashboard.html"
rg -q "OpenPerp" "$workdir/dashboard.html"
rg -q "No live execution" "$workdir/dashboard.html"
rg -q "ExecutionDisabledDryRun" "$workdir/dashboard.html"
rg -q "AdapterVersionMismatch" "$workdir/dashboard.html"

echo "== Static 404 behavior =="
missing_status="$(status_code "/does-not-exist-oprs-smoke")"
env_status="$(status_code "/.env")"
if [ "$missing_status" != "404" ]; then
  echo "Expected 404 for missing path, got $missing_status" >&2
  exit 1
fi
if [ "$env_status" != "404" ]; then
  echo "Expected 404 for /.env, got $env_status" >&2
  exit 1
fi

echo "== Public secret marker check =="
if rg -q "HELIUS_RPC_URL|private_key|seed phrase|bearer token|wallet key" "$workdir/index.html" "$workdir/dashboard.html"; then
  echo "Public proof pack/dashboard contains a forbidden secret marker" >&2
  exit 1
fi

echo "== Hosted smoke checks passed =="
