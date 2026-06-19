#!/usr/bin/env python3
"""Validate a local Phoenix market telemetry probe output under target/."""

from __future__ import annotations

import sys
from pathlib import Path

from public_package_contract import load_json, scan_blocked_text, validate_json_schema


DEFAULT_PROBE = Path("target/oprs-phoenix-market-telemetry/latest.json")
SCHEMA_PATH = Path("schemas/datasets/phoenix-market-telemetry-probe-v0.json")


def validate_probe(probe_path: Path) -> list[str]:
    failures: list[str] = []
    if not probe_path.exists():
        return [f"missing probe output: {probe_path}"]
    if not SCHEMA_PATH.exists():
        return [f"missing probe schema: {SCHEMA_PATH}"]

    probe = load_json(probe_path)
    schema = load_json(SCHEMA_PATH)
    failures.extend(validate_json_schema(probe, schema, "phoenix-market-telemetry-probe"))
    failures.extend(scan_blocked_text(probe_path, probe_path.read_text(encoding="utf-8")))

    if probe.get("query", {}).get("path") != "/v1/exchange/snapshot":
        failures.append("probe query.path must stay /v1/exchange/snapshot")
    if probe.get("response_summary", {}).get("http_status") != 200:
        failures.append("probe http_status must be 200")
    if probe.get("response_summary", {}).get("market_count", 0) <= 0:
        failures.append("probe market_count must be positive")
    if probe.get("response_summary", {}).get("sample_market_count", 0) > probe.get("query", {}).get("max_markets", 0):
        failures.append("probe sample_market_count exceeds query.max_markets")

    readiness = probe.get("readiness", {})
    for key in [
        "auth_used",
        "trader_state_used",
        "instruction_builder_used",
        "order_operation_used",
        "raw_response_committed",
        "execution_claimed",
        "replay_ready",
    ]:
        if readiness.get(key) is not False:
            failures.append(f"probe readiness.{key} must be false")

    scrub = probe.get("scrub", {})
    for key in [
        "raw_response_committed",
        "account_addresses_committed",
        "credential_material_committed",
    ]:
        if scrub.get(key) is not False:
            failures.append(f"probe scrub.{key} must be false")

    return failures


def main() -> int:
    probe_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PROBE
    failures = validate_probe(probe_path)
    if failures:
        print("Phoenix market telemetry probe validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"PASS Phoenix market telemetry probe: {probe_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
