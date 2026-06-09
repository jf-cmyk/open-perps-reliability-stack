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
DRIFT_PERP_MARKET_SOURCE = f"https://github.com/drift-labs/protocol-v2/blob/{DRIFT_PROTOCOL_V2_COMMIT}/programs/drift/src/state/perp_market.rs"
DRIFT_SPOT_MARKET_SOURCE = f"https://github.com/drift-labs/protocol-v2/blob/{DRIFT_PROTOCOL_V2_COMMIT}/programs/drift/src/state/spot_market.rs"
DRIFT_PAUSED_OPERATIONS_SOURCE = f"https://github.com/drift-labs/protocol-v2/blob/{DRIFT_PROTOCOL_V2_COMMIT}/programs/drift/src/state/paused_operations.rs"

EXPECTED_ACCOUNT_TYPES = {
    "state_account": "State",
    "perp_market_account": "PerpMarket",
    "spot_market_account": "SpotMarket",
}

MARKET_STATUS_LABELS = {
    0: "Initialized",
    1: "Active",
    2: "FundingPaused",
    3: "AmmPaused",
    4: "FillPaused",
    5: "WithdrawPaused",
    6: "ReduceOnly",
    7: "Settlement",
    8: "Delisted",
}

ASSET_TIER_LABELS = {
    0: "Collateral",
    1: "Protected",
    2: "Cross",
    3: "Isolated",
    4: "Unlisted",
}

CONTRACT_TYPE_LABELS = {
    0: "Perpetual",
    1: "Future",
    2: "Prediction",
}

CONTRACT_TIER_LABELS = {
    0: "A",
    1: "B",
    2: "C",
    3: "Speculative",
    4: "HighlySpeculative",
    5: "Isolated",
}

PERP_OPERATION_BITS = {
    0b00000001: "UpdateFunding",
    0b00000010: "AmmFill",
    0b00000100: "Fill",
    0b00001000: "SettlePnl",
    0b00010000: "SettlePnlWithPosition",
    0b00100000: "Liquidation",
    0b01000000: "AmmImmediateFill",
    0b10000000: "SettleRevPool",
}

SPOT_OPERATION_BITS = {
    0b00000001: "UpdateCumulativeInterest",
    0b00000010: "Fill",
    0b00000100: "Deposit",
    0b00001000: "Withdraw",
    0b00010000: "Liquidation",
}

INSURANCE_FUND_OPERATION_BITS = {
    0b00000001: "Init",
    0b00000010: "Add",
    0b00000100: "RequestRemove",
    0b00001000: "Remove",
}

