#!/usr/bin/env python3
"""Validate machine-readable source-review records."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from public_package_contract import load_json, scan_blocked_text, validate_json_schema


SCHEMA_PATH = Path("schemas/datasets/source-review-record-v0.json")
DEFAULT_RECORDS = [
    Path("examples/datasets/jupiter_position_authority_source_review_example.json"),
    Path("examples/datasets/drift_public_field_source_review_template.json"),
]


def validate_record(path: Path) -> list[str]:
    failures: list[str] = []
    schema = load_json(SCHEMA_PATH)
    record = load_json(path)
    failures.extend(validate_json_schema(record, schema, path.as_posix()))
    failures.extend(scan_string_values(path, record))

    forbidden_claims = record.get("forbidden_claims", {})
    for claim, value in forbidden_claims.items():
        if value is not False:
            failures.append(f"{path}: forbidden claim `{claim}` must be false")

    approval_status = record.get("approval_status")
    gates: dict[str, Any] = record.get("approval_gates", {})
    if approval_status == "approved":
        incomplete = sorted(key for key, value in gates.items() if value is not True)
        if incomplete:
            failures.append(f"{path}: approved record has incomplete gates: {incomplete}")

    if record.get("review_kind") == "jupiter_position_authority_confirmation":
        source_status = record.get("source_authority", {}).get("status")
        if source_status != "canonical_confirmed":
            if approval_status not in {"blocked", "rejected"}:
                failures.append(
                    f"{path}: Jupiter authority without canonical source must be blocked or rejected"
                )
            if gates.get("canonical_source_confirmed") is not False:
                failures.append(
                    f"{path}: Jupiter canonical_source_confirmed must be false until source authority lands"
                )

    if record.get("review_kind") == "drift_public_field_offset":
        if gates.get("local_validator_required") is not True:
            failures.append(f"{path}: Drift source review must require local validator")
        if gates.get("local_only_until_scrubbed") is not True:
            failures.append(f"{path}: Drift source review must stay local-only until scrubbed")

    source_refs = record.get("source_authority", {}).get("source_refs", [])
    for ref in source_refs:
        if isinstance(ref, str) and not (
            ref.startswith("http://")
            or ref.startswith("https://")
            or (not Path(ref).is_absolute() and ".." not in Path(ref).parts)
        ):
            failures.append(f"{path}: unsafe source ref {ref!r}")

    return failures


def scan_string_values(path: Path, value: Any, prefix: str = "$") -> list[str]:
    failures: list[str] = []
    if isinstance(value, str):
        return [failure.replace(str(path), f"{path}:{prefix}") for failure in scan_blocked_text(path, value)]
    if isinstance(value, list):
        for index, item in enumerate(value):
            failures.extend(scan_string_values(path, item, f"{prefix}[{index}]"))
    if isinstance(value, dict):
        for key, item in value.items():
            failures.extend(scan_string_values(path, item, f"{prefix}.{key}"))
    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("records", nargs="*", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = args.records or DEFAULT_RECORDS
    failures: list[str] = []
    if not SCHEMA_PATH.exists():
        failures.append(f"missing schema: {SCHEMA_PATH}")
    for path in paths:
        if not path.exists():
            failures.append(f"missing source-review record: {path}")
            continue
        failures.extend(validate_record(path))

    if failures:
        print("Source-review record validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"PASS source-review records: {len(paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
