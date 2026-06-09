#!/usr/bin/env python3
"""Validate the committed public Drift guardrail example package.

This validator is intentionally offline and dependency-free. It checks the
mechanical gates that matter for publishing: checksums, row counts, readiness
flags, and absence of common secret/user-state markers.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from public_package_contract import (
    load_contract_entry,
    load_json,
    scan_blocked_text,
    validate_manifest_dq_and_outputs,
    validate_payload_schema_versions,
)


DEFAULT_PACKAGE = Path("examples/public/drift-guardrails-v0")
DEFAULT_PACKAGE_ID = "drift-guardrails-v0"


def validate_package(package_dir: Path, contract_entry: dict[str, Any] | None = None) -> list[str]:
    failures: list[str] = []
    manifest_path = package_dir / "manifest.json"
    dq_path = package_dir / "dq.json"
    if contract_entry is not None:
        expected_manifest = Path(contract_entry.get("manifest_path", ""))
        expected_dq = Path(contract_entry.get("dq_path", ""))
        if expected_manifest != manifest_path:
            failures.append(f"contract index manifest_path mismatch: {expected_manifest} != {manifest_path}")
        if expected_dq != dq_path:
            failures.append(f"contract index dq_path mismatch: {expected_dq} != {dq_path}")

    if contract_entry is None:
        payload_specs = [
            {
                "role": "spot_guardrails",
                "path": str(package_dir / "spot_guardrails.json"),
                "schema_path": "schemas/datasets/spot-guardrail-snapshot-v0.json",
                "schema_version": "oprs.spot_guardrail_snapshot.v0",
            },
            {
                "role": "perp_guardrails",
                "path": str(package_dir / "perp_guardrails.json"),
                "schema_path": "schemas/datasets/perp-guardrail-snapshot-v0.json",
                "schema_version": "oprs.perp_guardrail_snapshot.v0",
            },
        ]
    else:
        payload_specs = contract_entry.get("payloads", [])
    payload_paths = [Path(spec.get("path", "")) for spec in payload_specs]

    for required in [manifest_path, *payload_paths, dq_path]:
        if not required.exists():
            failures.append(f"missing required file: {required}")
    for spec in payload_specs:
        schema_path = Path(spec.get("schema_path", ""))
        if not schema_path.exists():
            failures.append(f"missing payload schema: {schema_path}")

    if failures:
        return failures

    manifest = load_json(manifest_path)
    dq = load_json(dq_path)
    payloads = [(spec, load_json(Path(spec["path"]))) for spec in payload_specs]

    for path in [manifest_path, *payload_paths, dq_path]:
        failures.extend(scan_blocked_text(path, path.read_text(encoding="utf-8")))

    records_by_path = {Path(spec["path"]).name: payload.get("records", []) for spec, payload in payloads}
    failures.extend(validate_payload_schema_versions(payloads))
    for spec, payload in payloads:
        label = spec.get("role", Path(spec["path"]).name)
        readiness = payload.get("readiness", {})
        required_false = ["user_state_decoded", "market_economics_decoded", "replay_ready"]
        for key in required_false:
            if readiness.get(key) is not False:
                failures.append(f"{label} readiness.{key} must be false")
        if readiness.get("public_guardrails_decoded") is not True:
            failures.append(f"{label} readiness.public_guardrails_decoded must be true")
        records = payload.get("records", [])
        if not isinstance(records, list) or not records:
            failures.append(f"{label}.records must be a non-empty array")

    failures.extend(
        validate_manifest_dq_and_outputs(
            package_dir=package_dir,
            manifest=manifest,
            dq=dq,
            row_counts_by_output_path={
                **{path: len(records) for path, records in records_by_path.items()},
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
    manifest_path = package_dir / "manifest.json"
    manifest = load_json(manifest_path)
    manifest["outputs"][0]["sha256"] = "0" * 64
    tmp_dir = Path("target/public-guardrail-negative-self-test")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    for path in ["spot_guardrails.json", "perp_guardrails.json", "dq.json"]:
        (tmp_dir / path).write_text((package_dir / path).read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_dir / "manifest.json").write_text(json_dumps(manifest), encoding="utf-8")
    observed = validate_package(tmp_dir, None)
    if not any("sha256 mismatch" in failure for failure in observed):
        failures.append("self-test expected sha256 mismatch")
    return failures


def json_dumps(value: object) -> str:
    import json

    return json.dumps(value, indent=2, sort_keys=True)


def main() -> int:
    package_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKAGE
    contract_entry, index_failures = load_contract_entry(
        DEFAULT_PACKAGE_ID,
        "scripts/validate_public_guardrail_package.py",
    )
    failures = index_failures + validate_package(package_dir, contract_entry)
    if len(sys.argv) == 1:
        failures.extend(run_self_tests(contract_entry))
    if failures:
        print("Public guardrail package validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"PASS public guardrail package: {package_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
