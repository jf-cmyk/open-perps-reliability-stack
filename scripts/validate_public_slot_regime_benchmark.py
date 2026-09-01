#!/usr/bin/env python3
"""Validate the public Solana slot-regime benchmark package."""

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


DEFAULT_PACKAGE = Path("examples/public/slot-regime-benchmark-v0")
DEFAULT_PACKAGE_ID = "slot-regime-benchmark-v0"


def validate_package(package_dir: Path, contract_entry: dict[str, Any] | None = None) -> list[str]:
    failures: list[str] = []
    manifest_path = package_dir / "manifest.json"
    benchmark_path = package_dir / "benchmark_windows.json"
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
                "role": "benchmark_windows",
                "path": str(benchmark_path),
                "schema_path": "schemas/datasets/slot-regime-benchmark-v0.json",
                "schema_version": "oprs.slot_regime_benchmark.v0",
            }
        ]

    for required in [manifest_path, benchmark_path, dq_path]:
        if not required.exists():
            failures.append(f"missing required file: {required}")
    for spec in payload_specs:
        schema_path = Path(spec.get("schema_path", ""))
        if not schema_path.exists():
            failures.append(f"missing payload schema: {schema_path}")
    if failures:
        return failures

    manifest = load_json(manifest_path)
    benchmark = load_json(benchmark_path)
    dq = load_json(dq_path)

    for spec in payload_specs:
        schema = load_json(Path(spec["schema_path"]))
        failures.extend(validate_json_schema(benchmark, schema, spec.get("role", "benchmark_windows")))

    for path in [manifest_path, benchmark_path, dq_path]:
        failures.extend(scan_blocked_text(path, path.read_text(encoding="utf-8")))

    failures.extend(validate_payload_schema_versions([(payload_specs[0], benchmark)]))

    activation = benchmark.get("activation", {})
    if activation.get("activation_slot") != 440208000:
        failures.append("activation.activation_slot must be 440208000")
    if activation.get("previous_slot_duration_target_ms") != 400:
        failures.append("activation.previous_slot_duration_target_ms must be 400")
    if activation.get("new_slot_duration_target_ms") != 350:
        failures.append("activation.new_slot_duration_target_ms must be 350")

    readiness = benchmark.get("readiness", {})
    if readiness.get("activation_boundary_verified") is not True:
        failures.append("readiness.activation_boundary_verified must be true")
    for key in [
        "slot_duration_observed",
        "performance_improvement_claimed",
        "validator_performance_claimed",
        "execution_claimed",
        "replay_ready",
    ]:
        if readiness.get(key) is not False:
            failures.append(f"readiness.{key} must be false")

    records = benchmark.get("records", [])
    relations = {record.get("relation_to_activation") for record in records}
    if relations != {"pre_activation", "post_activation"}:
        failures.append("records must contain exactly pre_activation and post_activation windows")
    for record in records:
        window_id = record.get("window_id", "<missing>")
        if record.get("read_only_supported") is not True:
            failures.append(f"{window_id}: read_only_supported must be true")
        blocked = " ".join(record.get("blocked_claims", [])).lower()
        for marker in ["claim", "no"]:
            if marker not in blocked:
                failures.append(f"{window_id}: blocked_claims must explicitly reject claims")
        if record.get("relation_to_activation") == "pre_activation":
            if record.get("slot_range", {}).get("end_slot") >= activation.get("activation_slot", 0):
                failures.append(f"{window_id}: pre_activation window must end before activation slot")
            if record.get("slot_range", {}).get("slot_duration_target_ms") != 400:
                failures.append(f"{window_id}: pre_activation target duration must be 400")
        if record.get("relation_to_activation") == "post_activation":
            if record.get("slot_range", {}).get("start_slot") < activation.get("activation_slot", 0):
                failures.append(f"{window_id}: post_activation window must start at or after activation slot")
            if record.get("slot_range", {}).get("slot_duration_target_ms") != 350:
                failures.append(f"{window_id}: post_activation target duration must be 350")

    failures.extend(
        validate_manifest_dq_and_outputs(
            package_dir=package_dir,
            manifest=manifest,
            dq=dq,
            row_counts_by_output_path={
                "benchmark_windows.json": len(records),
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
    benchmark = load_json(package_dir / "benchmark_windows.json")
    benchmark["readiness"]["performance_improvement_claimed"] = True
    tmp_dir = Path("target/slot-regime-benchmark-negative-self-test")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    for path in ["manifest.json", "dq.json"]:
        (tmp_dir / path).write_text((package_dir / path).read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_dir / "benchmark_windows.json").write_text(json_dumps(benchmark), encoding="utf-8")
    observed = validate_package(tmp_dir, None)
    if not any("performance_improvement_claimed" in failure for failure in observed):
        failures.append("self-test expected performance_improvement_claimed failure")
    return failures


def json_dumps(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True)


def main() -> int:
    package_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKAGE
    contract_entry, index_failures = load_contract_entry(
        DEFAULT_PACKAGE_ID,
        "scripts/validate_public_slot_regime_benchmark.py",
    )
    failures = index_failures + validate_package(package_dir, contract_entry)
    if len(sys.argv) == 1:
        failures.extend(run_self_tests(contract_entry))
    if failures:
        print("Public slot-regime benchmark package validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"PASS public slot-regime benchmark package: {package_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
