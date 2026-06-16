#!/usr/bin/env python3
"""Validate the public Phoenix market telemetry example package."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from public_package_contract import (
    load_contract_entry,
    load_json,
    scan_blocked_text,
    validate_json_schema,
    validate_manifest_dq_and_outputs,
    validate_payload_schema_versions,
)


DEFAULT_PACKAGE = Path("examples/public/phoenix-market-telemetry-v0")
DEFAULT_PACKAGE_ID = "phoenix-market-telemetry-v0"


def validate_package(package_dir: Path, contract_entry: dict[str, Any] | None = None) -> list[str]:
    failures: list[str] = []
    manifest_path = package_dir / "manifest.json"
    telemetry_path = package_dir / "telemetry_surfaces.json"
    dq_path = package_dir / "dq.json"

    if contract_entry is not None:
        expected_manifest = Path(contract_entry.get("manifest_path", ""))
        expected_dq = Path(contract_entry.get("dq_path", ""))
        if expected_manifest != manifest_path:
            failures.append(f"contract index manifest_path mismatch: {expected_manifest} != {manifest_path}")
        if expected_dq != dq_path:
            failures.append(f"contract index dq_path mismatch: {expected_dq} != {dq_path}")
        payload_specs = contract_entry.get("payloads", [])
    else:
        payload_specs = [
            {
                "role": "telemetry_surfaces",
                "path": str(telemetry_path),
                "schema_path": "schemas/datasets/phoenix-market-telemetry-v0.json",
                "schema_version": "oprs.phoenix_market_telemetry.v0",
            }
        ]

    for required in [manifest_path, telemetry_path, dq_path]:
        if not required.exists():
            failures.append(f"missing required file: {required}")
    for spec in payload_specs:
        schema_path = Path(spec.get("schema_path", ""))
        if not schema_path.exists():
            failures.append(f"missing payload schema: {schema_path}")
    if failures:
        return failures

    manifest = load_json(manifest_path)
    telemetry = load_json(telemetry_path)
    dq = load_json(dq_path)

    for spec in payload_specs:
        schema = load_json(Path(spec["schema_path"]))
        failures.extend(validate_json_schema(telemetry, schema, spec.get("role", "telemetry_surfaces")))

    for path in [manifest_path, telemetry_path, dq_path]:
        failures.extend(scan_blocked_text(path, path.read_text(encoding="utf-8")))

    failures.extend(validate_payload_schema_versions([(payload_specs[0], telemetry)]))

    readiness = telemetry.get("readiness", {})
    required_true = [
        "market_metadata_supported",
        "orderbook_snapshot_supported",
        "live_stream_supported",
    ]
    for key in required_true:
        if readiness.get(key) is not True:
            failures.append(f"telemetry readiness.{key} must be true")
    required_false = [
        "trader_state_claimed",
        "instruction_builder_claimed",
        "execution_claimed",
        "replay_ready",
    ]
    for key in required_false:
        if readiness.get(key) is not False:
            failures.append(f"telemetry readiness.{key} must be false")

    records = telemetry.get("records", [])
    if not isinstance(records, list) or not records:
        failures.append("telemetry records must be a non-empty array")
    for record in records:
        surface_id = record.get("surface_id", "<missing>")
        if record.get("read_only_supported") is not True:
            failures.append(f"{surface_id}: read_only_supported must be true")
        if record.get("access_surface") not in {"public_http", "public_websocket"}:
            failures.append(f"{surface_id}: access_surface must be public_http or public_websocket")
        for source_ref in record.get("public_source_refs", []):
            if not (
                source_ref.startswith("https://docs.phoenix.trade/")
                or source_ref.startswith("https://github.com/ellipsis-labs/")
            ):
                failures.append(f"{surface_id}: unsupported public source ref {source_ref}")
        joined_blocked = " ".join(record.get("blocked_operations", [])).lower()
        for marker in ["order placement", "order cancellation", "instruction building"]:
            if marker not in joined_blocked:
                failures.append(f"{surface_id}: blocked_operations must include {marker}")

    failures.extend(
        validate_manifest_dq_and_outputs(
            package_dir=package_dir,
            manifest=manifest,
            dq=dq,
            row_counts_by_output_path={
                "telemetry_surfaces.json": len(records),
                "dq.json": len(dq.get("checks", [])),
            },
        )
    )

    return failures


def run_self_tests(contract_entry: dict[str, Any] | None) -> list[str]:
    failures: list[str] = []
    if contract_entry is None:
        failures.append("self-test requires contract entry")
        return failures

    package_dir = DEFAULT_PACKAGE
    telemetry = load_json(package_dir / "telemetry_surfaces.json")
    telemetry["readiness"]["execution_claimed"] = True
    tmp_dir = Path("target/phoenix-market-telemetry-negative-self-test")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    for path in ["manifest.json", "dq.json"]:
        (tmp_dir / path).write_text((package_dir / path).read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_dir / "telemetry_surfaces.json").write_text(json_dumps(telemetry), encoding="utf-8")
    observed = validate_package(tmp_dir, None)
    if not any("execution_claimed" in failure for failure in observed):
        failures.append("self-test expected execution_claimed failure")
    return failures


def json_dumps(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True)


def main() -> int:
    package_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKAGE
    contract_entry, index_failures = load_contract_entry(
        DEFAULT_PACKAGE_ID,
        "scripts/validate_public_phoenix_market_telemetry.py",
    )
    failures = index_failures + validate_package(package_dir, contract_entry)
    if len(sys.argv) == 1:
        failures.extend(run_self_tests(contract_entry))
    if failures:
        print("Public Phoenix market telemetry package validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"PASS public Phoenix market telemetry package: {package_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
