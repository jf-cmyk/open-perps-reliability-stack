#!/usr/bin/env python3
"""Discover public Jupiter Perps program, custody, and oracle metadata.

This command intentionally writes only scrubbed public metadata. It must never
print HELIUS_RPC_URL or any other RPC credential.
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


JUPITER_PERPS_PROGRAM_ID = "PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu"

JUPITER_DEVELOPER_DOCS = "https://developers.jup.ag/docs/get-started/index"
JUPITER_TECHNICAL_REFERENCE = "https://docs.jup.ag/user-docs/trade/perps-and-jlp/technical-reference"
JUPITER_CUSTODY_ACCOUNT_DOCS = "https://developers.jup.ag/docs/perps/custody-account"
JUPITER_POOL_ACCOUNT_DOCS = "https://developers.jup.ag/docs/perps/pool-account"
JUPITER_POSITION_ACCOUNT_DOCS = "https://developers.jup.ag/docs/perps/position-account"
JUPITER_POSITION_REQUEST_DOCS = "https://developers.jup.ag/docs/perps/position-request-account"

CUSTODY_ACCOUNTS = [
    {
        "asset": "SOL",
        "address": "7xS2gz2bTp3fwCC7knJvUWTEU9Tycczu6VhJYKgi1wdz",
        "source": JUPITER_TECHNICAL_REFERENCE,
    },
    {
        "asset": "ETH",
        "address": "AQCGyheWPLeo6Qp9WpYS9m3Qj479t7R636N9ey1rEjEn",
        "source": JUPITER_TECHNICAL_REFERENCE,
    },
    {
        "asset": "BTC",
        "address": "5Pv3gM9JrFFH883SWAhvJC9RPYmo8UNxuFtv5bMMALkm",
        "source": JUPITER_TECHNICAL_REFERENCE,
    },
    {
        "asset": "USDC",
        "address": "G18jKKXQwBbrHeiK3C9MRXhkHsLHf7XgCSisykV46EZa",
        "source": JUPITER_TECHNICAL_REFERENCE,
    },
    {
        "asset": "USDT",
        "address": "4vkNeXiYEUizLdrpdPS1eC2mccyM4NUPRtERrk6ZETkk",
        "source": JUPITER_TECHNICAL_REFERENCE,
    },
]

ORACLE_ACCOUNTS = [
    {
        "asset": "SOL",
        "address": "FYq2BWQ1V5P1WFBqr3qB2Kb5yHVvSv7upzKodgQE5zXh",
        "oracle_system": "Edge by Chaos Labs primary, Chainlink/Pyth verification and fallback per Jupiter docs",
        "source": JUPITER_TECHNICAL_REFERENCE,
    },
    {
        "asset": "ETH",
        "address": "AFZnHPzy4mvVCffrVwhewHbFc93uTHvDSFrVH7GtfXF1",
        "oracle_system": "Edge by Chaos Labs primary, Chainlink/Pyth verification and fallback per Jupiter docs",
        "source": JUPITER_TECHNICAL_REFERENCE,
    },
    {
        "asset": "BTC",
        "address": "hUqAT1KQ7eW1i6Csp9CXYtpPfSAvi835V7wKi5fRfmC",
        "oracle_system": "Edge by Chaos Labs primary, Chainlink/Pyth verification and fallback per Jupiter docs",
        "source": JUPITER_TECHNICAL_REFERENCE,
    },
    {
        "asset": "USDC",
        "address": "6Jp2xZUTWdDD2ZyUPRzeMdc6AFQ5K3pFgZxk2EijfjnM",
        "oracle_system": "Edge by Chaos Labs primary, Chainlink/Pyth verification and fallback per Jupiter docs",
        "source": JUPITER_TECHNICAL_REFERENCE,
    },
    {
        "asset": "USDT",
        "address": "Fgc93D641F8N2d1xLjQ4jmShuD3GE3BsCXA56KBQbF5u",
        "oracle_system": "Edge by Chaos Labs primary, Chainlink/Pyth verification and fallback per Jupiter docs",
        "source": JUPITER_TECHNICAL_REFERENCE,
    },
]


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
            "id": "oprs-jupiter-perps-readonly-targets",
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


def static_target(target_id: str, target_kind: str, address: str, source: str, metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "target_id": target_id,
        "protocol": "jupiter_perps",
        "target_kind": target_kind,
        "address": address,
        "readiness": "target_discovered",
        "source": source,
        "metadata": metadata,
    }


def build_report(rpc_url: str) -> dict[str, Any]:
    observed_slot = rpc_call(rpc_url, "getSlot", [{"commitment": "confirmed"}])
    now = int(time.time())

    targets = [
        static_target(
            "jupiter_perps_program",
            "program_account",
            JUPITER_PERPS_PROGRAM_ID,
            JUPITER_DEVELOPER_DOCS,
            {
                "program": "Jupiter Perpetuals",
                "network": "solana-mainnet-beta",
                "integration_type": "read_only_metadata_probe",
            },
        )
    ]

    for custody in CUSTODY_ACCOUNTS:
        targets.append(
            static_target(
                f"jupiter_perps_custody_{custody['asset'].lower()}",
                "custody_account",
                custody["address"],
                custody["source"],
                {
                    "asset": custody["asset"],
                    "safe_first_fields": [
                        "pool",
                        "mint",
                        "tokenAccount",
                        "decimals",
                        "isStable",
                        "oracle",
                        "pricing",
                        "permissions",
                        "assets",
                        "fundingRateState",
                    ],
                },
            )
        )

    for oracle in ORACLE_ACCOUNTS:
        targets.append(
            static_target(
                f"jupiter_perps_oracle_{oracle['asset'].lower()}",
                "oracle_account",
                oracle["address"],
                oracle["source"],
                {
                    "asset": oracle["asset"],
                    "oracle_system": oracle["oracle_system"],
                    "safe_first_fields": [
                        "account_owner",
                        "executable",
                        "lamports",
                        "context_slot",
                    ],
                },
            )
        )

    for target in targets:
        target["probe"] = account_probe(rpc_url, target["address"])

    methods = ["getSlot"] + ["getAccountInfo"] * len(targets)

    return {
        "schema_version": "0.1.0",
        "report_id": "jupiter_perps_readonly_target_discovery",
        "generated_at_unix": now,
        "generated_by": "scripts/discover_jupiter_perps_readonly_targets.py",
        "rpc": {
            "provider_label": "local_readonly_rpc_env",
            "credential_printed": False,
            "commitment": "confirmed",
            "observed_slot": observed_slot,
        },
        "source_refs": {
            "jupiter_developer_docs": JUPITER_DEVELOPER_DOCS,
            "technical_reference": JUPITER_TECHNICAL_REFERENCE,
            "custody_account_docs": JUPITER_CUSTODY_ACCOUNT_DOCS,
            "pool_account_docs": JUPITER_POOL_ACCOUNT_DOCS,
            "position_account_docs": JUPITER_POSITION_ACCOUNT_DOCS,
            "position_request_docs": JUPITER_POSITION_REQUEST_DOCS,
        },
        "target_resolution": {
            "program_id_source": "Jupiter developer docs core programs table",
            "custody_source": "Jupiter technical reference custody accounts table",
            "oracle_source": "Jupiter technical reference oracle price accounts table",
            "decode_status": "target_discovered_not_binary_decoded",
            "source_strength": "official_docs_for_targets; canonical IDL/source revision still unresolved",
        },
        "targets": targets,
        "data_reconstruction_envelope": {
            "schema_version": "0.1.0",
            "envelope_id": "jupiter_perps_readonly_target_reconstruction",
            "dataset_name": "jupiter_perps_readonly_target_discovery",
            "chain_id": "solana-mainnet-beta",
            "protocol": "jupiter_perps",
            "reconstruction_type": "historical_rpc",
            "sources": [
                {
                    "source_id": "local_helius_rpc_confirmed",
                    "source_kind": "solana_rpc",
                    "provider_label": "helius_hobby_plan",
                    "commitment": "confirmed",
                    "lifecycle_stage": "read_only_rpc_probe",
                    "retention_boundary": "provider_default_retention_not_assessed",
                },
                {
                    "source_id": "jupiter_perps_official_docs",
                    "source_kind": "official_documentation",
                    "provider_label": "jupiter_developer_docs",
                    "commitment": "not_applicable",
                    "lifecycle_stage": "target_resolution",
                    "retention_boundary": "public_docs_current_version",
                },
            ],
            "slot_range": {
                "start_slot": observed_slot,
                "end_slot": observed_slot,
                "coverage": "partial",
            },
            "query_config": {
                "methods": methods,
                "transaction_details": None,
                "max_supported_transaction_version": None,
                "address_filter_count": len(targets),
                "stream_gap_count": 0,
                "unsupported_version_count": 0,
            },
            "evidence_refs": [
                "target/oprs-jupiter-perps-readonly-targets/latest.json"
            ],
            "known_gaps": [
                "This command probes account metadata and target resolution only; it does not decode account binary layouts yet.",
                "Canonical Jupiter Perps IDL/source revision remains unresolved and must be pinned before decoded_snapshot claims.",
                "No request, fulfillment, position, pre-state, transaction history, or liquidation event reconstruction is performed.",
            ],
            "source_limitations": [
                "Program, custody, and oracle addresses are resolved from current Jupiter public docs.",
                "Jupiter Perps request/fulfillment semantics require separate transaction-history proof before replay claims.",
                "RPC retention and provider backfill limits are not assessed in this metadata probe.",
            ],
            "generated_at_unix": now,
            "generated_by": "scripts/discover_jupiter_perps_readonly_targets.py",
        },
        "forbidden_actions": [
            "sign",
            "submit_transaction",
            "retry_transaction",
            "bid_priority_fee",
            "load_keypair",
            "manage_capital",
            "call_order_endpoint",
            "call_execute_endpoint",
            "call_build_endpoint",
            "call_submit_endpoint",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", default=".env")
    parser.add_argument(
        "--out",
        default="target/oprs-jupiter-perps-readonly-targets/latest.json",
        help="Output path for scrubbed Jupiter Perps read-only target report.",
    )
    args = parser.parse_args()

    load_dotenv(Path(args.env_file))
    rpc_url = os.environ.get("HELIUS_RPC_URL")
    if not rpc_url:
        print("HELIUS_RPC_URL is not configured; Jupiter Perps target discovery skipped.", file=sys.stderr)
        return 2
    if not rpc_url.startswith("https://"):
        print("HELIUS_RPC_URL must be an HTTPS RPC URL.", file=sys.stderr)
        return 2

    report = build_report(rpc_url)
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"Wrote scrubbed Jupiter Perps read-only target report to {output_path}")
    print("HELIUS_RPC_URL loaded locally and was not printed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
