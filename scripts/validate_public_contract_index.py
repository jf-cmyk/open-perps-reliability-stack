#!/usr/bin/env python3
"""Validate the public dataset contract index."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_INDEX = Path("examples/public/contract-index.json")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def is_safe_relative_path(path: str) -> bool:
    candidate = Path(path)
    return bool(path) and not candidate.is_absolute() and ".." not in candidate.parts


def validate_index(index_path: Path) -> list[str]:
    failures: list[str] = []
    if not index_path.exists():
        return [f"missing contract index: {index_path}"]

    index = load_json(index_path)
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


def main() -> int:
    index_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INDEX
    failures = validate_index(index_path)
    if failures:
        print("Public contract index validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"PASS public contract index: {index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
