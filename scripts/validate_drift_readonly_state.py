#!/usr/bin/env python3
"""Validate a local Drift read-only state/public-field report under target/."""

from __future__ import annotations

import sys
import re
from pathlib import Path
from typing import Any

from public_package_contract import load_json


DEFAULT_REPORT = Path("target/oprs-drift-readonly-state/latest-public-fields.json")
EXPECTED_COMMIT = "0ae3e3b1db782a6765c3525b3dec38ad4d9d3a62"
EXPECTED_IDL_SHA = "9646dd6a893568d85d8dc47507e047010bf7e945"
LOCAL_BLOCKED_PATTERNS = {
    "rpc_url": re.compile(r"https://[^\"'\s]*(helius|rpc|api-key|apikey)[^\"'\s]*", re.IGNORECASE),
    "env_file": re.compile(r"(^|[/:])\.env(\b|$)"),
    "local_path": re.compile(r"/Users/|/Volumes/|/private/"),
    "bearer_token": re.compile(r"bearer\s+[a-z0-9._-]+", re.IGNORECASE),
    "raw_payload": re.compile(r"raw_account_bytes|account_data_base64|raw_bytes", re.IGNORECASE),
}


def validate_report(report_path: Path) -> list[str]:
    failures: list[str] = []
    if not report_path.exists():
        return [f"missing Drift read-only state report: {report_path}"]

    report = load_json(report_path)
    failures.extend(scan_local_blocked_text(report_path, report_path.read_text(encoding="utf-8")))

    if report.get("report_id") != "drift_readonly_state_discovery":
        failures.append("report_id must be drift_readonly_state_discovery")
    if report.get("rpc", {}).get("credential_printed") is not False:
        failures.append("rpc.credential_printed must be false")

    provenance = report.get("decoder_provenance", {})
    if provenance.get("protocol_repo_commit") != EXPECTED_COMMIT:
        failures.append("decoder_provenance.protocol_repo_commit mismatch")
    if provenance.get("drift_idl_blob_sha") != EXPECTED_IDL_SHA:
        failures.append("decoder_provenance.drift_idl_blob_sha mismatch")

    forbidden_actions = set(report.get("forbidden_actions", []))
    for required in [
        "sign",
        "submit_transaction",
        "retry_transaction",
        "bid_priority_fee",
        "load_keypair",
        "manage_capital",
    ]:
        if required not in forbidden_actions:
            failures.append(f"forbidden_actions missing {required}")

    targets = report.get("targets", [])
    if not isinstance(targets, list) or not targets:
        failures.append("targets must be a non-empty array")
        return failures

    public_field_decode_count = 0
    public_field_count = 0
    for target in targets:
        if not isinstance(target, dict):
            failures.append("target must be an object")
            continue
        probe = target.get("probe", {})
        if probe.get("exists") is False:
            continue
        if probe.get("executable") is True:
            failures.append(f"{target.get('target_id')}: target account must not be executable")
        if target.get("target_kind") in {"state_account", "perp_market_account", "spot_market_account"}:
            snapshot = target.get("shape_snapshot", {})
            failures.extend(validate_shape_snapshot(target, snapshot))
            public_decode = snapshot.get("public_field_decode")
            if isinstance(public_decode, dict):
                public_field_decode_count += 1
                fields = public_decode.get("fields", [])
                public_field_count += len(fields) if isinstance(fields, list) else 0
                failures.extend(validate_public_field_decode(target, public_decode))

    if provenance.get("public_field_decode_included") is True and public_field_decode_count == 0:
        failures.append("public_field_decode_included=true but no public field decodes found")
    if public_field_decode_count > 0 and public_field_count == 0:
        failures.append("public field decodes found but no fields decoded")

    envelope = report.get("data_reconstruction_envelope", {})
    if envelope.get("protocol") != "drift":
        failures.append("data_reconstruction_envelope.protocol must be drift")
    if envelope.get("query_config", {}).get("transaction_details") is not None:
        failures.append("transaction_details must stay null")

    return failures


def scan_local_blocked_text(path: Path, text: str) -> list[str]:
    failures: list[str] = []
    for label, pattern in LOCAL_BLOCKED_PATTERNS.items():
        if pattern.search(text):
            failures.append(f"{path}: blocked local marker `{label}`")
    return failures


def validate_shape_snapshot(target: dict[str, Any], snapshot: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    target_id = target.get("target_id", "<unknown>")
    if not isinstance(snapshot, dict):
        return [f"{target_id}: missing shape_snapshot"]
    if snapshot.get("raw_account_data_committed") is not False:
        failures.append(f"{target_id}: raw_account_data_committed must be false")
    if snapshot.get("replay_ready") is not False:
        failures.append(f"{target_id}: replay_ready must be false")
    if snapshot.get("discriminator_match") is not True:
        failures.append(f"{target_id}: discriminator_match must be true")
    if snapshot.get("source_commit") != EXPECTED_COMMIT:
        failures.append(f"{target_id}: source_commit mismatch")
    if snapshot.get("idl_blob_sha") != EXPECTED_IDL_SHA:
        failures.append(f"{target_id}: idl_blob_sha mismatch")
    return failures


def validate_public_field_decode(target: dict[str, Any], public_decode: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    target_id = target.get("target_id", "<unknown>")
    if public_decode.get("user_state_decoded") is not False:
        failures.append(f"{target_id}: user_state_decoded must be false")
    if public_decode.get("market_economics_decoded") is not False:
        failures.append(f"{target_id}: market_economics_decoded must be false")
    if public_decode.get("replay_ready") is not False:
        failures.append(f"{target_id}: public decode replay_ready must be false")
    if public_decode.get("field_decode_claimed") is not True:
        failures.append(f"{target_id}: field_decode_claimed must be true for public decode")
    if public_decode.get("validation_failures") not in ([], None):
        failures.append(f"{target_id}: validation_failures must be empty")

    fields = public_decode.get("fields", [])
    if not isinstance(fields, list) or not fields:
        failures.append(f"{target_id}: public decode fields must be non-empty")
        return failures
    for field in fields:
        if not isinstance(field, dict):
            failures.append(f"{target_id}: public field must be an object")
            continue
        if field.get("matches_expected") is not True:
            failures.append(f"{target_id}.{field.get('field')}: matches_expected must be true")
        if "value" not in field:
            failures.append(f"{target_id}.{field.get('field')}: missing value")
        if field.get("offset", -1) < 0:
            failures.append(f"{target_id}.{field.get('field')}: offset must be non-negative")
        if field.get("length", 0) <= 0:
            failures.append(f"{target_id}.{field.get('field')}: length must be positive")
    return failures


def main() -> int:
    report_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_REPORT
    failures = validate_report(report_path)
    if failures:
        print("Drift read-only state validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"PASS Drift read-only state report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
