#!/usr/bin/env python3
"""Sample public Jupiter Perps transaction history through read-only RPC.

This command intentionally writes only scrubbed public transaction summaries. It
must never print HELIUS_RPC_URL or any other RPC credential.
"""

from __future__ import annotations

import argparse
import hashlib
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

COMMON_PROGRAM_ACCOUNTS = {
    "11111111111111111111111111111111",
    "ComputeBudget111111111111111111111111111111",
    "SysvarRent111111111111111111111111111111111",
    "SysvarC1ock11111111111111111111111111111111",
    "Sysvar1nstructions1111111111111111111111111",
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
    "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL",
    "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr",
    JUPITER_PERPS_PROGRAM_ID,
}


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


def stable_hash(values: list[str]) -> str:
    return hashlib.sha256("\n".join(sorted(values)).encode("utf-8")).hexdigest()


def shared_account_owner_summary(shared_keys: list[str], account_metadata: dict[str, dict[str, Any]]) -> dict[str, Any]:
    owner_counts: dict[str, int] = {}
    existing_count = 0
    metadata_known_count = 0
    executable_count = 0
    non_executable_count = 0
    missing_count = 0
    for key in shared_keys:
        metadata = account_metadata.get(key)
        if not metadata:
            continue
        metadata_known_count += 1
        if metadata.get("exists") is not True:
            missing_count += 1
            continue
        existing_count += 1
        if metadata.get("executable") is True:
            executable_count += 1
        elif metadata.get("executable") is False:
            non_executable_count += 1
        owner = metadata.get("owner")
        if isinstance(owner, str):
            owner_counts[owner] = owner_counts.get(owner, 0) + 1

    top_owners = [
        {"owner": owner, "count": count}
        for owner, count in sorted(owner_counts.items(), key=lambda item: (-item[1], item[0]))[:8]
    ]
    return {
        "metadata_known_count": metadata_known_count,
        "existing_count": existing_count,
        "missing_count": missing_count,
        "executable_count": executable_count,
        "non_executable_count": non_executable_count,
        "owner_counts_top": top_owners,
        "owner_counts_truncated": len(owner_counts) > len(top_owners),
    }


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
    candidate_account_keys = sorted(set(account_keys) - COMMON_PROGRAM_ACCOUNTS)
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
            "candidate_account_key_count": len(candidate_account_keys),
            "account_keys_hash": stable_hash(account_keys),
            "top_level_instruction_count": len(instructions),
            "top_level_program_instruction_count": top_level_program_instruction_count,
            "inner_program_instruction_count": inner_program_instruction_count,
            "log_message_count": len(log_messages) if isinstance(log_messages, list) else None,
            "version": transaction.get("version"),
        }
    )
    return summary


def account_metadata_batch(rpc_url: str, addresses: list[str]) -> dict[str, dict[str, Any]]:
    metadata: dict[str, dict[str, Any]] = {}
    if not addresses:
        return metadata

    for start in range(0, len(addresses), 100):
        chunk = addresses[start : start + 100]
        result = rpc_call(
            rpc_url,
            "getMultipleAccounts",
            [
                chunk,
                {
                    "commitment": "confirmed",
                    "encoding": "base64",
                    "dataSlice": {"offset": 0, "length": 0},
                },
            ],
        )
        values = result.get("value", []) if isinstance(result, dict) else []
        for address, value in zip(chunk, values):
            if value is None:
                metadata[address] = {
                    "exists": False,
                    "owner": None,
                    "executable": None,
                    "perps_owned_non_executable": False,
                }
            else:
                owner = value.get("owner")
                executable = value.get("executable")
                metadata[address] = {
                    "exists": True,
                    "owner": owner,
                    "executable": executable,
                    "perps_owned_non_executable": owner == JUPITER_PERPS_PROGRAM_ID and executable is False,
                }
    return metadata


