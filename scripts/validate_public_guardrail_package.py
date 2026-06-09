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
DEFAULT_CONTRACT_INDEX = Path("examples/public/contract-index.json")
DEFAULT_PACKAGE_ID = "drift-guardrails-v0"

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


def is_safe_relative_path(path: str) -> bool:
    candidate = Path(path)
    return bool(path) and not candidate.is_absolute() and ".." not in candidate.parts


def scan_blocked_text(path: Path, text: str) -> list[str]:
    failures = []
    for label, pattern in BLOCKED_PATTERNS.items():
        if pattern.search(text):
            failures.append(f"{path}: blocked marker `{label}`")
    return failures


def load_contract_entry(index_path: Path, package_id: str) -> tuple[dict[str, Any] | None, list[str]]:
    failures: list[str] = []
    if not index_path.exists():
        return None, [f"missing contract index: {index_path}"]
    index = load_json(index_path)
    if index.get("contract_index_version") != "oprs.public_contract_index.v0":
        failures.append("contract index version must be oprs.public_contract_index.v0")
    packages = index.get("packages", [])
    if not isinstance(packages, list):
        failures.append("contract index packages must be an array")
        return None, failures
    matches = [package for package in packages if package.get("package_id") == package_id]
    if len(matches) != 1:
        failures.append(f"contract index must contain exactly one `{package_id}` package")
        return None, failures
    entry = matches[0]
    if entry.get("capability") != "read_only_dry_run":
        failures.append("contract index package capability must be read_only_dry_run")
    if entry.get("publishable") is not True:
        failures.append("contract index package must be publishable")
    if entry.get("validator") != "scripts/validate_public_guardrail_package.py":
        failures.append("contract index validator must point to scripts/validate_public_guardrail_package.py")
    boundary = entry.get("claim_boundary", {})
    if not boundary.get("allowed_claims") or not boundary.get("blocked_claims"):
        failures.append("contract index claim_boundary must include allowed_claims and blocked_claims")
    for key in ["manifest_path", "dq_path", "validator"]:
        value = entry.get(key, "")
        if not is_safe_relative_path(value):
            failures.append(f"contract index {key} must be a package-safe relative path")
    for payload in entry.get("payloads", []):
        for key in ["path", "schema_path"]:
            value = payload.get(key, "")
            if not is_safe_relative_path(value):
                failures.append(f"contract index payload {key} must be a package-safe relative path")
    return entry, failures


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

    if manifest.get("capability") != "read_only_dry_run":
        failures.append("manifest capability must be read_only_dry_run")
    if manifest.get("scrub", {}).get("status") != "passed":
        failures.append("manifest scrub.status must be passed")
    if manifest.get("dq", {}).get("blocking_failures") != 0:
        failures.append("manifest dq.blocking_failures must be 0")

    records_by_path = {Path(spec["path"]).name: payload.get("records", []) for spec, payload in payloads}
    for spec, payload in payloads:
        label = spec.get("role", Path(spec["path"]).name)
        if payload.get("schema_version") != spec.get("schema_version"):
            failures.append(
                f"{label} schema_version mismatch: {payload.get('schema_version')} != {spec.get('schema_version')}"
            )
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
        if relative_path in records_by_path:
            observed_rows = len(records_by_path[relative_path])
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
    contract_entry, index_failures = load_contract_entry(DEFAULT_CONTRACT_INDEX, DEFAULT_PACKAGE_ID)
    failures = index_failures + validate_package(package_dir, contract_entry)
    if failures:
        print("Public guardrail package validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"PASS public guardrail package: {package_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
