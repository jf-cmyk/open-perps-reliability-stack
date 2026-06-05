#!/usr/bin/env python3
"""Sample public Jupiter Perps transaction history through read-only RPC.

This command intentionally writes only scrubbed public transaction summaries. It
must never print HELIUS_RPC_URL or any other RPC credential.
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
JUPITER_POSITION_REQUEST_DOCS = "https://developers.jup.ag/docs/perps/position-request-account"
JUPITER_POSITION_DOCS = "https://developers.jup.ag/docs/perps/position-account"


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
            "id": "oprs-jupiter-perps-transaction-history",
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
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as error:
        raise SystemExit(f"RPC request failed for method {method}: {error.reason}") from error

    if "error" in payload:
        raise SystemExit(f"RPC method {method} returned error: {payload['error']}")
    return payload.get("result")


def account_key_value(account_key: Any) -> str | None:
    if isinstance(account_key, str):
        return account_key
    if isinstance(account_key, dict):
        value = account_key.get("pubkey")
        return value if isinstance(value, str) else None
    return None


def summarize_transaction(signature_row: dict[str, Any], transaction: dict[str, Any] | None) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "signature": signature_row.get("signature"),
        "slot": signature_row.get("slot"),
        "block_time": signature_row.get("blockTime"),
        "confirmation_status": signature_row.get("confirmationStatus"),
        "signature_err": signature_row.get("err"),
        "transaction_available": transaction is not None,
        "lifecycle_claim": "program_invocation_observed_only",
        "request_fulfillment_pair_claimed": False,
        "position_request_decoded": False,
        "raw_transaction_committed": False,
    }
    if transaction is None:
        summary["known_gap"] = "RPC returned no transaction body for this signature."
        return summary

    meta = transaction.get("meta") if isinstance(transaction, dict) else {}
    tx = transaction.get("transaction") if isinstance(transaction, dict) else {}
    message = tx.get("message") if isinstance(tx, dict) else {}
    account_keys = [account_key_value(key) for key in message.get("accountKeys", [])]
    account_keys = [key for key in account_keys if key]
    instructions = message.get("instructions", []) if isinstance(message, dict) else []
    inner_instructions = meta.get("innerInstructions", []) if isinstance(meta, dict) else []
    log_messages = meta.get("logMessages", []) if isinstance(meta, dict) else []

    def instruction_program_id(instruction: dict[str, Any]) -> str | None:
        if "programId" in instruction and isinstance(instruction["programId"], str):
            return instruction["programId"]
        index = instruction.get("programIdIndex")
        if isinstance(index, int) and 0 <= index < len(account_keys):
            return account_keys[index]
        return None

    top_level_program_instruction_count = sum(
        1
        for instruction in instructions
        if isinstance(instruction, dict) and instruction_program_id(instruction) == JUPITER_PERPS_PROGRAM_ID
    )
    inner_program_instruction_count = 0
    for group in inner_instructions:
        for instruction in group.get("instructions", []) if isinstance(group, dict) else []:
            if isinstance(instruction, dict) and instruction_program_id(instruction) == JUPITER_PERPS_PROGRAM_ID:
                inner_program_instruction_count += 1

    summary.update(
        {
            "transaction_slot": transaction.get("slot"),
            "transaction_block_time": transaction.get("blockTime"),
            "fee": meta.get("fee") if isinstance(meta, dict) else None,
            "transaction_err": meta.get("err") if isinstance(meta, dict) else None,
            "account_key_count": len(account_keys),
            "top_level_instruction_count": len(instructions),
            "top_level_program_instruction_count": top_level_program_instruction_count,
            "inner_program_instruction_count": inner_program_instruction_count,
            "log_message_count": len(log_messages) if isinstance(log_messages, list) else None,
            "version": transaction.get("version"),
        }
    )
    return summary


def build_report(rpc_url: str, limit: int, transaction_limit: int) -> dict[str, Any]:
    observed_slot = rpc_call(rpc_url, "getSlot", [{"commitment": "confirmed"}])
    now = int(time.time())
    signatures = rpc_call(
        rpc_url,
        "getSignaturesForAddress",
        [
            JUPITER_PERPS_PROGRAM_ID,
            {
                "commitment": "confirmed",
                "limit": limit,
            },
        ],
    )
    if not isinstance(signatures, list):
        signatures = []

    sampled: list[dict[str, Any]] = []
    unsupported_version_count = 0
    for row in signatures[:transaction_limit]:
        signature = row.get("signature") if isinstance(row, dict) else None
        if not signature:
            continue
        try:
            transaction = rpc_call(
                rpc_url,
                "getTransaction",
                [
                    signature,
                    {
                        "commitment": "confirmed",
                        "encoding": "json",
                        "maxSupportedTransactionVersion": 0,
                    },
                ],
            )
        except SystemExit as error:
            if "Unsupported transaction version" in str(error):
                unsupported_version_count += 1
                transaction = None
            else:
                raise
        sampled.append(summarize_transaction(row, transaction))

    methods = ["getSlot", "getSignaturesForAddress"] + ["getTransaction"] * len(sampled)

    return {
        "schema_version": "0.1.0",
        "report_id": "jupiter_perps_transaction_history_sample",
        "generated_at_unix": now,
        "generated_by": "scripts/discover_jupiter_perps_transaction_history.py",
        "rpc": {
            "provider_label": "local_readonly_rpc_env",
            "credential_printed": False,
            "commitment": "confirmed",
            "observed_slot": observed_slot,
        },
        "source_refs": {
            "jupiter_developer_docs": JUPITER_DEVELOPER_DOCS,
            "technical_reference": JUPITER_TECHNICAL_REFERENCE,
            "position_request_docs": JUPITER_POSITION_REQUEST_DOCS,
            "position_docs": JUPITER_POSITION_DOCS,
        },
        "history_scope": {
            "program_id": JUPITER_PERPS_PROGRAM_ID,
            "status": "transaction_history_sample_only",
            "claim": "public Jupiter Perps program signatures and transaction summaries can be sampled through read-only RPC",
            "not_claimed": [
                "request_fulfillment_pairing",
                "position_request_binary_decode",
                "keeper_identity_or_strategy",
                "liquidation_replay",
                "order_submission",
            ],
        },
        "signature_sample": signatures,
        "transaction_summaries": sampled,
        "data_reconstruction_envelope": {
            "schema_version": "0.1.0",
            "envelope_id": "jupiter_perps_transaction_history_reconstruction",
            "dataset_name": "jupiter_perps_transaction_history_sample",
            "chain_id": "solana-mainnet-beta",
            "protocol": "jupiter_perps",
            "reconstruction_type": "historical_rpc",
            "sources": [
                {
                    "source_id": "local_helius_rpc_confirmed",
                    "source_kind": "solana_rpc",
                    "provider_label": "helius_hobby_plan",
                    "commitment": "confirmed",
                    "lifecycle_stage": "read_only_transaction_history_sample",
                    "retention_boundary": "provider_default_retention_not_assessed",
                },
                {
                    "source_id": "jupiter_perps_official_docs",
                    "source_kind": "protocol_docs",
                    "provider_label": "jupiter_developer_docs",
                    "commitment": "not_applicable",
                    "lifecycle_stage": "request_fulfillment_model_context",
                    "retention_boundary": "public_docs_current_version",
                },
            ],
            "slot_range": {
                "start_slot": min((row.get("slot") for row in signatures if isinstance(row.get("slot"), int)), default=None),
                "end_slot": max((row.get("slot") for row in signatures if isinstance(row.get("slot"), int)), default=None),
                "coverage": "partial",
            },
            "query_config": {
                "methods": methods,
                "transaction_details": "json_summary_only",
                "max_supported_transaction_version": 0,
                "address_filter_count": 1,
                "stream_gap_count": 0,
                "unsupported_version_count": unsupported_version_count,
            },
            "evidence_refs": [
                "target/oprs-jupiter-perps-transaction-history/latest.json"
            ],
            "known_gaps": [
                "This command samples public program signatures and transaction summaries only.",
                "It does not pair request and fulfillment transactions.",
                "It does not decode PositionRequest or Position account binary layouts.",
                "Canonical Jupiter Perps IDL/source revision remains unresolved and must be pinned before decoded_snapshot claims.",
            ],
            "source_limitations": [
                "RPC retention and provider backfill limits are not assessed.",
                "Raw transaction bodies, instruction data, and logs are not committed to output.",
                "Program invocation counts are structural summaries, not semantic lifecycle labels.",
            ],
            "generated_at_unix": now,
            "generated_by": "scripts/discover_jupiter_perps_transaction_history.py",
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
            "call_auth_endpoint",
            "keeper_operation",
            "rfq_or_order_routing",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", default=".env")
    parser.add_argument(
        "--out",
        default="target/oprs-jupiter-perps-transaction-history/latest.json",
        help="Output path for scrubbed Jupiter Perps transaction-history sample.",
    )
    parser.add_argument("--limit", type=int, default=12, help="Number of public signatures to sample.")
    parser.add_argument(
        "--transaction-limit",
        type=int,
        default=5,
        help="Number of sampled signatures to summarize with getTransaction.",
    )
    args = parser.parse_args()

    if args.limit < 1 or args.limit > 100:
        print("--limit must be between 1 and 100.", file=sys.stderr)
        return 2
    if args.transaction_limit < 0 or args.transaction_limit > args.limit:
        print("--transaction-limit must be between 0 and --limit.", file=sys.stderr)
        return 2

    load_dotenv(Path(args.env_file))
    rpc_url = os.environ.get("HELIUS_RPC_URL")
    if not rpc_url:
        print("HELIUS_RPC_URL is not configured; Jupiter Perps transaction history skipped.", file=sys.stderr)
        return 2
    if not rpc_url.startswith("https://"):
        print("HELIUS_RPC_URL must be an HTTPS RPC URL.", file=sys.stderr)
        return 2

    report = build_report(rpc_url, args.limit, args.transaction_limit)
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"Wrote scrubbed Jupiter Perps transaction-history sample to {output_path}")
    print("HELIUS_RPC_URL loaded locally and was not printed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