def build_lifecycle_candidates(
    summaries: list[dict[str, Any]],
    min_shared_keys: int,
    account_metadata: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    candidates = []
    available = [summary for summary in summaries if summary.get("transaction_available")]
    for index, first in enumerate(available):
        first_sig = first.get("signature")
        first_slot = first.get("slot")
        if not isinstance(first_sig, str) or not isinstance(first_slot, int):
            continue

        for second in available[index + 1 :]:
            second_sig = second.get("signature")
            second_slot = second.get("slot")
            if not isinstance(second_sig, str) or not isinstance(second_slot, int):
                continue

            first_keys = set(first.get("_candidate_account_keys", []))
            second_keys = set(second.get("_candidate_account_keys", []))
            shared_keys = sorted(first_keys & second_keys)
            if len(shared_keys) < min_shared_keys:
                continue

            perps_owned_shared_keys = [
                key
                for key in shared_keys
                if account_metadata.get(key, {}).get("perps_owned_non_executable") is True
            ]
            first_time = first.get("block_time")
            second_time = second.get("block_time")
            lifecycle_seed = [first_sig, second_sig] + shared_keys
            quality_flags = [
                "no_position_request_decode",
                "no_semantic_instruction_decode",
                "pairing_is_heuristic",
            ]
            if perps_owned_shared_keys:
                quality_flags.append("shared_perps_owned_non_executable_account_seen")
                candidate_strength = "shared_perps_owned_non_executable_account_seen_unverified"
            else:
                quality_flags.append("no_shared_perps_owned_non_executable_account_seen")
                candidate_strength = "shared_keys_only_unverified"
            candidates.append(
                {
                    "lifecycle_id": hashlib.sha256("\n".join(lifecycle_seed).encode("utf-8")).hexdigest(),
                    "first_signature": first_sig,
                    "second_signature": second_sig,
                    "first_slot": first_slot,
                    "second_slot": second_slot,
                    "latency_slots_abs": abs(second_slot - first_slot),
                    "latency_seconds_abs": (
                        abs(second_time - first_time)
                        if isinstance(first_time, int) and isinstance(second_time, int)
                        else None
                    ),
                    "pairing_basis": "shared_public_account_keys_only",
                    "shared_account_key_count": len(shared_keys),
                    "shared_account_keys": shared_keys[:12],
                    "shared_account_keys_truncated": len(shared_keys) > 12,
                    "shared_account_keys_hash": stable_hash(shared_keys),
                    "shared_account_owner_summary": shared_account_owner_summary(shared_keys, account_metadata),
                    "shared_perps_owned_non_executable_count": len(perps_owned_shared_keys),
                    "shared_perps_owned_non_executable_keys": perps_owned_shared_keys[:12],
                    "shared_perps_owned_non_executable_keys_truncated": len(perps_owned_shared_keys) > 12,
                    "shared_perps_owned_non_executable_keys_hash": stable_hash(perps_owned_shared_keys),
                    "request_fulfillment_pair_candidate": True,
                    "request_fulfillment_pair_claimed": False,
                    "position_request_decoded": False,
                    "raw_transaction_committed": False,
                    "proof_status": "candidate_pair_unverified",
                    "candidate_strength": candidate_strength,
                    "quality_flags": quality_flags,
                }
            )
    return sorted(
        candidates,
        key=lambda candidate: (
            -candidate["shared_perps_owned_non_executable_count"],
            -candidate["shared_account_key_count"],
            candidate["latency_slots_abs"],
            candidate["first_signature"],
            candidate["second_signature"],
        ),
    )


def build_report(
    rpc_url: str,
    limit: int,
    transaction_limit: int,
    min_shared_keys: int,
    probe_shared_accounts: bool,
) -> dict[str, Any]:
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
        summary = summarize_transaction(row, transaction)
        if transaction is not None:
            tx = transaction.get("transaction") if isinstance(transaction, dict) else {}
            message = tx.get("message") if isinstance(tx, dict) else {}
            account_keys = [account_key_value(key) for key in message.get("accountKeys", [])]
            summary["_candidate_account_keys"] = sorted(set(key for key in account_keys if key) - COMMON_PROGRAM_ACCOUNTS)
        sampled.append(summary)

    methods = ["getSlot", "getSignaturesForAddress"] + ["getTransaction"] * len(sampled)
    shared_account_candidates = sorted(
        {
            key
            for index, first in enumerate(sampled)
            for second in sampled[index + 1 :]
            for key in set(first.get("_candidate_account_keys", [])) & set(second.get("_candidate_account_keys", []))
        }
    )
    account_metadata = account_metadata_batch(rpc_url, shared_account_candidates) if probe_shared_accounts else {}
    if probe_shared_accounts and shared_account_candidates:
        methods.append("getMultipleAccounts")
    lifecycle_candidates = build_lifecycle_candidates(sampled, min_shared_keys, account_metadata)
    stronger_candidate_count = sum(
        1
        for candidate in lifecycle_candidates
        if candidate.get("shared_perps_owned_non_executable_count", 0) > 0
    )
    public_summaries = []
    for summary in sampled:
        clean = dict(summary)
        clean.pop("_candidate_account_keys", None)
        public_summaries.append(clean)

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
                "verified_request_fulfillment_pairing",
                "position_request_binary_decode",
                "keeper_identity_or_strategy",
                "liquidation_replay",
                "order_submission",
            ],
        },
        "signature_sample": signatures,
        "transaction_summaries": public_summaries,
        "lifecycle_candidates": lifecycle_candidates,
        "pairing_heuristic": {
            "status": "candidate_pairing_only",
            "min_shared_non_common_account_keys": min_shared_keys,
            "basis": "shared public transaction account keys after common program account exclusion",
            "shared_account_metadata_probe": probe_shared_accounts,
            "shared_account_metadata_probe_count": len(shared_account_candidates) if probe_shared_accounts else 0,
            "shared_account_metadata_probe_methods": ["getMultipleAccounts"] if probe_shared_accounts else [],
            "stronger_candidate_count": stronger_candidate_count,
            "stronger_candidate_basis": "shared Jupiter-owned non-executable account seen, still unverified without PositionRequest/Position decode",
            "verified_request_fulfillment_pair_claimed": False,
            "raw_account_key_sets_committed": False,
        },
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
                "Lifecycle candidates are shared-account-key heuristics only and are not verified request/fulfillment pairs.",
                "A shared Jupiter-owned non-executable account strengthens a candidate but is not sufficient to claim request/fulfillment pairing.",
                "It does not decode PositionRequest or Position account binary layouts.",
                "Canonical Jupiter Perps IDL/source revision remains unresolved and must be pinned before decoded_snapshot claims.",
            ],
            "source_limitations": [
                "RPC retention and provider backfill limits are not assessed.",
                "Raw transaction bodies, instruction data, and logs are not committed to output.",
                "Program invocation counts are structural summaries, not semantic lifecycle labels.",
                "Raw account key sets are not committed; only account-key hashes and bounded shared candidate keys are emitted.",
                "Shared account metadata probes use dataSlice length 0 and do not emit raw account bytes.",
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
    parser.add_argument(
        "--min-shared-keys",
        type=int,
        default=2,
        help="Minimum non-common shared account keys required for an unverified lifecycle candidate.",
    )
    parser.add_argument(
        "--skip-shared-account-probe",
        action="store_true",
        help="Skip metadata-only getMultipleAccounts probes for shared candidate accounts.",
    )
    args = parser.parse_args()

    if args.limit < 1 or args.limit > 100:
        print("--limit must be between 1 and 100.", file=sys.stderr)
        return 2
    if args.transaction_limit < 0 or args.transaction_limit > args.limit:
        print("--transaction-limit must be between 0 and --limit.", file=sys.stderr)
        return 2
    if args.min_shared_keys < 1 or args.min_shared_keys > 20:
        print("--min-shared-keys must be between 1 and 20.", file=sys.stderr)
        return 2

    load_dotenv(Path(args.env_file))
    rpc_url = os.environ.get("HELIUS_RPC_URL")
    if not rpc_url:
        print("HELIUS_RPC_URL is not configured; Jupiter Perps transaction history skipped.", file=sys.stderr)
        return 2
    if not rpc_url.startswith("https://"):
        print("HELIUS_RPC_URL must be an HTTPS RPC URL.", file=sys.stderr)
        return 2

    report = build_report(
        rpc_url,
        args.limit,
        args.transaction_limit,
        args.min_shared_keys,
        probe_shared_accounts=not args.skip_shared_account_probe,
    )
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"Wrote scrubbed Jupiter Perps transaction-history sample to {output_path}")
    print("HELIUS_RPC_URL loaded locally and was not printed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
