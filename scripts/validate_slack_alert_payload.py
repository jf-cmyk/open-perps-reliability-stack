#!/usr/bin/env python3
"""Validate a scrubbed Slack alert payload for the read-only worker."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

from public_package_contract import load_json, validate_json_schema


DEFAULT_PATH = Path("examples/datasets/slack_alert_payload_example.json")
SCHEMA_PATH = Path("schemas/datasets/slack-alert-payload-v0.json")
BLOCKED_VALUE_PATTERNS = {
    "rpc_url": re.compile(r"https://[^\"'\s]*(helius|rpc|api-key|apikey)[^\"'\s]*", re.IGNORECASE),
    "slack_webhook": re.compile(r"https://hooks\.slack(?:-gov)?\.com/services/[a-z0-9/_-]+", re.IGNORECASE),
    "bearer_token": re.compile(r"bearer\s+[a-z0-9._-]+", re.IGNORECASE),
    "local_path": re.compile(r"/Users/|/Volumes/|/private/"),
    "private_key": re.compile(r"private[_ -]?key|seed phrase|keypair|wallet secret", re.IGNORECASE),
    "raw_payload": re.compile(r"raw_account_bytes|account_data_base64|raw_transaction_body|raw_bytes", re.IGNORECASE),
}
FALSE_INVARIANTS = [
    "contains_rpc_url",
    "contains_api_key",
    "contains_webhook_url",
    "contains_private_key",
    "contains_seed_phrase",
    "contains_wallet_path",
    "contains_raw_transaction_body",
    "contains_raw_account_bytes",
    "contains_signer_or_custody_config",
    "contains_capital_or_execution_policy",
]


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


def validate_payload(path: Path) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"missing Slack alert payload: {path}"]

    payload = load_json(path)
    schema = load_json(SCHEMA_PATH)
    failures.extend(validate_json_schema(payload, schema, "slack-alert-payload"))

    searchable_text = "\n".join(_string_values(payload))
    for label, pattern in BLOCKED_VALUE_PATTERNS.items():
        if pattern.search(searchable_text):
            failures.append(f"{path}: blocked value marker `{label}`")

    delivery = payload.get("delivery", {})
    if delivery.get("destination") != "slack_incoming_webhook":
        failures.append("delivery.destination must be slack_incoming_webhook")
    if delivery.get("webhook_variable") != "OPRS_ALERT_WEBHOOK_URL":
        failures.append("delivery.webhook_variable must be OPRS_ALERT_WEBHOOK_URL")
    if delivery.get("webhook_url_committed") is not False:
        failures.append("delivery.webhook_url_committed must be false")

    source_event = payload.get("source_event", {})
    if source_event.get("service_name") != "oprs-readonly-worker":
        failures.append("source_event.service_name must be oprs-readonly-worker")
    if source_event.get("public_output_published") is not False:
        failures.append("source_event.public_output_published must be false")

    invariants = payload.get("safety_invariants", {})
    for key in FALSE_INVARIANTS:
        if invariants.get(key) is not False:
            failures.append(f"safety_invariants.{key} must be false")

    return failures


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PATH
    failures = validate_payload(path)
    if failures:
        print("Slack alert payload validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"PASS Slack alert payload: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
