#!/usr/bin/env python3
"""Run non-served invalid public-package fixture cases."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import validate_public_contract_index
import validate_public_guardrail_package
import validate_public_jupiter_authority_gap


CASES_PATH = Path("tests/fixtures/public-packages/invalid/cases.json")
TARGET_DIR = Path("target/invalid-public-package-fixtures")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def copy_package(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def run_case(case: dict[str, str]) -> list[str]:
    case_id = case["case_id"]
    validator = case["validator"]
    mutation = case["mutation"]
    expected_failure = case["expected_failure"]
    workspace = TARGET_DIR / case_id
    workspace.parent.mkdir(parents=True, exist_ok=True)

    if validator == "drift_guardrails":
        copy_package(Path("examples/public/drift-guardrails-v0"), workspace)
        mutate_drift_package(workspace, mutation)
        failures = validate_public_guardrail_package.validate_package(workspace, None)
    elif validator == "jupiter_authority_gap":
        copy_package(Path("examples/public/jupiter-authority-gap-v0"), workspace)
        mutate_jupiter_package(workspace, mutation)
        failures = validate_public_jupiter_authority_gap.validate_package(workspace)
    elif validator == "contract_index":
        workspace.mkdir(parents=True, exist_ok=True)
        index_path = workspace / "contract-index.json"
        index = load_json(Path("examples/public/contract-index.json"))
        mutate_contract_index(index, mutation)
        write_json(index_path, index)
        failures = validate_public_contract_index.validate_index(index_path)
    else:
        return [f"{case_id}: unknown validator `{validator}`"]

    if not failures:
        return [f"{case_id}: invalid fixture unexpectedly passed"]
    if not any(expected_failure in failure for failure in failures):
        return [
            f"{case_id}: expected failure containing `{expected_failure}`, got {failures}"
        ]
    return []


def mutate_drift_package(package_dir: Path, mutation: str) -> None:
    if mutation == "set_spot_replay_ready_true":
        payload_path = package_dir / "spot_guardrails.json"
        payload = load_json(payload_path)
        payload["readiness"]["replay_ready"] = True
        write_json(payload_path, payload)
        return
    if mutation == "add_raw_account_bytes_marker":
        payload_path = package_dir / "perp_guardrails.json"
        payload = load_json(payload_path)
        payload["raw_account_bytes"] = "AAECAwQ="
        write_json(payload_path, payload)
        return
    if mutation == "set_manifest_checksum_invalid":
        manifest_path = package_dir / "manifest.json"
        manifest = load_json(manifest_path)
        manifest["outputs"][0]["sha256"] = "0" * 64
        write_json(manifest_path, manifest)
        return
    if mutation == "add_manifest_absolute_path":
        manifest_path = package_dir / "manifest.json"
        manifest = load_json(manifest_path)
        manifest.setdefault("known_limitations", []).append(
            "/Users/example/private/source-cache"
        )
        write_json(manifest_path, manifest)
        return
    if mutation == "remove_spot_required_asset":
        payload_path = package_dir / "spot_guardrails.json"
        payload = load_json(payload_path)
        payload["records"][0].pop("asset", None)
        write_json(payload_path, payload)
        return
    raise ValueError(f"unknown Drift mutation `{mutation}`")


def mutate_jupiter_package(package_dir: Path, mutation: str) -> None:
    payload_path = package_dir / "gap_report.json"
    payload = load_json(payload_path)
    if mutation == "set_verified_pairing_true":
        payload["readiness"]["verified_pairing_claimed"] = True
    elif mutation == "set_record_status_verified":
        payload["records"][0]["status"] = "verified"
    elif mutation == "add_rpc_url_evidence_ref":
        payload["records"][0]["public_evidence_refs"].append(
            "https://mainnet.helius-rpc.com/?api-key=secret"
        )
    elif mutation == "add_bearer_token_marker":
        payload.setdefault("known_gaps", []).append("Bearer secret-token")
    elif mutation == "add_absolute_evidence_ref":
        payload["records"][0]["public_evidence_refs"].append(
            "/Users/example/private/jupiter-source.json"
        )
    elif mutation == "add_record_extra_property":
        payload["records"][0]["decoded"] = True
    else:
        raise ValueError(f"unknown Jupiter mutation `{mutation}`")
    write_json(payload_path, payload)


def mutate_contract_index(index: dict[str, Any], mutation: str) -> None:
    if mutation == "set_contract_payload_schema_version_invalid":
        index["packages"][0]["payloads"][0]["schema_version"] = "oprs.invalid_schema.v0"
        return
    if mutation == "duplicate_first_package":
        index["packages"].append(dict(index["packages"][0]))
        return
    if mutation == "set_validator_missing":
        index["packages"][0]["validator"] = "scripts/missing_validator.py"
        return
    if mutation == "set_schema_path_missing":
        index["packages"][0]["payloads"][0]["schema_path"] = (
            "schemas/datasets/missing-schema.json"
        )
        return
    if mutation == "set_manifest_path_missing":
        index["packages"][0]["manifest_path"] = (
            "examples/public/drift-guardrails-v0/missing-manifest.json"
        )
        return
    raise ValueError(f"unknown contract-index mutation `{mutation}`")


def main() -> int:
    fixture = load_json(CASES_PATH)
    failures: list[str] = []
    for case in fixture.get("cases", []):
        failures.extend(run_case(case))
    if failures:
        print("Invalid public-package fixture validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"PASS invalid public-package fixtures: {CASES_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
