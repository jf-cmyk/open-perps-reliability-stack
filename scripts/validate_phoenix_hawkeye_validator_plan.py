#!/usr/bin/env python3
"""Validate the Phoenix/Hawkeye validator-plan contract stays non-executing."""

from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

from public_package_contract import load_json, scan_blocked_text, validate_json_schema


PLAN_PATH = Path("examples/datasets/phoenix_hawkeye_validator_plan_example.json")
SCHEMA_PATH = Path("schemas/datasets/phoenix-hawkeye-validator-plan-v0.json")

EXPECTED = {
    "rise_public_commit": "09f59aaf06037ecff395a6c47eea7440f9eef7c2",
    "source_phoenix_commit": "6051225fb045fbb5b6a454bd445e7fc2e31e5722",
    "production_program_id": "EtrnLzgbS7nMMy5fbD42kXiUzGg8XQzJ972Xtk1cjWih",
    "production_log_authority": "GdxfTLSsdSY37G6fZoYtdGDSfgFnbT2EmRpuePZxWShS",
    "production_global_configuration": "2zskx2iyCvb6Stg7RBZkt1f6MrF4dpYtMG3yMvKwqtUZ",
    "hawkeye_program_id": "RiSeVw3ZjNfsaXPRb4mgaqYaEEt41pNNJoDvVh7pgQj",
    "hawkeye_return_version": 1,
}
BETA_PROGRAM_ID = "phDEVv4w6BcfkLrLNeXr8HhhgQxnxziVGXpGPcaadMf"


def validate_plan(plan: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    source = plan.get("source_authority", {})
    for key, expected in EXPECTED.items():
        if source.get(key) != expected:
            failures.append(f"source_authority.{key} mismatch")
    if source.get("production_program_id") == BETA_PROGRAM_ID:
        failures.append("production_program_id must not be the beta Phoenix program")

    scope = plan.get("validator_scope", {})
    required_views = {"margin", "asset", "liquidation_price", "bbo", "funding"}
    if set(scope.get("covered_views", [])) != required_views:
        failures.append("validator_scope.covered_views must cover all planned Hawkeye views")
    for key in [
        "account_level_decode_claimed",
        "exact_oracle_input_identity_claimed",
        "liquidation_replay_claimed",
        "instruction_builder_claimed",
        "transaction_submission_claimed",
    ]:
        if scope.get(key) is not False:
            failures.append(f"validator_scope.{key} must be false")

    scrub = plan.get("scrub_policy", {})
    for key in [
        "raw_account_data_committed",
        "raw_return_data_committed",
        "trader_addresses_committed",
        "credential_material_committed",
    ]:
        if scrub.get(key) is not False:
            failures.append(f"scrub_policy.{key} must be false")
    if scrub.get("scrubbed_fixture_shapes_allowed") is not True:
        failures.append("scrub_policy.scrubbed_fixture_shapes_allowed must be true")

    readiness = plan.get("readiness", {})
    if readiness.get("source_constants_pinned") is not True:
        failures.append("readiness.source_constants_pinned must be true")
    for key in [
        "local_validator_implemented",
        "public_regression_fixtures_available",
        "account_decode_ready",
        "replay_ready",
        "execution_ready",
    ]:
        if readiness.get(key) is not False:
            failures.append(f"readiness.{key} must remain false until implemented and scrubbed")

    gates = {item.get("gate"): item.get("status") for item in plan.get("promotion_gates", [])}
    for gate in ["exact oracle input identity verified", "account-level decode promoted"]:
        if gates.get(gate) != "blocked":
            failures.append(f"promotion gate '{gate}' must stay blocked")

    return failures


def run_self_tests(plan: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    beta_plan = deepcopy(plan)
    beta_plan["source_authority"]["production_program_id"] = BETA_PROGRAM_ID
    if not any("beta" in failure for failure in validate_plan(beta_plan)):
        failures.append("self-test expected beta program rejection")

    raw_plan = deepcopy(plan)
    raw_plan["scrub_policy"]["raw_return_data_committed"] = True
    if not any("raw_return_data_committed" in failure for failure in validate_plan(raw_plan)):
        failures.append("self-test expected raw return data rejection")

    replay_plan = deepcopy(plan)
    replay_plan["readiness"]["replay_ready"] = True
    if not any("replay_ready" in failure for failure in validate_plan(replay_plan)):
        failures.append("self-test expected replay_ready rejection")

    return failures


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else PLAN_PATH
    failures: list[str] = []
    for required in [path, SCHEMA_PATH]:
        if not required.exists():
            failures.append(f"missing required file: {required}")
    if failures:
        return fail(failures)

    plan = load_json(path)
    schema = load_json(SCHEMA_PATH)
    failures.extend(validate_json_schema(plan, schema, "phoenix-hawkeye-validator-plan"))
    failures.extend(scan_blocked_text(path, path.read_text(encoding="utf-8")))
    failures.extend(validate_plan(plan))
    failures.extend(run_self_tests(plan))
    if failures:
        return fail(failures)

    print(f"PASS Phoenix/Hawkeye validator plan: {path}")
    return 0


def fail(failures: list[str]) -> int:
    print("Phoenix/Hawkeye validator-plan validation failed:", file=sys.stderr)
    for failure in failures:
        print(f"- {failure}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
