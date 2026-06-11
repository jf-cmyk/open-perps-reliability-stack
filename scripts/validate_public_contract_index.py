#!/usr/bin/env python3
"""Validate the public dataset contract index."""

from __future__ import annotations

import sys
from pathlib import Path

from public_package_contract import is_safe_relative_path, load_json, validate_json_schema


DEFAULT_INDEX = Path("examples/public/contract-index.json")


def validate_index(index_path: Path) -> list[str]:
    failures: list[str] = []
    if not index_path.exists():
        return [f"missing contract index: {index_path}"]

    index = load_json(index_path)
    schema = load_json(Path("schemas/datasets/public-contract-index-v0.json"))
    failures.extend(validate_json_schema(index, schema, "contract-index"))

    if index.get("contract_index_version") != "oprs.public_contract_index.v0":
        failures.append("contract_index_version must be oprs.public_contract_index.v0")

    packages = index.get("packages", [])
    if not isinstance(packages, list) or not packages:
        failures.append("packages must be a non-empty array")
        return failures

    seen_package_ids: set[str] = set()
    for package in packages:
        package_id = package.get("package_id", "")
        if package_id in seen_package_ids:
            failures.append(f"duplicate package_id: {package_id}")
        seen_package_ids.add(package_id)

        if package.get("capability") != "read_only_dry_run":
            failures.append(f"{package_id}: capability must be read_only_dry_run")
        if package.get("publishable") is not True:
            failures.append(f"{package_id}: publishable must be true")

        for key in ["manifest_path", "dq_path", "validator"]:
            value = package.get(key, "")
            if not is_safe_relative_path(value):
                failures.append(f"{package_id}: {key} must be a safe relative path")
            elif not Path(value).exists():
                failures.append(f"{package_id}: {key} does not exist: {value}")

        validator_path = Path(package.get("validator", ""))
        if validator_path.exists() and not validator_path.stat().st_mode & 0o111:
            failures.append(f"{package_id}: validator is not executable: {validator_path}")

        boundary = package.get("claim_boundary", {})
        allowed_claims = boundary.get("allowed_claims", [])
        blocked_claims = boundary.get("blocked_claims", [])
        if not allowed_claims:
            failures.append(f"{package_id}: claim_boundary.allowed_claims must be non-empty")
        if not blocked_claims:
            failures.append(f"{package_id}: claim_boundary.blocked_claims must be non-empty")
        blocked_text = " ".join(blocked_claims).lower()
        for required in ["signing", "transaction submission"]:
            if required not in blocked_text:
                failures.append(f"{package_id}: blocked_claims must include `{required}`")

        payload_roles: set[str] = set()
        for payload in package.get("payloads", []):
            role = payload.get("role", "")
            if role in payload_roles:
                failures.append(f"{package_id}: duplicate payload role: {role}")
            payload_roles.add(role)

            for key in ["path", "schema_path"]:
                value = payload.get(key, "")
                if not is_safe_relative_path(value):
                    failures.append(f"{package_id}/{role}: {key} must be a safe relative path")
                elif not Path(value).exists():
                    failures.append(f"{package_id}/{role}: {key} does not exist: {value}")

            payload_path = Path(payload.get("path", ""))
            if payload_path.exists():
                payload_json = load_json(payload_path)
                if payload_json.get("schema_version") != payload.get("schema_version"):
                    failures.append(
                        f"{package_id}/{role}: payload schema_version mismatch"
                    )

    return failures


def run_self_tests() -> list[str]:
    failures: list[str] = []
    index = load_json(DEFAULT_INDEX)
    packages = index["packages"]
    original = packages[0]["payloads"][0]["schema_version"]
    packages[0]["payloads"][0]["schema_version"] = "oprs.invalid_schema.v0"
    tmp_path = Path("target/contract-index-negative-self-test.json")
    tmp_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json_dumps(index), encoding="utf-8")
    observed = validate_index(tmp_path)
    packages[0]["payloads"][0]["schema_version"] = original
    try:
        tmp_path.unlink()
    except FileNotFoundError:
        pass
    if not any("payload schema_version mismatch" in failure for failure in observed):
        failures.append("self-test expected payload schema_version mismatch")
    return failures


def json_dumps(value: object) -> str:
    import json

    return json.dumps(value, indent=2, sort_keys=True)


def main() -> int:
    index_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INDEX
    failures = validate_index(index_path)
    if len(sys.argv) == 1:
        failures.extend(run_self_tests())
    if failures:
        print("Public contract index validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"PASS public contract index: {index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
