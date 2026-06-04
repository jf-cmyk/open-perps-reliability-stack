#!/usr/bin/env python3
"""Discover public read-only Solana targets for OPRS decode proof.

This command intentionally prints and writes only scrubbed public metadata.
It must never print HELIUS_RPC_URL or any other RPC credential.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DRIFT_PROGRAM_ID = "dRiftyHA39MWEi3m9aunc5MzRF1JYuBsbn6VPcn33UH"


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def rpc_call(rpc_url: str, method: str, params: list[Any] | None = None) -> Any:
    body = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": "oprs-readonly-target-discovery",
            "method": method,
            "params": params or [],
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        rpc_url,
        data=body,
        headers={"content-type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as error:
        raise SystemExit(f"RPC request failed for method {method}: {error.reason}") from error

    if "error" in payload:
        raise SystemExit(f"RPC method {method} returned error: {payload['error']}")
    return payload.get("result")


def account_probe(rpc_url: str, address: str) -> dict[str, Any]:
    result = rpc_call(
        rpc_url,
        "getAccountInfo",
        [
            address,
            {
                "commitment": "confirmed",
                "encoding": "base64",
                "dataSlice": {"offset": 0, "length": 0},
            },
        ],
    )
    context = result.get("context", {}) if isinstance(result, dict) else {}
    value = result.get("value") if isinstance(result, dict) else None
    if value is None:
        return {
            "address": address,
            "exists": False,
            "context_slot": context.get("slot"),
        }
    return {
        "address": address,
        "exists": True,
        "context_slot": context.get("slot"),
        "lamports": value.get("lamports"),
        "owner": value.get("owner"),
        "executable": value.get("executable"),
        "rent_epoch": value.get("rentEpoch"),
    }


def build_report(rpc_url: str) -> dict[str, Any]:
    observed_slot = rpc_call(rpc_url, "getSlot", [{"commitment": "confirmed"}])
    drift_program = account_probe(rpc_url, DRIFT_PROGRAM_ID)
    now = int(time.time())

    return {
        "schema_version": "0.1.0",
        "report_id": "readonly_target_discovery",
        "generated_at_unix": now,
        "generated_by": "scripts/discover_readonly_targets.py",
        "rpc": {
            "provider_label": "local_readonly_rpc_env",
            "credential_printed": False,
            "commitment": "confirmed",
            "observed_slot": observed_slot,
        },
        "targets": [
            {
                "target_id": "drift_protocol_program",
                "protocol": "drift",
                "priority": 1,
                "target_kind": "program_account",
                "address": DRIFT_PROGRAM_ID,
                "readiness": "ready_for_readonly_decode_proof",
                "probe": drift_program,
                "why": [
                    "Drift has public program/account/liquidation documentation.",
                    "Program account metadata can be fetched without signer or wallet access.",
                    "This is the safest first Helius proof target before user/market account decoding.",
                ],
                "forbidden_actions": [
                    "sign",
                    "submit_transaction",
                    "retry_transaction",
                    "bid_priority_fee",
                    "load_keypair",
                    "manage_capital",
                ],
            },
            {
                "target_id": "jupiter_perps_pool_or_custody_state",
                "protocol": "jupiter_perps",
                "priority": 2,
                "target_kind": "pool_or_custody_account",
                "address": None,
                "readiness": "needs_public_program_or_account_resolution",
                "probe": None,
                "why": [
                    "Jupiter Perps is relevant as a major trader-to-LP/JLP Solana perps venue.",
                    "It provides a pool/custody/oracle contrast to Drift's margin-account model.",
                ],
                "next_step": "Resolve a public Jupiter Perps pool, custody, or program account from an official source before RPC probing.",
            },
            {
                "target_id": "phoenix_rise_market_data",
                "protocol": "phoenix_rise",
                "priority": 3,
                "target_kind": "public_market_data",
                "address": None,
                "readiness": "http_ws_telemetry_first",
                "probe": None,
                "why": [
                    "Phoenix/Rise is relevant for orderbook, fill, depth, candle, and funding telemetry.",
                    "Instruction builders remain out of scope; start with read-only HTTP/WS data.",
                ],
            },
        ],
        "data_reconstruction_envelope": {
            "schema_version": "0.1.0",
            "envelope_id": "readonly_target_discovery_reconstruction",
            "dataset_name": "readonly_target_discovery",
            "chain_id": "solana-mainnet-beta",
            "protocol": "multi",
            "reconstruction_type": "historical_rpc",
            "sources": [
                {
                    "source_id": "local_helius_rpc_confirmed",
                    "source_kind": "solana_rpc",
                    "provider_label": "helius_hobby_plan",
                    "commitment": "confirmed",
                    "lifecycle_stage": "read_only_rpc_probe",
                    "retention_boundary": "provider_default_retention_not_assessed",
                }
            ],
            "slot_range": {
                "start_slot": observed_slot,
                "end_slot": observed_slot,
                "coverage": "partial",
            },
            "query_config": {
                "methods": ["getSlot", "getAccountInfo"],
                "transaction_details": None,
                "max_supported_transaction_version": None,
                "address_filter_count": 1,
                "stream_gap_count": 0,
                "unsupported_version_count": 0,
            },
            "evidence_refs": [
                "target/oprs-readonly-target-discovery/latest.json"
            ],
            "known_gaps": [
                "Only Drift program account metadata is probed in this first command.",
                "Jupiter and Phoenix targets require resolved public account/API targets before probing.",
            ],
            "source_limitations": [
                "No transaction history, user account, market account, or oracle account decode is performed yet.",
                "RPC retention and provider backfill limits are not assessed in this first probe.",
            ],
            "generated_at_unix": now,
            "generated_by": "scripts/discover_readonly_targets.py",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", default=".env")
    parser.add_argument(
        "--out",
        default="target/oprs-readonly-target-discovery/latest.json",
        help="Output path for scrubbed discovery report.",
    )
    args = parser.parse_args()

    load_dotenv(Path(args.env_file))
    rpc_url = os.environ.get("HELIUS_RPC_URL")
    if not rpc_url:
        print("HELIUS_RPC_URL is not configured; discovery skipped.", file=sys.stderr)
        return 2
    if not rpc_url.startswith("https://"):
        print("HELIUS_RPC_URL must be an HTTPS RPC URL.", file=sys.stderr)
        return 2

    report = build_report(rpc_url)
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"Wrote scrubbed read-only discovery report to {output_path}")
    print("HELIUS_RPC_URL loaded locally and was not printed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