PUBLIC_FIELD_LAYOUTS = {
    "state_account": [
        {
            "name": "admin",
            "type": "publicKey",
            "offset": 8,
            "length": 32,
            "source_field": "State.admin",
        },
        {
            "name": "signer",
            "type": "publicKey",
            "offset": 104,
            "length": 32,
            "source_field": "State.signer",
        },
    ],
    "perp_market_account": [
        {
            "name": "pubkey",
            "type": "publicKey",
            "offset": 8,
            "length": 32,
            "source_field": "PerpMarket.pubkey",
            "expected_from": "target_address",
        },
        {
            "name": "market_index",
            "type": "u16",
            "offset": 1160,
            "length": 2,
            "source_field": "PerpMarket.market_index",
            "expected_from": "market.market_index",
        },
        {
            "name": "status",
            "type": "u8",
            "offset": 1162,
            "length": 1,
            "source_field": "PerpMarket.status",
        },
        {
            "name": "contract_type",
            "type": "u8",
            "offset": 1163,
            "length": 1,
            "source_field": "PerpMarket.contract_type",
        },
        {
            "name": "contract_tier",
            "type": "u8",
            "offset": 1164,
            "length": 1,
            "source_field": "PerpMarket.contract_tier",
        },
        {
            "name": "paused_operations",
            "type": "u8",
            "offset": 1165,
            "length": 1,
            "source_field": "PerpMarket.paused_operations",
        },
    ],
    "spot_market_account": [
        {
            "name": "pubkey",
            "type": "publicKey",
            "offset": 8,
            "length": 32,
            "source_field": "SpotMarket.pubkey",
            "expected_from": "target_address",
        },
        {
            "name": "oracle",
            "type": "publicKey",
            "offset": 40,
            "length": 32,
            "source_field": "SpotMarket.oracle",
            "expected_from": "market.oracle",
        },
        {
            "name": "mint",
            "type": "publicKey",
            "offset": 72,
            "length": 32,
            "source_field": "SpotMarket.mint",
            "expected_from": "market.mint",
        },
        {
            "name": "vault",
            "type": "publicKey",
            "offset": 104,
            "length": 32,
            "source_field": "SpotMarket.vault",
        },
        {
            "name": "name",
            "type": "bytes32String",
            "offset": 136,
            "length": 32,
            "source_field": "SpotMarket.name",
            "expected_from": "market.symbol",
        },
        {
            "name": "decimals",
            "type": "u32",
            "offset": 680,
            "length": 4,
            "source_field": "SpotMarket.decimals",
            "expected_from": "market.decimals",
        },
        {
            "name": "market_index",
            "type": "u16",
            "offset": 684,
            "length": 2,
            "source_field": "SpotMarket.market_index",
            "expected_from": "market.market_index",
        },
        {
            "name": "orders_enabled",
            "type": "bool",
            "offset": 686,
            "length": 1,
            "source_field": "SpotMarket.orders_enabled",
        },
        {
            "name": "status",
            "type": "u8",
            "offset": 688,
            "length": 1,
            "source_field": "SpotMarket.status",
        },
        {
            "name": "asset_tier",
            "type": "u8",
            "offset": 689,
            "length": 1,
            "source_field": "SpotMarket.asset_tier",
        },
        {
            "name": "paused_operations",
            "type": "u8",
            "offset": 690,
            "length": 1,
            "source_field": "SpotMarket.paused_operations",
        },
        {
            "name": "if_paused_operations",
            "type": "u8",
            "offset": 691,
            "length": 1,
            "source_field": "SpotMarket.if_paused_operations",
        },
        {
            "name": "pool_id",
            "type": "u8",
            "offset": 735,
            "length": 1,
            "source_field": "SpotMarket.pool_id",
            "expected_from": "market.pool_id",
        },
    ],
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
        "decimals": 6,
        "pyth_feed_id": "0xeaa020c61cc479712813461ce153894a96a6c00b21ed0cfc2798d1f9a9e9c94a",
    },
    {
        "symbol": "SOL",
        "market_index": 1,
        "pool_id": 0,
        "oracle": "3m6i4RFWEDw2Ft4tFHPJtYgmpPe21k56M3FHeWYrgGBz",
        "oracle_source": "PYTH_LAZER",
        "mint": "So11111111111111111111111111111111111111112",
        "decimals": 9,
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


def expected_field_value(target: dict[str, Any], expected_from: str | None) -> Any:
    if expected_from is None:
        return None
    if expected_from == "target_address":
        return target["address"]
    if expected_from.startswith("market."):
        market = target.get("market", {})
        return market.get(expected_from.split(".", 1)[1])
    return None


def active_operation_labels(value: int, operation_bits: dict[int, str]) -> list[str]:
    return [label for bit, label in operation_bits.items() if value & bit]


def semantic_public_field(target_kind: str, field_name: str, value: Any) -> dict[str, Any]:
    if field_name == "status":
        return {
            "semantic_value": MARKET_STATUS_LABELS.get(value, "Unknown"),
            "semantic_source": DRIFT_PERP_MARKET_SOURCE,
        }
    if field_name == "contract_type":
        return {
            "semantic_value": CONTRACT_TYPE_LABELS.get(value, "Unknown"),
            "semantic_source": DRIFT_PERP_MARKET_SOURCE,
        }
    if field_name == "contract_tier":
        return {
            "semantic_value": CONTRACT_TIER_LABELS.get(value, "Unknown"),
            "semantic_source": DRIFT_PERP_MARKET_SOURCE,
        }
    if field_name == "asset_tier":
        return {
            "semantic_value": ASSET_TIER_LABELS.get(value, "Unknown"),
            "semantic_source": DRIFT_SPOT_MARKET_SOURCE,
        }
    if field_name == "paused_operations":
        operation_bits = (
            PERP_OPERATION_BITS
            if target_kind == "perp_market_account"
            else SPOT_OPERATION_BITS
        )
        return {
            "semantic_value": active_operation_labels(value, operation_bits),
            "semantic_encoding": "bitset",
            "semantic_source": DRIFT_PAUSED_OPERATIONS_SOURCE,
        }
    if field_name == "if_paused_operations":
        return {
            "semantic_value": active_operation_labels(value, INSURANCE_FUND_OPERATION_BITS),
            "semantic_encoding": "bitset",
            "semantic_source": DRIFT_PAUSED_OPERATIONS_SOURCE,
        }
    return {}


def decode_public_fields(raw: bytes, target: dict[str, Any]) -> dict[str, Any]:
    layout = PUBLIC_FIELD_LAYOUTS.get(target["target_kind"], [])
    decoded = []
    validation_failures = []
    for field in layout:
        offset = field["offset"]
        length = field["length"]
        if offset + length > len(raw):
            validation_failures.append(f"{field['name']}:offset_out_of_bounds")
            continue

        field_bytes = raw[offset : offset + length]
        if field["type"] == "publicKey":
            value = b58encode(field_bytes)
        elif field["type"] == "bytes32String":
            value = field_bytes.decode("utf-8", errors="replace").rstrip("\x00 ")
        elif field["type"] == "u32":
            value = int.from_bytes(field_bytes, "little", signed=False)
        elif field["type"] == "u16":
            value = int.from_bytes(field_bytes, "little", signed=False)
        elif field["type"] == "u8":
            value = int.from_bytes(field_bytes, "little", signed=False)
        elif field["type"] == "bool":
            value = field_bytes != b"\x00"
        else:
            validation_failures.append(f"{field['name']}:unsupported_type")
            continue

        expected = expected_field_value(target, field.get("expected_from"))
        matches_expected = expected is None or value == expected
        if not matches_expected:
            validation_failures.append(f"{field['name']}:expected_mismatch")

        decoded_field = {
            "field": field["name"],
            "source_field": field["source_field"],
            "type": field["type"],
            "offset": offset,
            "length": length,
            "value": value,
            "expected": expected,
            "matches_expected": matches_expected,
        }
        decoded_field.update(semantic_public_field(target["target_kind"], field["name"], value))
        decoded.append(decoded_field)

    return {
        "readiness": "public_fields_decoded",
        "decode_level": "offset_validated_public_identity_metadata_guardrail_fields",
        "source_commit": DRIFT_PROTOCOL_V2_COMMIT,
        "idl_blob_sha": DRIFT_IDL_BLOB_SHA,
        "offset_source": "pinned Drift Rust repr(C) account field order and Anchor discriminator prefix",
        "semantic_source_scope": "MarketStatus, AssetTier, SpotOperation, and InsuranceFundOperation labels from pinned Drift Rust source",
        "fields": decoded,
        "validation_failures": validation_failures,
        "field_decode_claimed": len(decoded) > 0 and not validation_failures,
        "user_state_decoded": False,
        "market_economics_decoded": False,
        "replay_ready": False,
    }


def account_shape_snapshot(rpc_url: str, target: dict[str, Any], include_public_fields: bool = False) -> dict[str, Any]:
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

    snapshot = {
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
    if include_public_fields and snapshot["discriminator_match"]:
        snapshot["public_field_decode"] = decode_public_fields(raw, target)
        if snapshot["public_field_decode"]["field_decode_claimed"]:
            snapshot["readiness"] = "public_fields_decoded"
            snapshot["decode_level"] = "anchor_discriminator_data_length_and_public_fields"
            snapshot["field_decode_claimed"] = True
    return snapshot


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


def attach_shape_snapshot(rpc_url: str, target: dict[str, Any], include_public_fields: bool = False) -> None:
    if target["target_kind"] in EXPECTED_ACCOUNT_TYPES:
        target["shape_snapshot"] = account_shape_snapshot(rpc_url, target, include_public_fields)
        target["readiness"] = target["shape_snapshot"]["readiness"]


def build_report(rpc_url: str, include_shape_snapshot: bool = False, include_public_fields: bool = False) -> dict[str, Any]:
    if include_public_fields:
        include_shape_snapshot = True
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
        attach_shape_snapshot(rpc_url, state, include_public_fields)
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
            attach_shape_snapshot(rpc_url, target, include_public_fields)
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
            attach_shape_snapshot(rpc_url, target, include_public_fields)
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
            "perp_market_state": DRIFT_PERP_MARKET_SOURCE,
            "spot_market_state": DRIFT_SPOT_MARKET_SOURCE,
            "paused_operations_state": DRIFT_PAUSED_OPERATIONS_SOURCE,
        },
        "decoder_provenance": {
            "protocol_repo": "drift-labs/protocol-v2",
            "protocol_repo_commit": DRIFT_PROTOCOL_V2_COMMIT,
            "sdk_version": DRIFT_SDK_VERSION,
            "drift_idl_source": DRIFT_IDL_SOURCE,
            "drift_idl_blob_sha": DRIFT_IDL_BLOB_SHA,
            "decode_status": (
                "public_fields_decoded"
                if include_public_fields
                else "shape_snapshot_only"
                if include_shape_snapshot
                else "target_discovered_not_binary_decoded"
            ),
            "shape_snapshot_included": include_shape_snapshot,
            "shape_snapshot_scope": "account discriminator, account data length, account data SHA-256, and expected IDL account type only",
            "public_field_decode_included": include_public_fields,
            "public_field_decode_scope": "State admin/signer, PerpMarket pubkey, and selected SpotMarket identity/metadata/guardrail fields with source-backed guardrail labels only",
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
                "Shape snapshot mode decodes only account discriminator and account data length; optional public-field mode decodes selected identity and spot metadata fields.",
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
    parser.add_argument(
        "--include-public-fields",
        action="store_true",
        help="Also emit offset-validated public identity and spot metadata fields from selected Drift accounts.",
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

    report = build_report(
        rpc_url,
        include_shape_snapshot=args.include_shape_snapshot,
        include_public_fields=args.include_public_fields,
    )
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"Wrote scrubbed Drift read-only state report to {output_path}")
    print("HELIUS_RPC_URL loaded locally and was not printed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
