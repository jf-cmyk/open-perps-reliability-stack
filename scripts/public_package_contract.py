"""Shared offline helpers for public proof-pack package validators."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_CONTRACT_INDEX = Path("examples/public/contract-index.json")

BLOCKED_PATTERNS = {
    "rpc_url": re.compile(r"https://[^\"'\s]*(helius|rpc|api-key|apikey)[^\"'\s]*", re.IGNORECASE),
    "env_file": re.compile(r"(^|[/:])\.env(\b|$)"),
    "local_path": re.compile(r"/Users/|/Volumes/|/private/"),
    "bearer_token": re.compile(r"bearer\s+[a-z0-9._-]+", re.IGNORECASE),
    "private_key": re.compile(r"private[_ -]?key|seed phrase|keypair|wallet secret", re.IGNORECASE),
    "custody_or_capital": re.compile(r"custody|capital allocation|capital_limit|inventory", re.IGNORECASE),
    "raw_payload": re.compile(r"raw_account_bytes|account_data_base64|raw_bytes", re.IGNORECASE),
    "user_state_claim": re.compile(r"user_position|user_account|margin_health|liquidation_opportunity", re.IGNORECASE),
    "execution_claim": re.compile(r"submit_transaction|priority_fee_bid|capital_limit|wallet_inventory", re.IGNORECASE),
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


def load_contract_entry(
    package_id: str,
    expected_validator: str,
    index_path: Path = DEFAULT_CONTRACT_INDEX,
) -> tuple[dict[str, Any] | None, list[str]]:
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
        failures.append(f"{package_id}: capability must be read_only_dry_run")
    if entry.get("publishable") is not True:
        failures.append(f"{package_id}: publishable must be true")
    if entry.get("validator") != expected_validator:
        failures.append(f"{package_id}: validator must point to {expected_validator}")

    boundary = entry.get("claim_boundary", {})
    if not boundary.get("allowed_claims") or not boundary.get("blocked_claims"):
        failures.append(f"{package_id}: claim_boundary must include allowed_claims and blocked_claims")

    for key in ["manifest_path", "dq_path", "validator"]:
        value = entry.get(key, "")
        if not is_safe_relative_path(value):
            failures.append(f"{package_id}: {key} must be a safe relative path")
        elif key != "validator" and not Path(value).exists():
            failures.append(f"{package_id}: {key} does not exist: {value}")

    for payload in entry.get("payloads", []):
        for key in ["path", "schema_path"]:
            value = payload.get(key, "")
            if not is_safe_relative_path(value):
                failures.append(f"{package_id}: payload {key} must be a safe relative path")
            elif not Path(value).exists():
                failures.append(f"{package_id}: payload {key} does not exist: {value}")

    return entry, failures


def validate_manifest_dq_and_outputs(
    *,
    package_dir: Path,
    manifest: dict[str, Any],
    dq: dict[str, Any],
    row_counts_by_output_path: dict[str, int],
) -> list[str]:
    failures: list[str] = []
    if manifest.get("capability") != "read_only_dry_run":
        failures.append("manifest capability must be read_only_dry_run")
    if manifest.get("scrub", {}).get("status") != "passed":
        failures.append("manifest scrub.status must be passed")
    if manifest.get("dq", {}).get("blocking_failures") != 0:
        failures.append("manifest dq.blocking_failures must be 0")

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
        if relative_path in row_counts_by_output_path:
            observed_rows = row_counts_by_output_path[relative_path]
            if observed_rows != output.get("row_count"):
                failures.append(
                    f"{relative_path} row_count mismatch: {observed_rows} != {output.get('row_count')}"
                )

    for check in dq.get("checks", []):
        if check.get("severity") == "block_publish" and check.get("status") != "pass":
            failures.append(f"blocking DQ gate did not pass: {check.get('gate_id')}")

    return failures


def validate_payload_schema_versions(
    payloads: list[tuple[dict[str, Any], dict[str, Any]]],
) -> list[str]:
    failures: list[str] = []
    for spec, payload in payloads:
        label = spec.get("role", Path(spec.get("path", "")).name)
        if payload.get("schema_version") != spec.get("schema_version"):
            failures.append(
                f"{label} schema_version mismatch: {payload.get('schema_version')} != {spec.get('schema_version')}"
            )
    return failures
