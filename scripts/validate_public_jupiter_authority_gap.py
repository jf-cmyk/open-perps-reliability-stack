#!/usr/bin/env python3
"""Validate the public Jupiter authority-gap example package."""

from __future__ import annotations

import sys
from pathlib import Path

from public_package_contract import (
    load_json,
    scan_blocked_text,
    validate_json_schema,
    validate_manifest_dq_and_outputs,
)


DEFAULT_PACKAGE = Path("examples/public/jupiter-authority-gap-v0")


def validate_package(package_dir: Path) -> list[str]:
    failures: list[str] = []
    manifest_path = package_dir / "manifest.json"
    gap_path = package_dir / "gap_report.json"
    dq_path = package_dir / "dq.json"

    for required in [manifest_path, gap_path, dq_path]:
        if not required.exists():
            failures.append(f"missing required file: {required}")
    if failures:
        return failures

    manifest = load_json(manifest_path)
    gap_report = load_json(gap_path)
    dq = load_json(dq_path)
    schema = load_json(Path("schemas/datasets/jupiter-authority-gap-v0.json"))
    failures.extend(validate_json_schema(gap_report, schema, "jupiter-authority-gap"))

    for path in [manifest_path, gap_path, dq_path]:
        failures.extend(scan_blocked_text(path, path.read_text(encoding="utf-8")))

    readiness = gap_report.get("readiness", {})
    for key in [
        "canonical_source_confirmed",
        "binary_decode_claimed",
        "verified_pairing_claimed",
        "replay_ready",
    ]:
        if readiness.get(key) is not False:
            failures.append(f"gap_report readiness.{key} must be false")

    for record in gap_report.get("records", []):
        if record.get("status") not in {"blocked", "unverified"}:
            failures.append(f"gap record {record.get('gap_id')} must stay blocked or unverified")
        if "verified" in record.get("safe_interim_label", "") and "unverified" not in record.get(
            "safe_interim_label", ""
        ):
            failures.append(f"gap record {record.get('gap_id')} safe label overclaims verification")
        for evidence_ref in record.get("public_evidence_refs", []):
            if (
                not evidence_ref
                or evidence_ref.startswith("/")
                or ".." in evidence_ref
                or evidence_ref.startswith("http://")
                or evidence_ref.startswith("https://")
            ):
                failures.append(f"gap record {record.get('gap_id')} has unsafe evidence ref")

    failures.extend(
        validate_manifest_dq_and_outputs(
            package_dir=package_dir,
            manifest=manifest,
            dq=dq,
            row_counts_by_output_path={
                "gap_report.json": len(gap_report.get("records", [])),
                "dq.json": len(dq.get("checks", [])),
            },
        )
    )

    return failures


def run_self_tests() -> list[str]:
    failures: list[str] = []
    package_dir = DEFAULT_PACKAGE
    gap_report = load_json(package_dir / "gap_report.json")
    gap_report["readiness"]["verified_pairing_claimed"] = True
    tmp_dir = Path("target/jupiter-authority-gap-negative-self-test")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    for path in ["manifest.json", "dq.json"]:
        (tmp_dir / path).write_text((package_dir / path).read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_dir / "gap_report.json").write_text(json_dumps(gap_report), encoding="utf-8")
    observed = validate_package(tmp_dir)
    if not any("verified_pairing_claimed" in failure for failure in observed):
        failures.append("self-test expected verified_pairing_claimed failure")
    return failures


def json_dumps(value: object) -> str:
    import json

    return json.dumps(value, indent=2, sort_keys=True)


def main() -> int:
    package_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKAGE
    failures = validate_package(package_dir)
    if len(sys.argv) == 1:
        failures.extend(run_self_tests())
    if failures:
        print("Public Jupiter authority-gap package validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"PASS public Jupiter authority-gap package: {package_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
