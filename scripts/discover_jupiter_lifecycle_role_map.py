#!/usr/bin/env python3
"""Build a local-only Jupiter Perps instruction role-map probe.

This command combines the hash-pinned onchain Anchor IDL with public Jupiter
Perps transaction samples. It emits scrubbed role-binding summaries only: no
raw transactions, raw instruction data, RPC URLs, API keys, wallets, signers,
or account byte payloads are printed or committed.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import time
from pathlib import Path
from typing import Any

from fetch_jupiter_onchain_idl import JUPITER_PERPS_PROGRAM_ID, b58decode, load_dotenv, rpc_call


DEFAULT_IDL = "target/oprs-jupiter-onchain-idl/jupiter-perps-idl.json"
DEFAULT_OUT = "target/oprs-jupiter-lifecycle-role-map/latest.json"
JUPITER_POSITION_REQUEST_DOCS = "https://developers.jup.ag/docs/perps/position-request-account"
JUPITER_POSITION_DOCS = "https://developers.jup.ag/docs/perps/position-account"
JUPITER_TECHNICAL_REFERENCE = "https://docs.jup.ag/user-docs/trade/perps-and-jlp/technical-reference"

COMMON_PROGRAM_ACCOUNTS = {
    "11111111111111111111111111111111",
    "ComputeBudget111111111111111111111111111111",
    "SysvarRent11111111111111111111111111111111",
    "SysvarC1ock11111111111111111111111111111111",
    "Sysvar1nstructions1111111111111111111111111",
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
    "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL",
    JUPITER_PERPS_PROGRAM_ID,
}


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def instruction_discriminator(name: str) -> bytes:
    return hashlib.sha256(f"global:{name}".encode("utf-8")).digest()[:8]


def camel_to_snake(name: str) -> str:
    with_acronym_boundaries = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", with_acronym_boundaries).lower()


def account_key_value(account_key: Any) -> str | None:
    if isinstance(account_key, str):
        return account_key
    if isinstance(account_key, dict):
        pubkey = account_key.get("pubkey")
        return pubkey if isinstance(pubkey, str) else None
    return None


def message_account_keys(transaction: dict[str, Any]) -> list[str]:
    tx = transaction.get("transaction") if isinstance(transaction, dict) else {}
    message = tx.get("message") if isinstance(tx, dict) else {}
    keys = [account_key_value(key) for key in message.get("accountKeys", [])]
    clean = [key for key in keys if key]
    meta = transaction.get("meta") if isinstance(transaction, dict) else {}
    loaded = meta.get("loadedAddresses") if isinstance(meta, dict) else {}
    if isinstance(loaded, dict):
        for key in loaded.get("writable", []) + loaded.get("readonly", []):
            if isinstance(key, str):
                clean.append(key)
    return clean


def instruction_program_id(instruction: dict[str, Any], account_keys: list[str]) -> str | None:
    program_id = instruction.get("programId")
    if isinstance(program_id, str):
        return program_id
    index = instruction.get("programIdIndex")
    if isinstance(index, int) and 0 <= index < len(account_keys):
        return account_keys[index]
    return None


def instruction_accounts(instruction: dict[str, Any]) -> list[int]:
    accounts = instruction.get("accounts", [])
    if not isinstance(accounts, list):
        return []
    return [account for account in accounts if isinstance(account, int)]


def instruction_data_discriminator(instruction: dict[str, Any]) -> str | None:
    data = instruction.get("data")
    if not isinstance(data, str) or not data:
        return None
    try:
        raw = b58decode(data)
    except ValueError:
        return None
    if len(raw) < 8:
        return None
    return raw[:8].hex()


def flatten_idl_accounts(accounts: list[dict[str, Any]], prefix: str = "") -> list[dict[str, Any]]:
    roles: list[dict[str, Any]] = []
    for account in accounts:
        name = account.get("name")
        if not isinstance(name, str):
            continue
        path = f"{prefix}.{name}" if prefix else name
        nested = account.get("accounts")
        if isinstance(nested, list):
            roles.extend(flatten_idl_accounts(nested, path))
            continue
        roles.append(
            {
                "role": name,
                "role_path": path,
                "is_mut": bool(account.get("isMut", account.get("writable", False))),
                "is_signer": bool(account.get("isSigner", account.get("signer", False))),
            }
        )
    return roles


def idl_instruction_maps(
    idl: dict[str, Any],
) -> tuple[dict[str, str], dict[str, str], dict[str, dict[str, Any]]]:
    discriminator_to_name: dict[str, str] = {}
    discriminator_derivations: dict[str, str] = {}
    instruction_map: dict[str, dict[str, Any]] = {}
    for instruction in idl.get("instructions", []):
        name = instruction.get("name")
        if not isinstance(name, str):
            continue
        discriminator = instruction_discriminator(name).hex()
        snake_name = camel_to_snake(name)
        snake_discriminator = instruction_discriminator(snake_name).hex()
        roles = flatten_idl_accounts(instruction.get("accounts", []))
        discriminator_to_name[discriminator] = name
        discriminator_derivations[discriminator] = "idl_name"
        discriminator_to_name[snake_discriminator] = name
        discriminator_derivations[snake_discriminator] = "snake_case_idl_name"
        instruction_map[name] = {
            "name": name,
            "discriminator_hex": discriminator,
            "snake_case_discriminator_hex": snake_discriminator,
            "idl_role_count": len(roles),
            "roles": roles,
        }
    return discriminator_to_name, discriminator_derivations, instruction_map


def account_metadata_batch(rpc_url: str, addresses: list[str]) -> dict[str, dict[str, Any]]:
    metadata: dict[str, dict[str, Any]] = {}
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
                metadata[address] = {"exists": False, "owner_kind": "missing", "executable": None}
                continue
            owner = value.get("owner")
            if owner == JUPITER_PERPS_PROGRAM_ID:
                owner_kind = "jupiter_perps_program"
            elif owner in COMMON_PROGRAM_ACCOUNTS:
                owner_kind = "common_program"
            elif isinstance(owner, str):
                owner_kind = "other_public_owner_hash"
            else:
                owner_kind = "unknown"
            metadata[address] = {
                "exists": True,
                "owner_kind": owner_kind,
                "owner_hash": sha256_text(owner) if isinstance(owner, str) else None,
                "executable": value.get("executable"),
            }
    return metadata


def scrubbed_role_bindings(
    account_indices: list[int],
    account_keys: list[str],
    roles: list[dict[str, Any]],
    metadata: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    bindings = []
    for role_index, role in enumerate(roles[: len(account_indices)]):
        account_index = account_indices[role_index]
        pubkey = account_keys[account_index] if 0 <= account_index < len(account_keys) else None
        meta = metadata.get(pubkey, {}) if pubkey else {}
        bindings.append(
            {
                "role_index": role_index,
                "role": role["role"],
                "role_path": role["role_path"],
                "idl_is_mut": role["is_mut"],
                "idl_is_signer": role["is_signer"],
                "observed_pubkey_hash": sha256_text(pubkey) if pubkey else None,
                "observed_owner_kind": meta.get("owner_kind", "not_probed"),
                "observed_owner_hash": meta.get("owner_hash"),
                "observed_executable": meta.get("executable"),
            }
        )
    return bindings


def collect_jupiter_instructions(
    transaction: dict[str, Any],
    signature: str,
    discriminator_to_name: dict[str, str],
    discriminator_derivations: dict[str, str],
    instruction_map: dict[str, dict[str, Any]],
    metadata: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    account_keys = message_account_keys(transaction)
    tx = transaction.get("transaction") if isinstance(transaction, dict) else {}
    message = tx.get("message") if isinstance(tx, dict) else {}
    meta = transaction.get("meta") if isinstance(transaction, dict) else {}
    groups: list[tuple[str, list[dict[str, Any]]]] = [
        ("top_level", message.get("instructions", []) if isinstance(message.get("instructions"), list) else [])
    ]
    for group in meta.get("innerInstructions", []) if isinstance(meta, dict) else []:
        if isinstance(group, dict) and isinstance(group.get("instructions"), list):
            groups.append((f"inner_at_{group.get('index')}", group["instructions"]))

    observations = []
    for group_name, instructions in groups:
        for instruction_index, instruction in enumerate(instructions):
            if not isinstance(instruction, dict):
                continue
            if instruction_program_id(instruction, account_keys) != JUPITER_PERPS_PROGRAM_ID:
                continue
            discriminator = instruction_data_discriminator(instruction)
            name = discriminator_to_name.get(discriminator or "", "unknown")
            role_spec = instruction_map.get(name, {"idl_role_count": 0, "roles": []})
            accounts = instruction_accounts(instruction)
            observations.append(
                {
                    "observation_id": sha256_text(f"{signature}:{group_name}:{instruction_index}"),
                    "signature_hash": sha256_text(signature),
                    "slot": transaction.get("slot"),
                    "block_time": transaction.get("blockTime"),
                    "instruction_group": group_name,
                    "instruction_index": instruction_index,
                    "instruction_name": name,
                    "instruction_discriminator_hex": discriminator,
                    "discriminator_derivation": discriminator_derivations.get(discriminator or ""),
                    "matched_onchain_idl_instruction": name != "unknown",
                    "account_index_count": len(accounts),
                    "idl_role_count": role_spec["idl_role_count"],
                    "role_count_matches_observed_accounts": len(accounts) == role_spec["idl_role_count"],
                    "bound_role_count": min(len(accounts), role_spec["idl_role_count"]),
                    "role_bindings": scrubbed_role_bindings(
                        accounts, account_keys, role_spec["roles"], metadata
                    )[:40],
                    "role_bindings_truncated": min(len(accounts), role_spec["idl_role_count"]) > 40,
                    "raw_instruction_data_committed": False,
                    "raw_transaction_committed": False,
                }
            )
    return observations


def build_report(rpc_url: str, idl: dict[str, Any], limit: int, transaction_limit: int) -> dict[str, Any]:
    discriminator_to_name, discriminator_derivations, instruction_map = idl_instruction_maps(idl)
    signatures = rpc_call(
        rpc_url,
        "getSignaturesForAddress",
        [JUPITER_PERPS_PROGRAM_ID, {"commitment": "confirmed", "limit": limit}],
    )
    if not isinstance(signatures, list):
        signatures = []

    transactions: list[tuple[str, dict[str, Any]]] = []
    for row in signatures[:transaction_limit]:
        signature = row.get("signature") if isinstance(row, dict) else None
        if not isinstance(signature, str):
            continue
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
        if isinstance(transaction, dict):
            transactions.append((signature, transaction))

    role_account_keys = sorted(
        {
            key
            for _, transaction in transactions
            for key in message_account_keys(transaction)
            if key and key != JUPITER_PERPS_PROGRAM_ID
        }
    )
    metadata = account_metadata_batch(rpc_url, role_account_keys)
    observations = [
        item
        for signature, transaction in transactions
        for item in collect_jupiter_instructions(
            transaction,
            signature,
            discriminator_to_name,
            discriminator_derivations,
            instruction_map,
            metadata,
        )
    ]
    counts: dict[str, int] = {}
    for observation in observations:
        name = observation["instruction_name"]
        counts[name] = counts.get(name, 0) + 1

    return {
        "schema_version": "oprs.jupiter_lifecycle_role_map_probe.v0",
        "dataset_name": "jupiter_lifecycle_role_map_probe_local",
        "protocol": "jupiter_perps",
        "chain_id": "solana-mainnet-beta",
        "generated_at_unix": int(time.time()),
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "generated_by": "scripts/discover_jupiter_lifecycle_role_map.py",
        "source_authority": {
            "program_id": JUPITER_PERPS_PROGRAM_ID,
            "role_map_source": "onchain_anchor_idl_instruction_accounts",
            "account_layout_source": "onchain_anchor_idl_accounts",
            "official_docs_context": [
                JUPITER_POSITION_REQUEST_DOCS,
                JUPITER_POSITION_DOCS,
                JUPITER_TECHNICAL_REFERENCE,
            ],
        },
        "query": {
            "commitment": "confirmed",
            "signature_limit": limit,
            "transaction_limit": transaction_limit,
            "methods": ["getSignaturesForAddress", "getTransaction", "getMultipleAccounts"],
            "account_metadata_data_slice_len": 0,
        },
        "instruction_summary": {
            "idl_instruction_count": len(instruction_map),
            "sampled_signature_count": len(signatures),
            "sampled_transaction_count": len(transactions),
            "jupiter_instruction_observation_count": len(observations),
            "matched_instruction_counts": dict(sorted(counts.items())),
            "unmatched_instruction_count": counts.get("unknown", 0),
            "discriminator_derivations": sorted(set(discriminator_derivations.values())),
        },
        "role_map_observations": observations,
        "readiness": {
            "live_rpc_read_claimed": True,
            "instruction_account_role_maps_from_idl": True,
            "transaction_role_bindings_observed": True,
            "verified_request_fulfillment_pair_claimed": False,
            "position_request_state_transition_claimed": False,
            "keeper_semantics_claimed": False,
            "liquidation_replay_claimed": False,
            "execution_claimed": False,
            "raw_transaction_committed": False,
            "raw_instruction_data_committed": False,
            "raw_account_bytes_committed": False,
            "account_pubkeys_committed": False,
        },
        "known_limitations": [
            "Role maps are read from the onchain IDL instruction account list, not a Jupiter-written lifecycle explainer.",
            "Observed bindings are hashed/local summaries and are not published as verified request/fulfillment pairs.",
            "The probe does not decode before/after account state for transaction lifecycle transitions.",
            "A role-count match is structural evidence only; it is not keeper behavior, replay readiness, liquidation opportunity detection, or production readiness.",
        ],
        "forbidden_actions": [
            "sign",
            "submit_transaction",
            "load_keypair",
            "bid_priority_fee",
            "manage_capital",
            "call_order_endpoint",
            "call_execute_endpoint",
            "call_build_endpoint",
            "call_submit_endpoint",
            "call_auth_endpoint",
            "keeper_operation",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", default=".env")
    parser.add_argument("--idl", default=DEFAULT_IDL)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--limit", type=int, default=40)
    parser.add_argument("--transaction-limit", type=int, default=20)
    args = parser.parse_args()

    if args.limit < 1 or args.limit > 100:
        print("--limit must be between 1 and 100.")
        return 2
    if args.transaction_limit < 0 or args.transaction_limit > args.limit:
        print("--transaction-limit must be between 0 and --limit.")
        return 2

    load_dotenv(Path(args.env_file))
    rpc_url = os.environ.get("HELIUS_RPC_URL")
    if not rpc_url:
        print("HELIUS_RPC_URL is required in local .env or environment.")
        return 2
    if not rpc_url.startswith("https://"):
        print("HELIUS_RPC_URL must be an HTTPS RPC URL.")
        return 2

    idl_path = Path(args.idl)
    if not idl_path.exists():
        print(f"Missing local IDL at {idl_path}; run scripts/fetch_jupiter_onchain_idl.py first.")
        return 2
    idl = json.loads(idl_path.read_text(encoding="utf-8"))
    report = build_report(rpc_url, idl, args.limit, args.transaction_limit)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote scrubbed local Jupiter lifecycle role-map probe to {out_path}")
    print("No RPC URL, API key, wallet secret, raw transaction, instruction data, or account bytes were committed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
