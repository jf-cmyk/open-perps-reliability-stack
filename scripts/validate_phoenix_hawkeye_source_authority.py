#!/usr/bin/env python3
"""Validate Phoenix/Rise Hawkeye source-authority evidence stays bounded."""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any


SOURCE_REVIEW_PATH = Path("examples/datasets/phoenix_hawkeye_source_review_example.json")
SOURCE_DOC_PATH = Path("docs/phoenix-source-authority.md")
RESEARCH_STATE_PATH = Path("research/solana-ecosystem/state.json")

EXPECTED = {
    "pinned_commit": "09f59aaf06037ecff395a6c47eea7440f9eef7c2",
    "source_phoenix_commit": "6051225fb045fbb5b6a454bd445e7fc2e31e5722",
    "production_program_id": "EtrnLzgbS7nMMy5fbD42kXiUzGg8XQzJ972Xtk1cjWih",
    "beta_program_id": "phDEVv4w6BcfkLrLNeXr8HhhgQxnxziVGXpGPcaadMf",
    "production_log_authority": "GdxfTLSsdSY37G6fZoYtdGDSfgFnbT2EmRpuePZxWShS",
    "production_global_configuration": "2zskx2iyCvb6Stg7RBZkt1f6MrF4dpYtMG3yMvKwqtUZ",
    "ember_program_id": "EMBERpYNE6ehWmXymZZS2skiFmCa9V5dp14e1iduM5qy",
    "flight_program_id": "F1ightu9cujFYo34k9CabifLrJT8qzfDVM2Q7BqhJn2W",
    "hawkeye_program_id": "RiSeVw3ZjNfsaXPRb4mgaqYaEEt41pNNJoDvVh7pgQj",
    "hawkeye_return_version": 1,
}

REQUIRED_BLOCKED_DOC_MARKERS = [
    "does not authorize order placement",
    "signing",
    "custody",
    "capital deployment",
    "production execution",
    "Claims that Phoenix account-level decode, liquidation replay, trader monitoring, or historical reconstruction is ready.",
    "Claims that the beta address is the production program.",
    "Claims that Flight routing, builder registration, referral activation, or invite activation are part of the grant MVP.",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_record(record: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if record.get("review_kind") != "phoenix_hawkeye_source_authority":
        failures.append("review_kind must be phoenix_hawkeye_source_authority")
    if record.get("protocol") != "phoenix_rise":
        failures.append("protocol must be phoenix_rise")
    if record.get("approval_status") != "pending":
        failures.append("approval_status must remain pending until a local validator and scrubbed fixture exist")

    source = record.get("source_authority", {})
    if source.get("status") != "pinned_source_reviewed":
        failures.append("source_authority.status must be pinned_source_reviewed")
    if source.get("program_id") != EXPECTED["production_program_id"]:
        failures.append("source_authority.program_id must be the production Phoenix/Rise program")
    if source.get("program_id") == EXPECTED["beta_program_id"]:
        failures.append("source_authority.program_id must not be the beta Phoenix/Rise program")
    if source.get("pinned_commit") != EXPECTED["pinned_commit"]:
        failures.append("source_authority.pinned_commit changed unexpectedly")
    if source.get("confirmation_required") is not False:
        failures.append("source_authority.confirmation_required must be false for source-pinned planning")

    gates = record.get("approval_gates", {})
    for key in ["canonical_source_confirmed", "discriminator_confirmed", "local_validator_required", "local_only_until_scrubbed"]:
        if gates.get(key) is not True:
            failures.append(f"approval_gates.{key} must be true")
    for key in [
        "account_size_confirmed",
        "offsets_confirmed",
        "enum_encoding_confirmed",
        "pda_seeds_confirmed",
        "instruction_roles_confirmed",
        "public_regression_fixtures_available",
    ]:
        if gates.get(key) is not False:
            failures.append(f"approval_gates.{key} must remain false until account-level validation lands")

    for claim, value in record.get("forbidden_claims", {}).items():
        if value is not False:
            failures.append(f"forbidden_claims.{claim} must be false")

    return failures


def validate_doc(text: str) -> list[str]:
    failures: list[str] = []
    for key, expected in EXPECTED.items():
        if str(expected) not in text:
            failures.append(f"{SOURCE_DOC_PATH}: missing expected {key}: {expected}")
    for marker in REQUIRED_BLOCKED_DOC_MARKERS:
        if marker not in text:
            failures.append(f"{SOURCE_DOC_PATH}: missing blocked marker: {marker}")
    return failures


def validate_research_state(state: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    phoenix = state.get("protocol_baselines", {}).get("phoenix_external_asset_perps", {})
    expected_fields = {
        "rise_public_commit": EXPECTED["pinned_commit"],
        "source_phoenix_commit_named_by_release": EXPECTED["source_phoenix_commit"],
        "production_program_id": EXPECTED["production_program_id"],
        "beta_program_id": EXPECTED["beta_program_id"],
        "production_log_authority": EXPECTED["production_log_authority"],
        "production_global_configuration": EXPECTED["production_global_configuration"],
        "hawkeye_program_id": EXPECTED["hawkeye_program_id"],
        "hawkeye_return_version": EXPECTED["hawkeye_return_version"],
        "flight_program_id": EXPECTED["flight_program_id"],
    }
    for field, expected in expected_fields.items():
        if phoenix.get(field) != expected:
            failures.append(f"{RESEARCH_STATE_PATH}: phoenix_external_asset_perps.{field} mismatch")
    if phoenix.get("account_decode_status") != "blocked_pending_local_validator_and_scrubbed_fixtures":
        failures.append(f"{RESEARCH_STATE_PATH}: account_decode_status must stay blocked")
    if phoenix.get("exact_oracle_input_identity_status") != "unverified":
        failures.append(f"{RESEARCH_STATE_PATH}: exact_oracle_input_identity_status must stay unverified")
    return failures


def run_self_tests(record: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    beta_record = deepcopy(record)
    beta_record["source_authority"]["program_id"] = EXPECTED["beta_program_id"]
    if not any("beta" in failure for failure in validate_record(beta_record)):
        failures.append("self-test expected beta program rejection")

    execution_record = deepcopy(record)
    execution_record["forbidden_claims"]["execution_claimed"] = True
    if not any("execution_claimed" in failure for failure in validate_record(execution_record)):
        failures.append("self-test expected execution_claimed rejection")

    approved_record = deepcopy(record)
    approved_record["approval_status"] = "approved"
    if not any("approval_status" in failure for failure in validate_record(approved_record)):
        failures.append("self-test expected premature approval rejection")

    return failures


def main() -> int:
    failures: list[str] = []
    for path in [SOURCE_REVIEW_PATH, SOURCE_DOC_PATH, RESEARCH_STATE_PATH]:
        if not path.exists():
            failures.append(f"missing required file: {path}")
    if failures:
        return fail(failures)

    record = load_json(SOURCE_REVIEW_PATH)
    state = load_json(RESEARCH_STATE_PATH)
    doc_text = SOURCE_DOC_PATH.read_text(encoding="utf-8")

    failures.extend(validate_record(record))
    failures.extend(validate_doc(doc_text))
    failures.extend(validate_research_state(state))
    failures.extend(run_self_tests(record))
    if failures:
        return fail(failures)

    print("PASS Phoenix/Hawkeye source authority")
    return 0


def fail(failures: list[str]) -> int:
    print("Phoenix/Hawkeye source-authority validation failed:", file=sys.stderr)
    for failure in failures:
        print(f"- {failure}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
