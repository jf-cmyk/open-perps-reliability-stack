#!/usr/bin/env python3
"""Build a public-safe worker candidate summary from a private run envelope."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Any

from public_package_contract import load_json
from validate_readonly_worker_public_candidate import validate_candidate
from validate_readonly_worker_run_envelope import validate_envelope


DEFAULT_ENVELOPE = Path("target/oprs-worker-run-envelopes/latest.json")
DEFAULT_OUT = Path("target/oprs-worker-public-candidates/latest.json")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _candidate_status(envelope: dict[str, Any], founder_reviewed: bool) -> str:
    if envelope.get("validation", {}).get("status") != "passed":
        return "blocked_validation_failed"
    if not founder_reviewed:
        return "blocked_pending_founder_review"
    return "ready_for_manual_public_package_review"


def build_candidate(envelope_path: Path, founder_reviewed: bool, candidate_id: str) -> dict[str, Any]:
    envelope = load_json(envelope_path)
    artifacts = envelope.get("artifacts", [])
    protocols = []
    for artifact in artifacts:
        summary = artifact.get("summary", {})
        protocols.append(
            {
                "protocol": artifact["protocol"],
                "dataset_name": artifact["dataset_name"],
                "source_kind": summary["source_kind"],
                "artifact_hash": artifact["sha256"],
                "validator_status": artifact["validator_status"],
                "live_read_claimed": summary["live_read_claimed"],
                "replay_ready": False,
                "execution_claimed": False,
            }
        )

    validation_status = envelope.get("validation", {}).get("status", "failed_closed")
    validator_passed = validation_status == "passed"
    scrub_passed = envelope.get("validation", {}).get("secret_scan_passed") is True
    return {
        "schema_version": "oprs.readonly_worker_public_candidate.v0",
        "candidate_id": candidate_id,
        "generated_at_unix": int(time.time()),
        "source_envelope": {
            "schema_version": envelope["schema_version"],
            "run_id": envelope["run_id"],
            "artifact_count": len(artifacts),
            "source_envelope_body_committed": False,
            "source_envelope_hash": _sha256(envelope_path),
        },
        "summary": {
            "worker_service": envelope["worker"]["service_name"],
            "output_mode": envelope["scope"]["output_mode"],
            "validation_status": validation_status,
            "validated_artifact_count": envelope["validation"]["validated_artifact_count"],
            "public_candidate_status": _candidate_status(envelope, founder_reviewed),
        },
        "protocols": protocols,
        "promotion_gates": {
            "founder_review_recorded": founder_reviewed,
            "validator_passed": validator_passed,
            "scrub_passed": scrub_passed,
            "public_package_manifest_created": False,
            "public_package_dq_created": False,
            "public_output_published": False,
        },
        "public_payload_policy": {
            "private_artifact_paths_committed": False,
            "private_payload_bodies_committed": False,
            "raw_account_data_committed": False,
            "raw_transaction_committed": False,
            "only_counts_hashes_and_status": True,
        },
        "safety_invariants": {
            "contains_rpc_url": False,
            "contains_api_key": False,
            "contains_webhook_url": False,
            "contains_private_key": False,
            "contains_wallet_path": False,
            "signing_enabled": False,
            "transaction_submission_enabled": False,
            "priority_fee_bidding_enabled": False,
            "custody_enabled": False,
            "capital_management_enabled": False,
        },
        "known_limitations": [
            "This candidate summarizes a private worker run envelope by counts, hashes, and statuses only.",
            "It is blocked from public-package promotion until founder review is recorded and package manifest/DQ files are created.",
            "It does not include private artifact paths, payload bodies, raw account data, raw transactions, RPC URLs, API keys, or webhooks.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--envelope", type=Path, default=DEFAULT_ENVELOPE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--candidate-id", default="local_worker_public_candidate_latest")
    parser.add_argument(
        "--founder-reviewed",
        action="store_true",
        help="Mark founder review as recorded. Still does not publish or create package files.",
    )
    args = parser.parse_args()

    envelope_failures = validate_envelope(args.envelope)
    if envelope_failures:
        print("source envelope failed validation:")
        for failure in envelope_failures:
            print(f"- {failure}")
        return 1

    candidate = build_candidate(args.envelope, args.founder_reviewed, args.candidate_id)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(candidate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    failures = validate_candidate(args.out)
    if failures:
        print("generated public candidate failed validation:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"PASS built read-only worker public candidate: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
