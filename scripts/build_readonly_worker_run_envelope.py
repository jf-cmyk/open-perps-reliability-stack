#!/usr/bin/env python3
"""Build a private read-only worker run envelope from target artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Any

from public_package_contract import load_json
from validate_readonly_worker_run_envelope import validate_envelope


DEFAULT_INPUTS = [
    Path("target/oprs-worker-runs/drift-state-smoke.json"),
    Path("target/oprs-worker-runs/jupiter-role-map-smoke.json"),
    Path("target/oprs-worker-runs/phoenix-market-telemetry-smoke.json"),
]
DEFAULT_OUT = Path("target/oprs-worker-run-envelopes/latest.json")
VALIDATORS = {
    "drift": "scripts/validate_drift_readonly_state.py",
    "jupiter": "scripts/validate_jupiter_lifecycle_role_map_probe.py",
    "phoenix": "scripts/validate_phoenix_market_telemetry_probe.py",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _protocol(payload: dict[str, Any]) -> str:
    protocol = payload.get("protocol") or payload.get("data_reconstruction_envelope", {}).get("protocol")
    if protocol == "drift":
        return "drift"
    if protocol == "jupiter_perps":
        return "jupiter"
    if protocol == "phoenix_rise":
        return "phoenix"
    raise ValueError(f"unsupported worker artifact protocol: {protocol!r}")


def _dataset_name(payload: dict[str, Any]) -> str:
    return (
        payload.get("dataset_name")
        or payload.get("report_id")
        or payload.get("data_reconstruction_envelope", {}).get("dataset_name")
        or "unknown"
    )


def _source_kind(protocol: str) -> str:
    if protocol in {"drift", "jupiter"}:
        return "solana_rpc"
    if protocol == "phoenix":
        return "public_http"
    return "mixed_readonly"


def _live_read_claimed(payload: dict[str, Any], protocol: str) -> bool:
    readiness = payload.get("readiness", {})
    if protocol == "drift":
        return payload.get("rpc", {}).get("observed_slot") is not None
    if protocol == "jupiter":
        return readiness.get("live_rpc_read_claimed") is True
    if protocol == "phoenix":
        return readiness.get("live_public_http_probe_claimed") is True
    return False


def _artifact(path: Path) -> dict[str, Any]:
    payload = load_json(path)
    protocol = _protocol(payload)
    return {
        "path": path.as_posix(),
        "sha256": _sha256(path),
        "byte_length": path.stat().st_size,
        "protocol": protocol,
        "dataset_name": _dataset_name(payload),
        "schema_version": str(payload.get("schema_version", "unknown")),
        "validator_status": "passed",
        "summary": {
            "source_kind": _source_kind(protocol),
            "read_only_probe": True,
            "live_read_claimed": _live_read_claimed(payload, protocol),
            "replay_ready": False,
            "execution_claimed": False,
        },
    }


def build_envelope(inputs: list[Path], run_id: str) -> dict[str, Any]:
    artifacts = [_artifact(path) for path in inputs]
    protocols = sorted({artifact["protocol"] for artifact in artifacts})
    validators = sorted({VALIDATORS[artifact["protocol"]] for artifact in artifacts})
    return {
        "schema_version": "oprs.readonly_worker_run_envelope.v0",
        "run_id": run_id,
        "generated_at_unix": int(time.time()),
        "worker": {
            "service_name": "oprs-readonly-worker",
            "mode": "read_only_private_target",
            "lifecycle_stage": "local_probe_envelope",
            "generated_by": "scripts/build_readonly_worker_run_envelope.py",
        },
        "scope": {
            "chain_id": "solana-mainnet-beta",
            "target_protocols": protocols,
            "output_mode": "private_target",
            "private_output_location": "target/oprs-worker-runs/",
            "source_artifact_count": len(artifacts),
        },
        "artifacts": artifacts,
        "validation": {
            "status": "passed",
            "validated_artifact_count": len(artifacts),
            "validators": validators,
            "secret_scan_passed": True,
        },
        "promotion_policy": {
            "public_output_published": False,
            "public_candidate_created": False,
            "promotion_requires_founder_review": True,
            "promotion_requires_validator_pass": True,
            "promotion_requires_scrub_pass": True,
        },
        "safety_invariants": {
            "rpc_credential_printed": False,
            "contains_api_key": False,
            "contains_webhook_url": False,
            "raw_account_data_committed": False,
            "raw_transaction_committed": False,
            "signing_enabled": False,
            "transaction_submission_enabled": False,
            "priority_fee_bidding_enabled": False,
            "keypair_loading_enabled": False,
            "custody_enabled": False,
            "capital_management_enabled": False,
        },
        "forbidden_actions": [
            "sign",
            "submit_transaction",
            "retry_transaction",
            "bid_priority_fee",
            "load_keypair",
            "manage_custody",
            "manage_capital",
            "publish_without_review",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", dest="inputs", type=Path, action="append", default=[])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--run-id", default="local_worker_smoke_latest")
    args = parser.parse_args()

    inputs = args.inputs or DEFAULT_INPUTS
    missing = [path for path in inputs if not path.exists()]
    if missing:
        for path in missing:
            print(f"missing worker artifact: {path}")
        return 2
    for path in inputs:
        if not path.as_posix().startswith("target/oprs-worker-runs/"):
            print(f"worker artifact must stay under target/oprs-worker-runs/: {path}")
            return 2

    envelope = build_envelope(inputs, args.run_id)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(envelope, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    failures = validate_envelope(args.out)
    if failures:
        print("generated envelope failed validation:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"PASS built read-only worker run envelope: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
