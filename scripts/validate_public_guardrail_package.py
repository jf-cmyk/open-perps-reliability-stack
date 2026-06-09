#!/usr/bin/env python3
"""Validate the committed public Drift guardrail example package.

This validator is intentionally offline and dependency-free. It checks the
mechanical gates that matter for publishing: checksums, row counts, readiness
flags, and absence of common secret/user-state markers.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


DEFAULT_PACKAGE = Path("examples/public/drift-guardrails-v0")

BLOCKED_PATTERNS = {
    "rpc_url": re.compile(r"https://[^\"'\s]*(helius|rpc|api-key|apikey)[^\"'\s]*", re.IGNORECASE),
    "env_file": re.compile(r"(^|[/:])\.env(\b|$)"),
    "local_path": re.compile(r"/Users/|/Volumes/|/private/"),
    "bearer_token": re.compile(r"bearer\s+[a-z0-9._-]+", re.IGNORECASE),
    "private_key": re.compile(r"private[_ -]?key|seed phrase|keypair|wallet secret", re.IGNORECASE),
    "custody_or_capital": re.compile(r"custody|capital allocation|capital_limit|inventory", re.IGNORECASE),
    "raw_account_bytes": re.compile(r"raw_account_bytes|account_data_base64|raw_bytes", re.IGNORECASE),
    "user_state_claim": re.compile(r"user_position|user_account|margin_health|liquidation_opportunity", re.IGNORECASE),
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scan_blocked_text(path: Path, text: str) -> list[str]:
    failures = []
    for label, pattern in BLOCKED_PATTERNS.items():
        if pattern.search(text):
            failures.append(f"{path}: blocked marker `{label}`")
    return failures


def validate_package(package_dir: Path) -> list[str]:
    failures: list[str] = []
    manifest_path = package_dir / "manifest.json"
    guardrails_path = package_dir / "guardrails.json"
    dq_path = package_dir / "dq.json"

    for required in [manifest_path, guardrails_path, dq_path]:
        if not required.exists():
            failures.append(f"missing required file: {required}")

    if failures:
        return failures

    manifest = load_json(manifest_path)
    guardrails = load_json(guardrails_path)
    dq = load_json(dq_path)

    for path in [manifest_path, guardrails_path, dq_path]:
        failures.extend(scan_blocked_text(path, path.read_text(encoding="utf-8")))

    if manifest.get("capability") != "read_only_dry_run":
        failures.append("manifest capability must be read_only_dry_run")
    if manifest.get("scrub", {}).get("status") != "passed":
        failures.append("manifest scrub.status must be passed")
    if manifest.get("dq", {}).get("blocking_failures") != 0:
        failures.append("manifest dq.blocking_failures must be 0")

    readiness = guardrails.get("readiness", {})
    required_false = ["user_state_decoded", "market_economics_decoded", "replay_ready"]
    for key in required_false:
        if readiness.get(key) is not False:
            failures.append(f"guardrails readiness.{key} must be false")
    if readiness.get("public_guardrails_decoded") is not True:
        failures.append("guardrails readiness.public_guardrails_decoded must be true")

    records = guardrails.get("records", [])
    if not isinstance(records, list) or not records:
        failures.append("guardrails.records must be a non-empty array")

    output_specs = manifest.get("outputs", [])
    for output in output_specs:
        relative_path = output.get("path")
        if not relative_path:
            failures.append("manifest output missing path")
            continue
        output_path = package_dir / relative_path
        if not output_path.exists():
            failures.append(f"manifest output missing file: {relative_path}")
            continue
        observed_sha = sha256_file(output_path)
        if observed_sha != output.get("sha256"):
            failures.append(f"{relative_path} sha256 mismatch: {observed_sha}")
        if relative_path == "guardrails.json":
            observed_rows = len(records)
        elif relative_path == "dq.json":
            observed_rows = len(dq.get("checks", []))
        else:
            observed_rows = None
        if observed_rows is not None and observed_rows != output.get("row_count"):
            failures.append(
                f"{relative_path} row_count mismatch: {observed_rows} != {output.get('row_count')}"
            )

    for check in dq.get("checks", []):
        if check.get("severity") == "block_publish" and check.get("status") != "pass":
            failures.append(f"blocking DQ gate did not pass: {check.get('gate_id')}")

    return failures


def main() -> int:
    package_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKAGE
    failures = validate_package(package_dir)
    if failures:
        print("Public guardrail package validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"PASS public guardrail package: {package_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
