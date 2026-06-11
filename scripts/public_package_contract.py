"""Shared offline helpers for public proof-pack package validators."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_CONTRACT_INDEX = Path("examples/public/contract-index.json")

BLOCKED_PATTERNS = {
    "rpc_url": re.compile(r"https://[^\"'\s]*(helius|rpc|api-key|apikey)[^\"'\s]*", re.IGNORECASE),
    "env_file": re.compile(r"(^|[/:])\.env(\b|$)"),
    "local_path": re.compile(r"/Users/|/Volumes/|/private/"),
    "bearer_token": re.compile(r"bearer\s+[a-z0-9._-]+", re.IGNORECASE),
    "private_key": re.compile(r"private[_ -]?key|seed phrase|keypair|wallet secret", re.IGNORECASE),
    "custody_or_capital": re.compile(r"custody|capital allocation|capital_limit|inventory", re.IGNORECASE),
    "raw_payload": re.compile(r"raw_account_bytes|account_data_base64|raw_bytes", re.IGNORECASE),
    "user_state_claim": re.compile(r"user_position|user_account|margin_health|liquidation_opportunity", re.IGNORECASE),
    "execution_claim": re.compile(r"submit_transaction|priority_fee_bid|capital_limit|wallet_inventory", re.IGNORECASE),
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_safe_relative_path(path: str) -> bool:
    candidate = Path(path)
    return bool(path) and not candidate.is_absolute() and ".." not in candidate.parts


def scan_blocked_text(path: Path, text: str) -> list[str]:
    failures = []
    for label, pattern in BLOCKED_PATTERNS.items():
        if pattern.search(text):
            failures.append(f"{path}: blocked marker `{label}`")
    return failures


def validate_json_schema(instance: Any, schema: dict[str, Any], label: str) -> list[str]:
    """Validate the bounded JSON Schema subset used by checked-in package schemas."""

    return _validate_schema_node(instance, schema, schema, label)


def _validate_schema_node(
    instance: Any,
    schema: dict[str, Any],
    root_schema: dict[str, Any],
    path: str,
) -> list[str]:
    failures: list[str] = []

    if "$ref" in schema:
        ref = schema["$ref"]
        if not isinstance(ref, str) or not ref.startswith("#/$defs/"):
            return [f"{path}: unsupported schema ref {ref!r}"]
        def_name = ref.removeprefix("#/$defs/")
        target = root_schema.get("$defs", {}).get(def_name)
        if not isinstance(target, dict):
            return [f"{path}: missing schema ref {ref}"]
        return _validate_schema_node(instance, target, root_schema, path)

    if "not" in schema and _schema_matches(instance, schema["not"], root_schema):
        failures.append(f"{path}: must not match forbidden schema")

    if "anyOf" in schema:
        options = schema["anyOf"]
        if not isinstance(options, list) or not any(
            _schema_matches(instance, option, root_schema)
            for option in options
            if isinstance(option, dict)
        ):
            failures.append(f"{path}: must match at least one anyOf schema")

    if "const" in schema and instance != schema["const"]:
        failures.append(f"{path}: expected const {schema['const']!r}, got {instance!r}")

    if "enum" in schema and instance not in schema["enum"]:
        failures.append(f"{path}: value {instance!r} not in enum {schema['enum']!r}")

    expected_type = schema.get("type")
    if expected_type is not None and not _matches_json_type(instance, expected_type):
        failures.append(f"{path}: expected type {expected_type}, got {_json_type_name(instance)}")
        return failures

    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            failures.append(f"{path}: length must be >= {schema['minLength']}")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            failures.append(f"{path}: length must be <= {schema['maxLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            failures.append(f"{path}: does not match pattern {schema['pattern']!r}")

    if isinstance(instance, int) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            failures.append(f"{path}: value must be >= {schema['minimum']}")

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            failures.append(f"{path}: item count must be >= {schema['minItems']}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(instance):
                failures.extend(
                    _validate_schema_node(item, item_schema, root_schema, f"{path}[{index}]")
                )

    if isinstance(instance, dict):
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        if isinstance(required, list):
            for key in required:
                if key not in instance:
                    failures.append(f"{path}: missing required property `{key}`")

        if isinstance(properties, dict):
            for key, property_schema in properties.items():
                if key in instance and isinstance(property_schema, dict):
                    failures.extend(
                        _validate_schema_node(
                            instance[key], property_schema, root_schema, f"{path}.{key}"
                        )
                    )

            if schema.get("additionalProperties") is False:
                extra = sorted(key for key in instance if key not in properties)
                for key in extra:
                    failures.append(f"{path}: additional property `{key}` is not allowed")

    return failures


def _schema_matches(instance: Any, schema: dict[str, Any], root_schema: dict[str, Any]) -> bool:
    return not _validate_schema_node(instance, schema, root_schema, "<match>")


def _matches_json_type(value: Any, expected_type: str) -> bool:
    if expected_type == "object":
        return isinstance(value, dict)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "boolean":
        return isinstance(value, bool)
    return False


def _json_type_name(value: Any) -> str:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    if isinstance(value, str):
        return "string"
    if isinstance(value, int):
        return "integer"
    if value is None:
        return "null"
    return type(value).__name__


def load_contract_entry(
    package_id: str,
    expected_validator: str,
    index_path: Path = DEFAULT_CONTRACT_INDEX,
) -> tuple[dict[str, Any] | None, list[str]]:
    failures: list[str] = []
    if not index_path.exists():
        return None, [f"missing contract index: {index_path}"]

    index = load_json(index_path)
    if index.get("contract_index_version") != "oprs.public_contract_index.v0":
        failures.append("contract index version must be oprs.public_contract_index.v0")

    packages = index.get("packages", [])
    if not isinstance(packages, list):
        failures.append("contract index packages must be an array")
        return None, failures

    matches = [package for package in packages if package.get("package_id") == package_id]
    if len(matches) != 1:
        failures.append(f"contract index must contain exactly one `{package_id}` package")
        return None, failures

    entry = matches[0]
    if entry.get("capability") != "read_only_dry_run":
        failures.append(f"{package_id}: capability must be read_only_dry_run")
    if entry.get("publishable") is not True:
        failures.append(f"{package_id}: publishable must be true")
    if entry.get("validator") != expected_validator:
        failures.append(f"{package_id}: validator must point to {expected_validator}")

    boundary = entry.get("claim_boundary", {})
    if not boundary.get("allowed_claims") or not boundary.get("blocked_claims"):
        failures.append(f"{package_id}: claim_boundary must include allowed_claims and blocked_claims")

    for key in ["manifest_path", "dq_path", "validator"]:
        value = entry.get(key, "")
        if not is_safe_relative_path(value):
            failures.append(f"{package_id}: {key} must be a safe relative path")
        elif key != "validator" and not Path(value).exists():
            failures.append(f"{package_id}: {key} does not exist: {value}")

    for payload in entry.get("payloads", []):
        for key in ["path", "schema_path"]:
            value = payload.get(key, "")
            if not is_safe_relative_path(value):
                failures.append(f"{package_id}: payload {key} must be a safe relative path")
            elif not Path(value).exists():
                failures.append(f"{package_id}: payload {key} does not exist: {value}")

    return entry, failures


def validate_manifest_dq_and_outputs(
    *,
    package_dir: Path,
    manifest: dict[str, Any],
    dq: dict[str, Any],
    row_counts_by_output_path: dict[str, int],
) -> list[str]:
    failures: list[str] = []
    if manifest.get("capability") != "read_only_dry_run":
        failures.append("manifest capability must be read_only_dry_run")
    if manifest.get("scrub", {}).get("status") != "passed":
        failures.append("manifest scrub.status must be passed")
    if manifest.get("dq", {}).get("blocking_failures") != 0:
        failures.append("manifest dq.blocking_failures must be 0")

    output_specs = manifest.get("outputs", [])
    for output in output_specs:
        relative_path = output.get("path")
        if not relative_path:
            failures.append("manifest output missing path")
            continue
        output_path = package_dir / relative_path
        if not output_path.exists():
            failures.append(f"manifest output missing file: {relative_path}")
            continue
        observed_sha = sha256_file(output_path)
        if observed_sha != output.get("sha256"):
            failures.append(f"{relative_path} sha256 mismatch: {observed_sha}")
        if relative_path in row_counts_by_output_path:
            observed_rows = row_counts_by_output_path[relative_path]
            if observed_rows != output.get("row_count"):
                failures.append(
                    f"{relative_path} row_count mismatch: {observed_rows} != {output.get('row_count')}"
                )

    for check in dq.get("checks", []):
        if check.get("severity") == "block_publish" and check.get("status") != "pass":
            failures.append(f"blocking DQ gate did not pass: {check.get('gate_id')}")

    return failures


def validate_payload_schema_versions(
    payloads: list[tuple[dict[str, Any], dict[str, Any]]],
) -> list[str]:
    failures: list[str] = []
    for spec, payload in payloads:
        label = spec.get("role", Path(spec.get("path", "")).name)
        if payload.get("schema_version") != spec.get("schema_version"):
            failures.append(
                f"{label} schema_version mismatch: {payload.get('schema_version')} != {spec.get('schema_version')}"
            )
    return failures
