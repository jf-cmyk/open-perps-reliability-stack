#!/usr/bin/env python3
"""Validate a read-only worker soak summary."""

from __future__ import annotations

import sys
import re
from pathlib import Path
from typing import Any

from public_package_contract import load_json, validate_json_schema


DEFAULT_PATH = Path("examples/datasets/readonly_soak_summary_example.json")
SCHEMA_PATH = Path("schemas/datasets/readonly-soak-summary-v0.json")
BLOCKED_LITERAL_PATTERNS = {
    "rpc_url": re.compile(r"https://[^\"'\s]*(helius|rpc|api-key|apikey)[^\"'\s]*", re.IGNORECASE),
    "bearer_token": re.compile(r"bearer\s+[a-z0-9._-]+", re.IGNORECASE),
    "local_path": re.compile(r"/Users/|/Volumes/|/private/"),
    "seed_phrase": re.compile(r"seed phrase", re.IGNORECASE),
    "wallet_secret": re.compile(r"wallet secret", re.IGNORECASE),
}


def _bool(value: Any) -> bool:
    return isinstance(value, bool) and value


def validate_summary(path: Path) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"missing read-only soak summary: {path}"]

    text = path.read_text(encoding="utf-8")
    for label, pattern in BLOCKED_LITERAL_PATTERNS.items():
        if pattern.search(text):
            failures.append(f"{path}: blocked literal marker `{label}`")

    report = load_json(path)
    schema = load_json(SCHEMA_PATH)
    failures.extend(validate_json_schema(report, schema, "readonly-soak-summary"))

    daily_checks = report.get("daily_checks", [])
    summary = report.get("summary", {})
    status = report.get("status")
    exit_decision = report.get("exit_decision", {})

    if len(daily_checks) != summary.get("expected_day_count"):
        failures.append("daily_checks length must match summary.expected_day_count")

    expected_days = list(range(1, len(daily_checks) + 1))
    actual_days = [day.get("day") for day in daily_checks if isinstance(day, dict)]
    if actual_days != expected_days:
        failures.append("daily_checks day values must be sequential from 1")

    passed_days = sum(1 for day in daily_checks if day.get("status") == "passed")
    failed_days = sum(1 for day in daily_checks if day.get("status") == "failed")
    if summary.get("passed_day_count") != passed_days:
        failures.append("summary.passed_day_count must match daily_checks")
    if summary.get("failed_day_count") != failed_days:
        failures.append("summary.failed_day_count must match daily_checks")

    for key in [
        "signing_enabled",
        "transaction_submission_enabled",
        "priority_fee_bidding_enabled",
        "block_engine_submission_enabled",
        "keypair_loading_enabled",
        "custody_enabled",
        "capital_management_enabled",
    ]:
        if report.get("safety_invariants", {}).get(key) is not False:
            failures.append(f"safety_invariants.{key} must be false")

    if status == "passed":
        required_true_fields = [
            "worker_completed_or_failed_closed",
            "secret_marker_scan_passed",
            "execution_marker_scan_passed",
            "schema_validation_passed",
            "probe_validator_passed",
            "freshness_recorded",
            "claim_boundary_reviewed",
        ]
        if len(daily_checks) != 7:
            failures.append("passed soak must include exactly 7 daily checks")
        if passed_days != 7:
            failures.append("passed soak must have 7 passed daily checks")
        if failed_days != 0:
            failures.append("passed soak must have zero failed daily checks")
        if summary.get("secret_marker_finding_count") != 0:
            failures.append("passed soak must have zero secret marker findings")
        if summary.get("execution_marker_finding_count") != 0:
            failures.append("passed soak must have zero execution marker findings")
        if exit_decision.get("recommendation") != "launch_read_only_service":
            failures.append("passed soak recommendation must be launch_read_only_service")
        if exit_decision.get("worker_can_be_operationally_live") is not True:
            failures.append("passed soak must mark worker_can_be_operationally_live true")
        for day in daily_checks:
            label = f"day {day.get('day')}"
            for field in required_true_fields:
                if not _bool(day.get(field)):
                    failures.append(f"{label}: {field} must be true for passed soak")
            if day.get("public_output_published") is not False:
                failures.append(f"{label}: public_output_published must remain false")
    else:
        if exit_decision.get("worker_can_be_operationally_live") is True:
            failures.append("only a passed soak can mark worker_can_be_operationally_live true")

    if exit_decision.get("execution_pilot_authorized") is not False:
        failures.append("exit_decision.execution_pilot_authorized must be false")

    return failures


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PATH
    failures = validate_summary(path)
    if failures:
        print("Read-only soak summary validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"PASS read-only soak summary: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
