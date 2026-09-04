#!/usr/bin/env python3
"""Validate a read-only worker public-candidate summary."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

from public_package_contract import load_json, validate_json_schema


DEFAULT_PATH = Path("examples/datasets/readonly_worker_public_candidate_example.json")
SCHEMA_PATH = Path("schemas/datasets/readonly-worker-public-candidate-v0.json")
BLOCKED_VALUE_PATTERNS = {
    "rpc_url": re.compile(r"https://[^\"'\s]*(helius|rpc|api-key|apikey)[^\"'\s]*", re.IGNORECASE),
    "slack_webhook": re.compile(r"https://hooks\.slack(?:-gov)?\.com/services/[a-z0-9/_-]+", re.IGNORECASE),
    "bearer_token": re.compile(r"bearer\s+[a-z0-9._-]+", re.IGNORECASE),
    "local_path": re.compile(r"/Users/|/Volumes/|/private/|target/oprs-worker-runs/"),
    "private_key": re.compile(r"private[_ -]?key|seed phrase|wallet secret", re.IGNORECASE),
    "raw_payload": re.compile(r"raw_account_bytes|account_data_base64|raw_bytes", re.IGNORECASE),
}


def _string_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        values: list[str] = []
        for item in value:
            values.extend(_string_values(item))
        return values
    if isinstance(value, dict):
        values = []
        for item in value.values():
            values.extend(_string_values(item))
        return values
    return []


def validate_candidate(path: Path) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"missing read-only worker public candidate: {path}"]

    candidate = load_json(path)
    schema = load_json(SCHEMA_PATH)
    failures.extend(validate_json_schema(candidate, schema, "readonly-worker-public-candidate"))

    searchable_text = "\n".join(_string_values(candidate))
    for label, pattern in BLOCKED_VALUE_PATTERNS.items():
        if pattern.search(searchable_text):
            failures.append(f"{path}: blocked value marker `{label}`")

    protocols = candidate.get("protocols", [])
    artifact_count = candidate.get("source_envelope", {}).get("artifact_count")
    if artifact_count != len(protocols):
        failures.append("source_envelope.artifact_count must match protocols length")

    validated_count = sum(
        1
        for protocol in protocols
        if isinstance(protocol, dict) and protocol.get("validator_status") == "passed"
    )
    summary = candidate.get("summary", {})
    if summary.get("validated_artifact_count") != validated_count:
        failures.append("summary.validated_artifact_count must match passed protocol count")

    gates = candidate.get("promotion_gates", {})
    if gates.get("public_output_published") is not False:
        failures.append("promotion_gates.public_output_published must be false")
    if gates.get("public_package_manifest_created") is not False:
        failures.append("promotion_gates.public_package_manifest_created must be false")
    if gates.get("public_package_dq_created") is not False:
        failures.append("promotion_gates.public_package_dq_created must be false")

    status = summary.get("public_candidate_status")
    if gates.get("founder_review_recorded") is not True and status != "blocked_pending_founder_review":
        failures.append("missing founder review must keep public_candidate_status blocked")
    if gates.get("founder_review_recorded") is True and status == "blocked_pending_founder_review":
        failures.append("founder-reviewed candidate should not remain blocked_pending_founder_review")
    if summary.get("validation_status") != "passed" and status != "blocked_validation_failed":
        failures.append("failed validation must keep public_candidate_status blocked_validation_failed")

    policy = candidate.get("public_payload_policy", {})
    for key in [
        "private_artifact_paths_committed",
        "private_payload_bodies_committed",
        "raw_account_data_committed",
        "raw_transaction_committed",
    ]:
        if policy.get(key) is not False:
            failures.append(f"public_payload_policy.{key} must be false")
    if policy.get("only_counts_hashes_and_status") is not True:
        failures.append("public_payload_policy.only_counts_hashes_and_status must be true")

    for protocol in protocols:
        if not isinstance(protocol, dict):
            continue
        if protocol.get("replay_ready") is not False:
            failures.append(f"{protocol.get('protocol')}: replay_ready must be false")
        if protocol.get("execution_claimed") is not False:
            failures.append(f"{protocol.get('protocol')}: execution_claimed must be false")

    safety = candidate.get("safety_invariants", {})
    for key, value in safety.items():
        if value is not False:
            failures.append(f"safety_invariants.{key} must be false")

    return failures


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PATH
    failures = validate_candidate(path)
    if failures:
        print("Read-only worker public candidate validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"PASS read-only worker public candidate: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
