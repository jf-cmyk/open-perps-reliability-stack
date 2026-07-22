#!/usr/bin/env python3
"""Validate scrubbed Drift liquidation-history probe output."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from public_package_contract import load_json, scan_blocked_text, validate_json_schema


SCHEMA_PATH = Path("schemas/datasets/drift-liquidation-history-probe-v0.json")
DEFAULT_PROBES = [Path("examples/datasets/drift_liquidation_history_probe_example.json")]


def scan_string_values(path: Path, value: Any, prefix: str = "$") -> list[str]:
    failures: list[str] = []
    if isinstance(value, str):
        return [
            failure.replace(str(path), f"{path}:{prefix}")
            for failure in scan_blocked_text(path, value)
        ]
    if isinstance(value, list):
        for index, item in enumerate(value):
            failures.extend(scan_string_values(path, item, f"{prefix}[{index}]"))
    if isinstance(value, dict):
        for key, item in value.items():
            failures.extend(scan_string_values(path, item, f"{prefix}.{key}"))
    return failures


def validate_probe(path: Path) -> list[str]:
    failures: list[str] = []
    schema = load_json(SCHEMA_PATH)
    probe = load_json(path)
    failures.extend(validate_json_schema(probe, schema, path.as_posix()))
    failures.extend(scan_string_values(path, probe))

    readiness = probe.get("readiness", {})
    must_be_false = [
        "auth_used",
        "trader_state_used",
        "instruction_builder_used",
        "order_operation_used",
        "raw_transaction_committed",
        "raw_logs_committed",
        "execution_claimed",
        "replay_ready",
    ]
    for flag in must_be_false:
        if readiness.get(flag) is not False:
            failures.append(f"{path}: readiness.{flag} must be false")

    candidates = probe.get("liquidation_candidates", [])
    summary = probe.get("scan_summary", {})
    if summary.get("liquidation_candidate_count") != len(candidates):
        failures.append(
            f"{path}: scan_summary.liquidation_candidate_count must match candidate rows"
        )

    for index, candidate in enumerate(candidates):
        if "matching_logs" in candidate:
            failures.append(f"{path}: candidate {index} must not include raw matching_logs")

    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("probes", nargs="*", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = args.probes or DEFAULT_PROBES
    failures: list[str] = []
    if not SCHEMA_PATH.exists():
        failures.append(f"missing schema: {SCHEMA_PATH}")
    for path in paths:
        if not path.exists():
            failures.append(f"missing Drift liquidation-history probe: {path}")
            continue
        failures.extend(validate_probe(path))

    if failures:
        print("Drift liquidation-history probe validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"PASS Drift liquidation-history probes: {len(paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
