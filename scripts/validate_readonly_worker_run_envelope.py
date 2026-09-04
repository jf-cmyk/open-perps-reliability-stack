#!/usr/bin/env python3
"""Validate a read-only worker run envelope."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

from public_package_contract import load_json, validate_json_schema


DEFAULT_PATH = Path("examples/datasets/readonly_worker_run_envelope_example.json")
SCHEMA_PATH = Path("schemas/datasets/readonly-worker-run-envelope-v0.json")
REQUIRED_FORBIDDEN_ACTIONS = {
    "sign",
    "submit_transaction",
    "retry_transaction",
    "bid_priority_fee",
    "load_keypair",
    "manage_custody",
    "manage_capital",
    "publish_without_review",
}
BLOCKED_VALUE_PATTERNS = {
    "rpc_url": re.compile(r"https://[^\"'\s]*(helius|rpc|api-key|apikey)[^\"'\s]*", re.IGNORECASE),
    "slack_webhook": re.compile(r"https://hooks\.slack(?:-gov)?\.com/services/[a-z0-9/_-]+", re.IGNORECASE),
    "bearer_token": re.compile(r"bearer\s+[a-z0-9._-]+", re.IGNORECASE),
    "absolute_local_path": re.compile(r"/Users/|/Volumes/|/private/"),
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


def validate_envelope(path: Path) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"missing read-only worker run envelope: {path}"]

    envelope = load_json(path)
    schema = load_json(SCHEMA_PATH)
    failures.extend(validate_json_schema(envelope, schema, "readonly-worker-run-envelope"))

    searchable_text = "\n".join(_string_values(envelope))
    for label, pattern in BLOCKED_VALUE_PATTERNS.items():
        if pattern.search(searchable_text):
            failures.append(f"{path}: blocked value marker `{label}`")

    artifacts = envelope.get("artifacts", [])
    protocols = [artifact.get("protocol") for artifact in artifacts if isinstance(artifact, dict)]
    declared_protocols = envelope.get("scope", {}).get("target_protocols", [])
    if sorted(set(protocols)) != sorted(set(declared_protocols)):
        failures.append("scope.target_protocols must match artifact protocols")

    if envelope.get("scope", {}).get("source_artifact_count") != len(artifacts):
        failures.append("scope.source_artifact_count must match artifacts length")

    validated_count = sum(
        1
        for artifact in artifacts
        if isinstance(artifact, dict) and artifact.get("validator_status") == "passed"
    )
    validation = envelope.get("validation", {})
    if validation.get("validated_artifact_count") != validated_count:
        failures.append("validation.validated_artifact_count must match passed artifact count")
    if validation.get("status") == "passed" and validated_count != len(artifacts):
        failures.append("validation.status=passed requires all artifacts to have validator_status=passed")
    if validation.get("secret_scan_passed") is not True:
        failures.append("validation.secret_scan_passed must be true")

    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        path_value = artifact.get("path", "")
        if not path_value.startswith("target/oprs-worker-runs/"):
            failures.append(f"artifact path must stay under target/oprs-worker-runs/: {path_value}")
        summary = artifact.get("summary", {})
        if summary.get("replay_ready") is not False:
            failures.append(f"{path_value}: summary.replay_ready must be false")
        if summary.get("execution_claimed") is not False:
            failures.append(f"{path_value}: summary.execution_claimed must be false")

    safety = envelope.get("safety_invariants", {})
    for key, value in safety.items():
        if value is not False:
            failures.append(f"safety_invariants.{key} must be false")

    promotion = envelope.get("promotion_policy", {})
    for key in ["public_output_published", "public_candidate_created"]:
        if promotion.get(key) is not False:
            failures.append(f"promotion_policy.{key} must be false")
    for key in [
        "promotion_requires_founder_review",
        "promotion_requires_validator_pass",
        "promotion_requires_scrub_pass",
    ]:
        if promotion.get(key) is not True:
            failures.append(f"promotion_policy.{key} must be true")

    missing_forbidden = sorted(REQUIRED_FORBIDDEN_ACTIONS - set(envelope.get("forbidden_actions", [])))
    if missing_forbidden:
        failures.append(f"forbidden_actions missing {missing_forbidden}")

    return failures


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PATH
    failures = validate_envelope(path)
    if failures:
        print("Read-only worker run envelope validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"PASS read-only worker run envelope: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
