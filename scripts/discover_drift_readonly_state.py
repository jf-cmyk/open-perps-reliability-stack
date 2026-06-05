#!/usr/bin/env python3
"""Discover public Drift state, market, and oracle metadata through read-only RPC.

This command intentionally writes only scrubbed public metadata. It must never
print HELIUS_RPC_URL or any other RPC credential.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DRIFT_PROGRAM_ID = "dRiftyHA39MWEi3m9aunc5MzRF1JYuBsbn6VPcn33UH"
DRIFT_PROGRAM_BYTES = None
DRIFT_PROTOCOL_V2_COMMIT = "0ae3e3b1db782a6765c3525b3dec38ad4d9d3a62"
DRIFT_SDK_VERSION = "2.163.0-beta.0"
DRIFT_IDL_BLOB_SHA = "9646dd6a893568d85d8dc47507e047010bf7e945"

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
BASE58_INDEX = {char: index for index, char in enumerate(BASE58_ALPHABET)}
PDA_MARKER = b"ProgramDerivedAddress"

ED25519_P = 2**255 - 19
ED25519_D = (-121665 * pow(121666, ED25519_P - 2, ED25519_P)) % ED25519_P

DRIFT_SDK_SOURCE = f"https://github.com/drift-labs/protocol-v2/blob/{DRIFT_PROTOCOL_V2_COMMIT}/sdk/src/addresses/pda.ts"
DRIFT_PERP_CONSTANTS_SOURCE = f"https://github.com/drift-labs/protocol-v2/blob/{DRIFT_PROTOCOL_V2_COMMIT}/sdk/src/constants/perpMarkets.ts"
DRIFT_SPOT_CONSTANTS_SOURCE = f"https://github.com/drift-labs/protocol-v2/blob/{DRIFT_PROTOCOL_V2_COMMIT}/sdk/src/constants/spotMarkets.ts"
DRIFT_IDL_SOURCE = f"https://github.com/drift-labs/protocol-v2/blob/{DRIFT_PROTOCOL_V2_COMMIT}/sdk/src/idl/drift.json"
DRIFT_ACCOUNT_FETCH_SOURCE = f"https://github.com/drift-labs/protocol-v2/blob/{DRIFT_PROTOCOL_V2_COMMIT}/sdk/src/accounts/fetch.ts"
DRIFT_ACCOUNT_MODEL_SOURCE = "https://docs.drift.trade/developers/concepts/account-model"

EXPECTED_ACCOUNT_TYPES = {
    "state_account": "State",
    "perp_market_account": "PerpMarket",
    "spot_market_account": "SpotMarket",
}

PERP_MARKETS = [
    {
        "symbol": "SOL-PERP",
        "base_asset_symbol": "SOL",
        "market_index": 0,
        "oracle": "3m6i4RFWEDw2Ft4tFHPJtYgmpPe21k56M3FHeWYrgGBz",
        "oracle_source": "PYTH_LAZER",
        "pyth_feed_id": "0xef0d8b6fda2ceba41da15d4095d1da392a0d2f8ed0c6c7bc0f4cfac8c280b56d",
    },
    {
        "symbol": "BTC-PERP",
        "base_asset_symbol": "BTC",
        "market_index": 1,
        "oracle": "35MbvS1Juz2wf7GsyHrkCw8yfKciRLxVpEhfZDZFrB4R",
        "oracle_source": "PYTH_LAZER",
        "pyth_feed_id": "0xe62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43",
    },
    {
        "symbol": "ETH-PERP",
        "base_asset_symbol": "ETH",
        "market_index": 2,
        "oracle": "93FG52TzNKCnMiasV14Ba34BYcHDb9p4zK4GjZnLwqWR",
        "oracle_source": "PYTH_LAZER",
        "pyth_feed_id": "0xff61491a931112ddf1bd8147cd1b641375f79f5825126d665480874634fd0ace",
    },
]

SPOT_MARKETS = [
    {
        "symbol": "USDC",
        "market_index": 0,
        "pool_id": 0,
        "oracle": "9VCioxmni2gDLv11qufWzT3RDERhQE4iY5Gf7NTfYyAV",
        "oracle_source": "PYTH_LAZER_STABLE_COIN",
        "mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        "pyth_feed_id": "0xeaa020c61cc479712813461ce153894a96a6c00b21ed0cfc2798d1f9a9e9c94a",
    },
    {
        "symbol": "SOL",
        "market_index": 1,
        "pool_id": 0,
        "oracle": "3m6i4RFWEDw2Ft4tFHPJtYgmpPe21k56M3FHeWYrgGBz",
        "oracle_source": "PYTH_LAZER",
        "mint": "So11111111111111111111111111111111111111112",
        "pyth_feed_id": "0xef0d8b6fda2ceba41da15d4095d1da392a0d2f8ed0c6c7bc0f4cfac8c280b56d",
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


def b58decode(value: str) -> bytes:
    number = 0
    for char in value:
        number = number * 58 + BASE58_INDEX[char]
    raw = number.to_bytes((number.bit_length() + 7) // 8, "big") if number else b""
    leading_zeroes = len(value) - len(value.lstrip("1"))
    return b"\x00" * leading_zeroes + raw


def b58encode(raw: bytes) -> str:
    number = int.from_bytes(raw, "big")
    encoded = ""
    while number:
        number, remainder = divmod(number, 58)
        encoded = BASE58_ALPHABET[remainder] + encoded
    leading_zeroes = len(raw) - len(raw.lstrip(b"\x00"))
    return "1" * leading_zeroes + (encoded or "")


def is_ed25519_curve_point(compressed: bytes) -> bool:
    if len(compressed) != 32:
        return False
    y = int.from_bytes(compressed, "little") & ((1 << 255) - 1)
    sign = compressed[31] >> 7
    if y >= ED25519_P:
        return False
    y2 = (y * y) % ED25519_P
    numerator = (y2 - 1) % ED25519_P
    denominator = (ED25519_D * y2 + 1) % ED25519_P
    if denominator == 0:
        return False
    x2 = (numerator * pow(denominator, ED25519_P - 2, ED25519_P)) % ED25519_P
    if x2 == 0:
        return sign == 0
    return pow(x2, (ED25519_P - 1) // 2, ED25519_P) == 1


def find_program_address(seeds: list[bytes], program_id: str) -> tuple[str, int]:
    program_bytes = b58decode(program_id)
    if len(program_bytes) != 32:
        raise ValueError("program id must decode to 32 bytes")
    for bump in range(255, -1, -1):
        digest = hashlib.sha256(b"".join(seeds + [bytes([bump])]) + program_bytes + PDA_MARKER).digest()
        if not is_ed25519_curve_point(digest):
            return b58encode(digest), bump
    raise ValueError("unable to find program address")


def u16_le(value: int) -> bytes:
    return value.to_bytes(2, "little")


def rpc_call(rpc_url: str, method: str, params: list[Any] | None = None) -> Any:
    body = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": "oprs-drift-readonly-state",
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


def anchor_account_discriminator(account_type: str) -> bytes:
    return hashlib.sha256(f"account:{account_type}".encode("utf-8")).digest()[:8]


def account_shape_snapshot(rpc_url: str, target: dict[str, Any]) -> dict[str, Any]:
    account_type = EXPECTED_ACCOUNT_TYPES.get(target["target_kind"])
    if account_type is None:
        raise ValueError(f"unsupported shape snapshot target kind: {target['target_kind']}")

    result = rpc_call(
        rpc_url,
        "getAccountInfo",
        [
            target["address"],
            {
                "commitment": "confirmed",
                "encoding": "base64",
            },
        ],
    )
    context = result.get("context", {}) if isinstance(result, dict) else {}
    value = result.get("value") if isinstance(result, dict) else None
    if value is None:
        return {
            "readiness": "target_missing",
            "context_slot": context.get("slot"),
            "raw_account_data_committed": False,
        }

    data_value = value.get("data")
    if not isinstance(data_value, list) or not data_value:
        raise SystemExit(f"RPC account data had unexpected shape for {target['target_id']}")

    raw = base64.b64decode(data_value[0])
    observed_discriminator = raw[:8]
    expected_discriminator = anchor_account_discriminator(account_type)

    return {
        "readiness": "shape_snapshot_only",
        "decode_level": "anchor_discriminator_and_data_length",
        "context_slot": context.get("slot"),
        "expected_account_type": account_type,
        "expected_anchor_discriminator_hex": expected_discriminator.hex(),
        "observed_anchor_discriminator_hex": observed_discriminator.hex(),
        "discriminator_match": observed_discriminator == expected_discriminator,
        "data_length": len(raw),
        "account_data_sha256": hashlib.sha256(raw).hexdigest(),
        "owner": value.get("owner"),
        "executable": value.get("executable"),
        "raw_account_data_committed": False,
        "field_decode_claimed": False,
        "replay_ready": False,
        "source_commit": DRIFT_PROTOCOL_V2_COMMIT,
        "idl_blob_sha": DRIFT_IDL_BLOB_SHA,
    }


def pda_target(target_id: str, target_kind: str, seeds: list[bytes], source: str) -> dict[str, Any]:
    address, bump = find_program_address(seeds, DRIFT_PROGRAM_ID)
    return {
        "target_id": target_id,
        "protocol": "drift",
        "target_kind": target_kind,
        "address": address,
        "pda": {
            "program_id": DRIFT_PROGRAM_ID,
            "bump": bump,
            "source": source,
        },
    }


def attach_shape_snapshot(rpc_url: str, target: dict[str, Any]) -> None:
    if target["target_kind"] in EXPECTED_ACCOUNT_TYPES:
        target["shape_snapshot"] = account_shape_snapshot(rpc_url, target)
        target["readiness"] = "shape_snapshot_only"


def build_report(rpc_url: str, include_shape_snapshot: bool = False) -> dict[str, Any]:
    observed_slot = rpc_call(rpc_url, "getSlot", [{"commitment": "confirmed"}])
    now = int(time.time())

    targets: list[dict[str, Any]] = []

    state = pda_target(
        "drift_state",
        "state_account",
        [b"drift_state"],
        DRIFT_SDK_SOURCE,
    )
    state["readiness"] = "target_discovered"
    state["probe"] = account_probe(rpc_url, state["address"])
    if include_shape_snapshot:
        attach_shape_snapshot(rpc_url, state)
    targets.append(state)

    oracle_addresses: dict[str, dict[str, Any]] = {}

    for market in PERP_MARKETS:
        target = pda_target(
            f"drift_perp_market_{market['market_index']}_{market['symbol'].lower().replace('-', '_')}",
            "perp_market_account",
            [b"perp_market", u16_le(market["market_index"])],
            DRIFT_SDK_SOURCE,
        )
        target.update(
            {
                "readiness": "target_discovered",
                "market": market,
                "probe": account_probe(rpc_url, target["address"]),
            }
        )
        if include_shape_snapshot:
            attach_shape_snapshot(rpc_url, target)
        targets.append(target)
        oracle_addresses[market["oracle"]] = {
            "oracle": market["oracle"],
            "oracle_source": market["oracle_source"],
            "pyth_feed_id": market["pyth_feed_id"],
            "used_by": oracle_addresses.get(market["oracle"], {}).get("used_by", []) + [market["symbol"]],
        }

    for market in SPOT_MARKETS:
        target = pda_target(
            f"drift_spot_market_{market['market_index']}_{market['symbol'].lower()}",
            "spot_market_account",
            [b"spot_market", u16_le(market["market_index"])],
            DRIFT_SDK_SOURCE,
        )
        target.update(
            {
                "readiness": "target_discovered",
                "market": market,
                "probe": account_probe(rpc_url, target["address"]),
            }
        )
        if include_shape_snapshot:
            attach_shape_snapshot(rpc_url, target)
        targets.append(target)
        oracle_addresses[market["oracle"]] = {
            "oracle": market["oracle"],
            "oracle_source": market["oracle_source"],
            "pyth_feed_id": market["pyth_feed_id"],
            "used_by": oracle_addresses.get(market["oracle"], {}).get("used_by", []) + [market["symbol"]],
        }

    for address, oracle in sorted(oracle_addresses.items()):
        targets.append(
            {
                "target_id": f"drift_oracle_{address}",
                "protocol": "drift",
                "target_kind": "oracle_account",
                "address": address,
                "readiness": "target_discovered",
                "oracle": oracle,
                "source": {
                    "perp_constants": DRIFT_PERP_CONSTANTS_SOURCE,
                    "spot_constants": DRIFT_SPOT_CONSTANTS_SOURCE,
                },
                "probe": account_probe(rpc_url, address),
            }
        )

    methods = ["getSlot"] + ["getAccountInfo"] * len(targets)
    if include_shape_snapshot:
        methods.extend(["getAccountInfo"] * sum(1 for target in targets if target["target_kind"] in EXPECTED_ACCOUNT_TYPES))

    return {
        "schema_version": "0.1.0",
        "report_id": "drift_readonly_state_discovery",
        "generated_at_unix": now,
        "generated_by": "scripts/discover_drift_readonly_state.py",
        "rpc": {
            "provider_label": "local_readonly_rpc_env",
            "credential_printed": False,
            "commitment": "confirmed",
            "observed_slot": observed_slot,
        },
        "source_refs": {
            "account_model": DRIFT_ACCOUNT_MODEL_SOURCE,
            "pda_helpers": DRIFT_SDK_SOURCE,
            "perp_market_constants": DRIFT_PERP_CONSTANTS_SOURCE,
            "spot_market_constants": DRIFT_SPOT_CONSTANTS_SOURCE,
            "drift_idl": DRIFT_IDL_SOURCE,
            "account_fetch_helpers": DRIFT_ACCOUNT_FETCH_SOURCE,
        },
        "decoder_provenance": {
            "protocol_repo": "drift-labs/protocol-v2",
            "protocol_repo_commit": DRIFT_PROTOCOL_V2_COMMIT,
            "sdk_version": DRIFT_SDK_VERSION,
            "drift_idl_source": DRIFT_IDL_SOURCE,
            "drift_idl_blob_sha": DRIFT_IDL_BLOB_SHA,
            "decode_status": "shape_snapshot_only" if include_shape_snapshot else "target_discovered_not_binary_decoded",
            "shape_snapshot_included": include_shape_snapshot,
            "shape_snapshot_scope": "account discriminator, account data length, account data SHA-256, and expected IDL account type only",
            "next_safe_decode_step": "public market fields only after field offsets are validated against the pinned IDL or SDK decoder",
        },
        "targets": targets,
        "data_reconstruction_envelope": {
            "schema_version": "0.1.0",
            "envelope_id": "drift_readonly_state_reconstruction",
            "dataset_name": "drift_readonly_state_discovery",
            "chain_id": "solana-mainnet-beta",
            "protocol": "drift",
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
                    "source_id": "drift_protocol_v2_sdk_constants",
                    "source_kind": "public_repository",
                    "provider_label": "drift_labs_protocol_v2",
                    "commitment": "not_applicable",
                    "lifecycle_stage": "target_resolution",
                    "retention_boundary": "public_git_history",
                    "source_revision": DRIFT_PROTOCOL_V2_COMMIT,
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
                "target/oprs-drift-readonly-state/latest.json"
            ],
            "known_gaps": [
                "Shape snapshot mode decodes only account discriminator and account data length; it does not decode market economics, user state, or liquidation pre-state.",
                "No user account, pre-state, transaction history, or liquidation event reconstruction is performed.",
                "Jupiter Perps pool/custody/oracle targets remain a separate proof lane.",
            ],
            "source_limitations": [
                "Drift market/oracle targets are resolved from public SDK constants and PDA helper source.",
                "RPC retention and provider backfill limits are not assessed in this metadata probe.",
                "Oracle account binary data is not decoded in this command.",
                "Raw account bytes are used in memory for shape checks only and are not written to output.",
            ],
            "generated_at_unix": now,
            "generated_by": "scripts/discover_drift_readonly_state.py",
        },
        "forbidden_actions": [
            "sign",
            "submit_transaction",
            "retry_transaction",
            "bid_priority_fee",
            "load_keypair",
            "manage_capital",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", default=".env")
    parser.add_argument(
        "--out",
        default="target/oprs-drift-readonly-state/latest.json",
        help="Output path for scrubbed Drift read-only state report.",
    )
    parser.add_argument(
        "--include-shape-snapshot",
        action="store_true",
        help="Fetch raw account bytes in memory and emit only discriminator/data-length shape checks.",
    )
    args = parser.parse_args()

    load_dotenv(Path(args.env_file))
    rpc_url = os.environ.get("HELIUS_RPC_URL")
    if not rpc_url:
        print("HELIUS_RPC_URL is not configured; Drift state discovery skipped.", file=sys.stderr)
        return 2
    if not rpc_url.startswith("https://"):
        print("HELIUS_RPC_URL must be an HTTPS RPC URL.", file=sys.stderr)
        return 2

    report = build_report(rpc_url, include_shape_snapshot=args.include_shape_snapshot)
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"Wrote scrubbed Drift read-only state report to {output_path}")
    print("HELIUS_RPC_URL loaded locally and was not printed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
