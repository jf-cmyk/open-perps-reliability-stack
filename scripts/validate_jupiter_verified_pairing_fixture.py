#!/usr/bin/env python3
"""Validate Jupiter verified-pairing fixture contracts.

The synthetic positive fixture can prove validator behavior only. It must not
be treated as a mainnet lifecycle pairing claim.
"""

from __future__ import annotations

import sys
import re
from pathlib import Path
from typing import Any

from public_package_contract import load_json, validate_json_schema


DEFAULT_PATHS = [
    Path("examples/datasets/jupiter_verified_pairing_rejected_fixture.json"),
    Path("examples/datasets/jupiter_verified_pairing_synthetic_positive_fixture.json"),
]
SCHEMA_PATH = Path("schemas/datasets/jupiter-verified-pairing-fixture-v0.json")
REQUIRED_FORBIDDEN_ACTIONS = {
    "sign",
    "submit_transaction",
    "retry_transaction",
    "bid_priority_fee",
    "load_keypair",
    "manage_custody",
    "manage_capital",
}
BLOCKED_VALUE_PATTERNS = {
    "rpc_url": re.compile(r"https://[^\"'\s]*(helius|rpc|api-key|apikey)[^\"'\s]*", re.IGNORECASE),
    "slack_webhook": re.compile(r"https://hooks\.slack(?:-gov)?\.com/services/[a-z0-9/_-]+", re.IGNORECASE),
    "bearer_token": re.compile(r"bearer\s+[a-z0-9._-]+", re.IGNORECASE),
    "local_path": re.compile(r"/Users/|/Volumes/|/private/"),
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


def validate_fixture(path: Path) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"missing Jupiter verified-pairing fixture: {path}"]

    fixture = load_json(path)
    schema = load_json(SCHEMA_PATH)
    failures.extend(validate_json_schema(fixture, schema, "jupiter-verified-pairing-fixture"))

    searchable_text = "\n".join(_string_values(fixture))
    for label, pattern in BLOCKED_VALUE_PATTERNS.items():
        if pattern.search(searchable_text):
            failures.append(f"{path}: blocked value marker `{label}`")

    source = fixture.get("source_authority", {})
    query = fixture.get("query", {})
    candidate = fixture.get("pairing_candidate", {})
    readiness = fixture.get("readiness", {})
    forbidden_actions = set(fixture.get("forbidden_actions", []))

    missing_forbidden = sorted(REQUIRED_FORBIDDEN_ACTIONS - forbidden_actions)
    if missing_forbidden:
        failures.append(f"{path}: forbidden_actions missing {missing_forbidden}")

    for key in [
        "raw_transaction_committed",
        "raw_instruction_data_committed",
        "raw_account_bytes_committed",
        "account_pubkeys_committed",
    ]:
        if query.get(key) is not False:
            failures.append(f"{path}: query.{key} must be false")

    for key in [
        "mainnet_verified_pairing_claimed",
        "position_request_state_transition_claimed",
        "keeper_semantics_claimed",
        "liquidation_replay_claimed",
        "execution_claimed",
        "public_claims_allowed",
    ]:
        if readiness.get(key) is not False:
            failures.append(f"{path}: readiness.{key} must be false")

    classification = candidate.get("classification")
    if classification == "verified_pair":
        if readiness.get("synthetic_fixture") is not True:
            failures.append(f"{path}: verified_pair is allowed only for synthetic_fixture=true")
        if candidate.get("confidence") != "high":
            failures.append(f"{path}: verified_pair requires confidence=high")
        if source.get("onchain_idl_hash_present") is not True:
            failures.append(f"{path}: verified_pair requires onchain_idl_hash_present=true")
        if source.get("jupiter_confirmed_lifecycle_artifact_present") is not True:
            failures.append(
                f"{path}: verified_pair requires jupiter_confirmed_lifecycle_artifact_present=true"
            )
        for key in [
            "role_bindings_include_request",
            "role_bindings_include_fulfillment_target",
            "pre_state_slot_present",
            "post_state_slot_present",
            "source_reviewed_transition_fields_present",
            "owner_checks_passed",
            "discriminator_checks_passed",
        ]:
            if candidate.get(key) is not True:
                failures.append(f"{path}: verified_pair requires pairing_candidate.{key}=true")
        if candidate.get("rejection_reasons"):
            failures.append(f"{path}: verified_pair must not include rejection_reasons")

    if classification in {"candidate_pair", "rejected_pair"}:
        if readiness.get("synthetic_fixture") is True:
            failures.append(f"{path}: synthetic_fixture=true should exercise verified_pair gates")
        if classification == "rejected_pair" and not candidate.get("rejection_reasons"):
            failures.append(f"{path}: rejected_pair must explain rejection_reasons")

    return failures


def main() -> int:
    paths = [Path(arg) for arg in sys.argv[1:]] or DEFAULT_PATHS
    failures: list[str] = []
    for path in paths:
        failures.extend(validate_fixture(path))
    if failures:
        print("Jupiter verified-pairing fixture validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    for path in paths:
        print(f"PASS Jupiter verified-pairing fixture: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
