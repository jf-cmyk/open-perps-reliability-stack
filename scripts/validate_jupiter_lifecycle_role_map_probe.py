#!/usr/bin/env python3
"""Validate a Jupiter lifecycle role-map probe output."""

from __future__ import annotations

import sys
from pathlib import Path

from public_package_contract import load_json, validate_json_schema


DEFAULT_PATH = Path("examples/datasets/jupiter_lifecycle_role_map_probe_example.json")


def validate_probe(path: Path) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"missing Jupiter lifecycle role-map probe: {path}"]

    report = load_json(path)
    schema = load_json(Path("schemas/datasets/jupiter-lifecycle-role-map-probe-v0.json"))
    failures.extend(validate_json_schema(report, schema, "jupiter-lifecycle-role-map-probe"))

    readiness = report.get("readiness", {})
    false_claims = [
        "verified_request_fulfillment_pair_claimed",
        "position_request_state_transition_claimed",
        "keeper_semantics_claimed",
        "liquidation_replay_claimed",
        "execution_claimed",
        "raw_transaction_committed",
        "raw_instruction_data_committed",
        "raw_account_bytes_committed",
        "account_pubkeys_committed",
    ]
    for key in false_claims:
        if readiness.get(key) is not False:
            failures.append(f"readiness.{key} must be false")

    if readiness.get("instruction_account_role_maps_from_idl") is not True:
        failures.append("readiness.instruction_account_role_maps_from_idl must be true")

    for index, observation in enumerate(report.get("role_map_observations", [])):
        label = observation.get("observation_id") or f"index-{index}"
        if observation.get("raw_instruction_data_committed") is not False:
            failures.append(f"{label}: raw_instruction_data_committed must be false")
        if observation.get("raw_transaction_committed") is not False:
            failures.append(f"{label}: raw_transaction_committed must be false")
        if observation.get("matched_onchain_idl_instruction") is True:
            if not observation.get("instruction_name") or observation.get("instruction_name") == "unknown":
                failures.append(f"{label}: matched instruction must have a concrete instruction_name")
            if observation.get("bound_role_count", 0) <= 0:
                failures.append(f"{label}: matched instruction must bind at least one role")
        for role in observation.get("role_bindings", []):
            if "observed_pubkey" in role:
                failures.append(f"{label}: role binding must not publish observed_pubkey")
            if "owner" in role and "observed_owner_hash" not in role:
                failures.append(f"{label}: role binding must hash owner values")

    summary = report.get("instruction_summary", {})
    observations = report.get("role_map_observations", [])
    if summary.get("jupiter_instruction_observation_count") != len(observations):
        failures.append(
            "instruction_summary.jupiter_instruction_observation_count must match role_map_observations length"
        )

    return failures


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PATH
    failures = validate_probe(path)
    if failures:
        print("Jupiter lifecycle role-map probe validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"PASS Jupiter lifecycle role-map probe: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
