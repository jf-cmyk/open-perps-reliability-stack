#!/usr/bin/env python3
"""Validate the public Jupiter authority-gap example package."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


DEFAULT_PACKAGE = Path("examples/public/jupiter-authority-gap-v0")

BLOCKED_PATTERNS = {
    "rpc_url": re.compile(r"https://[^\"'\s]*(helius|rpc|api-key|apikey)[^\"'\s]*", re.IGNORECASE),
    "env_file": re.compile(r"(^|[/:])\.env(\b|$)"),
    "local_path": re.compile(r"/Users/|/Volumes/|/private/"),
    "bearer_token": re.compile(r"bearer\s+[a-z0-9._-]+", re.IGNORECASE),
    "private_key": re.compile(r"private[_ -]?key|seed phrase|keypair|wallet secret", re.IGNORECASE),
    "raw_payload": re.compile(r"raw_account_bytes|account_data_base64|raw_bytes", re.IGNORECASE),
    "execution_claim": re.compile(r"submit_transaction|priority_fee_bid|capital_limit|wallet_inventory", re.IGNORECASE),
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

    for path in [manifest_path, gap_path, dq_path]:
        failures.extend(scan_blocked_text(path, path.read_text(encoding="utf-8")))

    if manifest.get("capability") != "read_only_dry_run":
        failures.append("manifest capability must be read_only_dry_run")
    if manifest.get("scrub", {}).get("status") != "passed":
        failures.append("manifest scrub.status must be passed")
    if manifest.get("dq", {}).get("blocking_failures") != 0:
        failures.append("manifest dq.blocking_failures must be 0")

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

    output_specs = manifest.get("outputs", [])
    records_by_path = {
        "gap_report.json": gap_report.get("records", []),
        "dq.json": dq.get("checks", []),
    }
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
        observed_rows = len(records_by_path.get(relative_path, []))
        if observed_rows != output.get("row_count"):
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
        print("Public Jupiter authority-gap package validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"PASS public Jupiter authority-gap package: {package_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
