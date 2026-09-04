#!/usr/bin/env python3
"""Validate the read-only worker public package promotion templates."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


DEFAULT_DIR = Path("examples/public/readonly-worker-candidate-template-v0")

BLOCKED_PUBLIC_MARKERS = {
    "rpc_or_api_url": re.compile(r"https://[^\"'\s]*(helius|rpc|api-key|apikey)[^\"'\s]*", re.IGNORECASE),
    "env_file": re.compile(r"(^|[/:])\.env(\b|$)"),
    "local_path": re.compile(r"/Users/|/Volumes/|/private/"),
    "bearer_token": re.compile(r"bearer\s+[a-z0-9._-]+", re.IGNORECASE),
    "private_key": re.compile(r"private[_ -]?key|seed phrase|wallet secret", re.IGNORECASE),
    "raw_payload": re.compile(r"raw_account_bytes|account_data_base64|raw_bytes", re.IGNORECASE),
    "execution_surface": re.compile(
        r"submit_transaction|priority_fee_bid|keypair_path|block_engine|wallet_inventory",
        re.IGNORECASE,
    ),
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def scan_text(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    failures: list[str] = []
    for label, pattern in BLOCKED_PUBLIC_MARKERS.items():
        if pattern.search(text):
            failures.append(f"{path}: blocked marker `{label}`")
    return failures


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if manifest.get("manifest_template_version") != "oprs.readonly_worker_public_package_manifest_template.v0":
        failures.append("manifest_template_version must be oprs.readonly_worker_public_package_manifest_template.v0")
    if manifest.get("package_template_id") != "readonly-worker-candidate-template-v0":
        failures.append("package_template_id must be readonly-worker-candidate-template-v0")
    if manifest.get("capability") != "read_only_dry_run":
        failures.append("capability must be read_only_dry_run")
    if manifest.get("template_status") != "blocked_until_founder_review":
        failures.append("template_status must be blocked_until_founder_review")
    if manifest.get("public_output_published") is not False:
        failures.append("public_output_published must be false")

    selected = manifest.get("selected_candidate", {})
    if selected.get("candidate_schema_version") != "oprs.readonly_worker_public_candidate.v0":
        failures.append("selected_candidate.candidate_schema_version must match the public candidate schema")
    if selected.get("candidate_summary_path") != "candidate_summary.json":
        failures.append("selected_candidate.candidate_summary_path must be candidate_summary.json")
    for key in ["candidate_id", "candidate_summary_sha256"]:
        if not str(selected.get(key, "")).startswith("REPLACE_"):
            failures.append(f"selected_candidate.{key} must remain a template placeholder")

    generated_from = manifest.get("generated_from", {})
    for key in [
        "private_worker_payload_bodies_used",
        "private_worker_payload_bodies_committed",
        "private_paths_committed",
    ]:
        if generated_from.get(key) is not False:
            failures.append(f"generated_from.{key} must be false")

    gates = manifest.get("promotion_gates", {})
    required_false_gates = [
        "founder_review_recorded",
        "candidate_validator_passed",
        "final_scrub_passed",
        "manifest_checksums_bound",
        "dq_blocking_failures_zero",
        "contract_index_entry_added",
    ]
    for gate in required_false_gates:
        if gates.get(gate) is not False:
            failures.append(f"promotion_gates.{gate} must be false in the template")

    outputs = manifest.get("outputs", [])
    if len(outputs) != 2:
        failures.append("outputs must contain candidate_summary.json and dq.json templates")
    output_paths = {output.get("path") for output in outputs if isinstance(output, dict)}
    if output_paths != {"candidate_summary.json", "dq.json"}:
        failures.append("outputs must list candidate_summary.json and dq.json")

    dq = manifest.get("dq", {})
    if dq.get("status") != "template_only":
        failures.append("dq.status must be template_only")
    if dq.get("blocking_failures") != 6:
        failures.append("dq.blocking_failures must remain 6 until final promotion")

    scrub = manifest.get("scrub", {})
    if scrub.get("status") != "template_only":
        failures.append("scrub.status must be template_only")

    limitations = " ".join(manifest.get("known_limitations", []))
    for required in ["Template only", "founder review", "replay readiness", "signing", "submission"]:
        if required not in limitations:
            failures.append(f"known_limitations must include `{required}` boundary text")

    return failures


def validate_dq(dq: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if dq.get("schema_version") != "oprs.public_dq_report.v0":
        failures.append("dq.schema_version must be oprs.public_dq_report.v0")
    if dq.get("status") != "template_only":
        failures.append("dq.status must be template_only")
    if dq.get("blocking_failures") != 6:
        failures.append("dq.blocking_failures must be 6 in the template")

    checks = dq.get("checks", [])
    if len(checks) != 6:
        failures.append("dq.checks must contain six publish-blocking template gates")
    for check in checks:
        if not isinstance(check, dict):
            failures.append("dq.checks entries must be objects")
            continue
        if check.get("severity") != "block_publish":
            failures.append(f"{check.get('gate_id', '<unknown>')}: severity must be block_publish")
        if check.get("status") != "pending":
            failures.append(f"{check.get('gate_id', '<unknown>')}: status must be pending")

    expected_gates = {
        "founder_review_recorded",
        "candidate_validator_passed",
        "final_scrub_passed",
        "manifest_checksums_bound",
        "dq_blocking_failures_zero",
        "contract_index_entry_added",
    }
    observed_gates = {check.get("gate_id") for check in checks if isinstance(check, dict)}
    if observed_gates != expected_gates:
        failures.append(f"dq gate set mismatch: {sorted(observed_gates)}")

    return failures


def validate_template(template_dir: Path) -> list[str]:
    failures: list[str] = []
    manifest_path = template_dir / "manifest.template.json"
    dq_path = template_dir / "dq.template.json"
    readme_path = template_dir / "README.md"

    for path in [manifest_path, dq_path, readme_path]:
        if not path.exists():
            failures.append(f"missing template file: {path}")
            continue
        failures.extend(scan_text(path))

    if manifest_path.exists():
        failures.extend(validate_manifest(load_json(manifest_path)))
    if dq_path.exists():
        failures.extend(validate_dq(load_json(dq_path)))
    if readme_path.exists():
        readme = readme_path.read_text(encoding="utf-8")
        for required in ["public promotion template", "not a promoted worker output", "contract-index.json"]:
            if required not in readme:
                failures.append(f"README missing `{required}`")

    return failures


def main() -> int:
    template_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DIR
    failures = validate_template(template_dir)
    if failures:
        print("Read-only worker public promotion template validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"PASS read-only worker public promotion template: {template_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
