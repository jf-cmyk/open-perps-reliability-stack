#!/usr/bin/env python3
"""Validate the public Jupiter onchain decode package."""

from __future__ import annotations

import sys
from pathlib import Path

from public_package_contract import (
    load_json,
    scan_blocked_text,
    validate_json_schema,
    validate_manifest_dq_and_outputs,
)


DEFAULT_PACKAGE = Path("examples/public/jupiter-onchain-decode-v0")


def validate_package(package_dir: Path) -> list[str]:
    failures: list[str] = []
    manifest_path = package_dir / "manifest.json"
    report_path = package_dir / "decode_report.json"
    dq_path = package_dir / "dq.json"

    for required in [manifest_path, report_path, dq_path]:
        if not required.exists():
            failures.append(f"missing required file: {required}")
    if failures:
        return failures

    manifest = load_json(manifest_path)
    report = load_json(report_path)
    dq = load_json(dq_path)
    schema = load_json(Path("schemas/datasets/jupiter-onchain-decode-v0.json"))
    failures.extend(validate_json_schema(report, schema, "jupiter-onchain-decode"))

    for path in [manifest_path, report_path, dq_path]:
        failures.extend(scan_blocked_text(path, path.read_text(encoding="utf-8")))

    source = report.get("source_authority", {})
    if source.get("authority_status") != "onchain_anchor_idl_hashable":
        failures.append("source_authority.authority_status must be onchain_anchor_idl_hashable")
    if source.get("program_owned_idl_account") is not True:
        failures.append("source_authority.program_owned_idl_account must be true")
    if source.get("docs_linked_candidate_matched") is not False:
        failures.append("docs-linked candidate mismatch must remain explicitly false")

    readiness = report.get("readiness", {})
    required_readiness = {
        "canonical_source_confirmed": True,
        "binary_decode_claimed": True,
        "verified_pairing_claimed": False,
        "replay_ready": False,
        "execution_claimed": False,
        "account_bytes_published": False,
    }
    for key, expected in required_readiness.items():
        if readiness.get(key) is not expected:
            failures.append(f"readiness.{key} must be {expected}")

    records = report.get("decode_records", [])
    names = {record.get("account_name") for record in records}
    if names != {"Position", "PositionRequest"}:
        failures.append("decode records must include exactly Position and PositionRequest")
    for record in records:
        identifier = record.get("account_identifier", {})
        if record.get("account_name") == "PositionRequest":
            if identifier.get("pubkey_redacted") is not True:
                failures.append("PositionRequest active account pubkey must be redacted")
            if "pubkey" in identifier:
                failures.append("PositionRequest active account pubkey must not be published")
        fields = record.get("selected_decoded_fields", {})
        if record.get("account_name") == "PositionRequest":
            for key in ["requestChange", "requestType", "side", "executed", "counter", "bump"]:
                if key not in fields:
                    failures.append(f"PositionRequest missing selected field {key}")
        if record.get("account_name") == "Position":
            for key in ["side", "price", "sizeUsd", "collateralUsd", "openTime", "updateTime", "bump"]:
                if key not in fields:
                    failures.append(f"Position missing selected field {key}")

    failures.extend(
        validate_manifest_dq_and_outputs(
            package_dir=package_dir,
            manifest=manifest,
            dq=dq,
            row_counts_by_output_path={
                "decode_report.json": len(records),
                "dq.json": len(dq.get("checks", [])),
            },
        )
    )
    return failures


def main() -> int:
    package_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKAGE
    failures = validate_package(package_dir)
    if failures:
        print("Public Jupiter onchain decode package validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"PASS public Jupiter onchain decode package: {package_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
