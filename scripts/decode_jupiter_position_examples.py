#!/usr/bin/env python3
"""Decode public Jupiter docs example Position and PositionRequest accounts.

This command uses the local onchain Anchor IDL fetched by
scripts/fetch_jupiter_onchain_idl.py and reads only the public Solana accounts
linked from Jupiter's official docs. It emits scrubbed decoded fields and does
not sign, build, or submit transactions.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import struct
import time
import urllib.request
from pathlib import Path
from typing import Any

from fetch_jupiter_onchain_idl import JUPITER_PERPS_PROGRAM_ID, b58encode, load_dotenv, rpc_call


DOCS_POSITION_ACCOUNT = "FBLzd5VM67MEKkoWerXu7Nu1ksbLXQvJDx63y5aeLEvt"
DOCS_POSITION_REQUEST_ACCOUNT = "DNnX2B1oiYqKLrbLLod1guuaZA28DQwJ8HuHsgDafoQK"
PUBLIC_DOCS = {
    "position": "https://developers.jup.ag/docs/perps/position-account",
    "position_request": "https://developers.jup.ag/docs/perps/position-request-account",
}


class Reader:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.offset = 8

    def take(self, size: int) -> bytes:
        if self.offset + size > len(self.data):
            raise ValueError(f"read past end at offset {self.offset}, size {size}")
        out = self.data[self.offset : self.offset + size]
        self.offset += size
        return out

    def pubkey(self) -> str:
        return b58encode(self.take(32))

    def u8(self) -> int:
        return self.take(1)[0]

    def bool(self) -> bool:
        value = self.u8()
        if value not in (0, 1):
            raise ValueError(f"invalid bool value {value} at offset {self.offset - 1}")
        return value == 1

    def i64(self) -> int:
        return struct.unpack("<q", self.take(8))[0]

    def u64(self) -> int:
        return struct.unpack("<Q", self.take(8))[0]

    def u128(self) -> int:
        return int.from_bytes(self.take(16), "little", signed=False)

    def option(self, inner: str) -> Any:
        tag = self.u8()
        if tag == 0:
            return None
        if tag != 1:
            raise ValueError(f"invalid option tag {tag} at offset {self.offset - 1}")
        return self.read_type(inner)

    def enum(self, variants: list[str]) -> dict[str, Any]:
        raw = self.u8()
        return {
            "raw": raw,
            "label": variants[raw] if raw < len(variants) else "UNKNOWN",
        }

    def read_type(self, typ: Any) -> Any:
        if typ == "publicKey":
            return self.pubkey()
        if typ == "u8":
            return self.u8()
        if typ == "bool":
            return self.bool()
        if typ == "i64":
            return self.i64()
        if typ == "u64":
            return self.u64()
        if typ == "u128":
            return self.u128()
        if isinstance(typ, dict) and "option" in typ:
            return self.option(typ["option"])
        raise ValueError(f"unsupported Jupiter example decode type: {typ!r}")


def account_discriminator(name: str) -> bytes:
    return hashlib.sha256(f"account:{name}".encode("utf-8")).digest()[:8]


def fetch_account(rpc_url: str, pubkey: str) -> dict[str, Any]:
    result = rpc_call(rpc_url, "getAccountInfo", [pubkey, {"encoding": "base64", "commitment": "finalized"}])
    value = result.get("value")
    if value is None:
        raise RuntimeError(f"account not found: {pubkey}")
    data = base64.b64decode(value["data"][0])
    return {
        "pubkey": pubkey,
        "owner": value.get("owner"),
        "lamports": value.get("lamports"),
        "executable": value.get("executable"),
        "rent_epoch": value.get("rentEpoch"),
        "data": data,
    }


def find_first_account_by_discriminator(rpc_url: str, discriminator: bytes) -> str | None:
    result = rpc_call(
        rpc_url,
        "getProgramAccounts",
        [
            JUPITER_PERPS_PROGRAM_ID,
            {
                "commitment": "finalized",
                "encoding": "base64",
                "dataSlice": {"offset": 0, "length": 0},
                "filters": [{"memcmp": {"offset": 0, "bytes": b58encode(discriminator)}}],
            },
        ],
    )
    if not result:
        return None
    return sorted(item["pubkey"] for item in result)[0]


def idl_account(idl: dict[str, Any], name: str) -> dict[str, Any]:
    for account in idl.get("accounts", []):
        if account.get("name") == name:
            return account
    raise KeyError(name)


def enum_variants(idl: dict[str, Any], name: str) -> list[str]:
    for typ in idl.get("types", []):
        if typ.get("name") == name and typ.get("type", {}).get("kind") == "enum":
            return [variant["name"] for variant in typ["type"].get("variants", [])]
    raise KeyError(name)


def decode_account(idl: dict[str, Any], account: dict[str, Any], account_name: str) -> dict[str, Any]:
    data = account["data"]
    expected = account_discriminator(account_name)
    actual = data[:8]
    if actual != expected:
        raise ValueError(
            f"{account_name} discriminator mismatch: expected {expected.hex()}, got {actual.hex()}"
        )
    reader = Reader(data)
    layout = idl_account(idl, account_name)["type"]["fields"]
    decoded: dict[str, Any] = {}
    offsets: dict[str, int] = {}
    for field in layout:
        name = field["name"]
        offsets[name] = reader.offset
        typ = field["type"]
        if isinstance(typ, dict) and "defined" in typ:
            decoded[name] = reader.enum(enum_variants(idl, typ["defined"]))
        else:
            decoded[name] = reader.read_type(typ)
    trailing = data[reader.offset :]
    return {
        "account_name": account_name,
        "pubkey": account["pubkey"],
        "owner": account["owner"],
        "executable": account["executable"],
        "data_len": len(data),
        "data_sha256": hashlib.sha256(data).hexdigest(),
        "discriminator_hex": actual.hex(),
        "decoded_len": reader.offset,
        "trailing_zero_padding_len": len(trailing) if all(byte == 0 for byte in trailing) else 0,
        "nonzero_trailing_bytes": 0 if all(byte == 0 for byte in trailing) else sum(1 for byte in trailing if byte),
        "field_offsets": offsets,
        "fields": decoded,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", default=".env", help="Local env file containing HELIUS_RPC_URL.")
    parser.add_argument(
        "--idl",
        default="target/oprs-jupiter-onchain-idl/jupiter-perps-idl.json",
        help="Local onchain IDL JSON produced by fetch_jupiter_onchain_idl.py.",
    )
    parser.add_argument(
        "--idl-evidence",
        default="target/oprs-jupiter-onchain-idl/latest.json",
        help="Local onchain IDL evidence JSON.",
    )
    parser.add_argument(
        "--out",
        default="target/oprs-jupiter-position-decode/latest.json",
        help="Scrubbed decoded output path.",
    )
    args = parser.parse_args()

    load_dotenv(Path(args.env))
    rpc_url = os.environ.get("HELIUS_RPC_URL")
    if not rpc_url:
        raise SystemExit("HELIUS_RPC_URL is required in local .env or environment")

    idl = json.loads(Path(args.idl).read_text(encoding="utf-8"))
    idl_evidence = json.loads(Path(args.idl_evidence).read_text(encoding="utf-8"))
    decoded: list[dict[str, Any]] = []
    observations: list[dict[str, Any]] = []

    position = fetch_account(rpc_url, DOCS_POSITION_ACCOUNT)
    decoded.append(decode_account(idl, position, "Position"))

    try:
        position_request = fetch_account(rpc_url, DOCS_POSITION_REQUEST_ACCOUNT)
        decoded.append(decode_account(idl, position_request, "PositionRequest"))
        observations.append(
            {
                "account": DOCS_POSITION_REQUEST_ACCOUNT,
                "account_name": "PositionRequest",
                "status": "docs_example_account_found_and_decoded",
            }
        )
    except RuntimeError as error:
        observations.append(
            {
                "account": DOCS_POSITION_REQUEST_ACCOUNT,
                "account_name": "PositionRequest",
                "status": "docs_example_account_not_found",
                "reason": str(error),
                "interpretation": "Official docs state non-TP/SL PositionRequest accounts are closed after execution or rejection; absence of this public example account is not a decode failure.",
            }
        )
        candidate = find_first_account_by_discriminator(rpc_url, account_discriminator("PositionRequest"))
        if candidate:
            candidate_account = fetch_account(rpc_url, candidate)
            decoded.append(decode_account(idl, candidate_account, "PositionRequest"))
            observations.append(
                {
                    "account": candidate,
                    "account_name": "PositionRequest",
                    "status": "active_account_found_by_discriminator_and_decoded",
                    "source": "getProgramAccounts memcmp offset 0 against Anchor account discriminator",
                }
            )
        else:
            observations.append(
                {
                    "account_name": "PositionRequest",
                    "status": "no_active_account_found_by_discriminator",
                    "source": "getProgramAccounts memcmp offset 0 against Anchor account discriminator",
                }
            )
    report = {
        "schema_version": "oprs.jupiter_position_decode_probe.v0",
        "generated_at_unix": int(time.time()),
        "generated_by": "scripts/decode_jupiter_position_examples.py",
        "program_id": JUPITER_PERPS_PROGRAM_ID,
        "source_authority": {
            "authority_status": idl_evidence["authority_status"],
            "idl_address": idl_evidence["anchor_idl_derivation"]["idl_address"],
            "idl_authority": idl_evidence["idl_hashes"]["idl_authority"],
            "normalized_idl_sha256": idl_evidence["idl_hashes"]["normalized_idl_sha256"],
            "docs_linked_candidate_matched": idl_evidence["comparison"][
                "onchain_matches_docs_linked_candidate"
            ],
        },
        "docs_examples": PUBLIC_DOCS,
        "decoded_accounts": decoded,
        "observations": observations,
        "readiness": {
            "live_rpc_read_claimed": True,
            "raw_account_data_committed": False,
            "binary_decode_claimed": True,
            "verified_request_fulfillment_pair_claimed": False,
            "liquidation_replay_claimed": False,
            "execution_claimed": False,
            "instruction_builder_used": False,
            "order_operation_used": False,
            "auth_used": False,
            "trader_private_state_used": False,
        },
        "claim_boundary": {
            "allowed": [
                "source_authority_from_onchain_anchor_idl",
                "docs_example_position_account_decoded",
                "docs_example_position_request_account_decoded",
                "field_offsets_emitted_for_source_review",
            ],
            "blocked": [
                "verified_request_fulfillment_pair_claim",
                "historical_liquidation_replay_claim",
                "keeper_execution_claim",
                "signing_or_transaction_submission",
            ],
        },
    }

    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote Jupiter docs-example decode report to {output_path}")
    print("No RPC URL, API key, wallet secret, signer, or raw transaction data was committed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
