#!/usr/bin/env python3
"""Fetch and hash the onchain Anchor IDL for Jupiter Perps.

This is a read-only source-authority probe. It derives the Anchor IDL account
for the live Jupiter Perps program, fetches it through the configured RPC URL,
inflates the stored IDL payload, and writes local scrubbed evidence under
target/. It never signs, builds, or submits transactions.
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
import zlib
from pathlib import Path
from typing import Any


JUPITER_PERPS_PROGRAM_ID = "PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu"
ANCHOR_IDL_SEED = "anchor:idl"
PDA_MARKER = b"ProgramDerivedAddress"
PUBLIC_GITHUB_IDL_CANDIDATE = (
    "https://raw.githubusercontent.com/julianfssen/"
    "jupiter-perps-anchor-idl-parsing/"
    "630cfd72cad499f45453a53383d7ac6d3e09e022/"
    "src/idl/jupiter-perpetuals-idl.ts"
)
BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key and key not in os.environ:
            os.environ[key] = value.strip().strip('"').strip("'")


def b58decode(value: str) -> bytes:
    n = 0
    for char in value:
        n *= 58
        if char not in BASE58_ALPHABET:
            raise ValueError(f"invalid base58 character: {char!r}")
        n += BASE58_ALPHABET.index(char)
    data = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    leading = len(value) - len(value.lstrip("1"))
    return b"\x00" * leading + data


def b58encode(data: bytes) -> str:
    n = int.from_bytes(data, "big")
    chars = []
    while n:
        n, rem = divmod(n, 58)
        chars.append(BASE58_ALPHABET[rem])
    leading = len(data) - len(data.lstrip(b"\x00"))
    return "1" * leading + ("".join(reversed(chars)) if chars else "")


def is_ed25519_on_curve(compressed: bytes) -> bool:
    if len(compressed) != 32:
        return False
    p = 2**255 - 19
    y = int.from_bytes(compressed, "little") & ((1 << 255) - 1)
    if y >= p:
        return False
    d = (-121665 * pow(121666, p - 2, p)) % p
    yy = (y * y) % p
    denominator = (d * yy + 1) % p
    if denominator == 0:
        return False
    x2 = ((yy - 1) * pow(denominator, p - 2, p)) % p
    if x2 == 0:
        return True
    return pow(x2, (p - 1) // 2, p) == 1


def create_program_address(seeds: list[bytes], program_id: bytes) -> bytes:
    digest = hashlib.sha256(b"".join(seeds) + program_id + PDA_MARKER).digest()
    if is_ed25519_on_curve(digest):
        raise ValueError("derived address is on curve")
    return digest


def find_program_address(seeds: list[bytes], program_id: bytes) -> tuple[bytes, int]:
    for bump in range(255, -1, -1):
        try:
            return create_program_address([*seeds, bytes([bump])], program_id), bump
        except ValueError:
            continue
    raise ValueError("no valid PDA bump found")


def create_with_seed(base: bytes, seed: str, owner: bytes) -> bytes:
    if len(seed.encode("utf-8")) > 32:
        raise ValueError("seed too long")
    return hashlib.sha256(base + seed.encode("utf-8") + owner).digest()


def anchor_idl_address(program_id: str) -> dict[str, Any]:
    program_bytes = b58decode(program_id)
    if len(program_bytes) != 32:
        raise ValueError("program id did not decode to 32 bytes")
    base, bump = find_program_address([], program_bytes)
    idl = create_with_seed(base, ANCHOR_IDL_SEED, program_bytes)
    return {
        "program_id": program_id,
        "base_pda": b58encode(base),
        "base_pda_bump": bump,
        "idl_address": b58encode(idl),
    }


def rpc_call(rpc_url: str, method: str, params: list[Any]) -> Any:
    body = json.dumps({"jsonrpc": "2.0", "id": "oprs", "method": method, "params": params}).encode(
        "utf-8"
    )
    request = urllib.request.Request(
        rpc_url,
        data=body,
        headers={"content-type": "application/json", "user-agent": "oprs-jupiter-idl-probe/0.1"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if "error" in payload:
        raise RuntimeError(payload["error"])
    return payload["result"]


def fetch_url_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"user-agent": "oprs-jupiter-idl-probe/0.1"})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read()


def normalize_idl_text(text: str) -> tuple[str, str]:
    stripped = text.strip()
    for prefix in (
        "export const IDL = ",
        "export const jupiterPerpetualsIdl = ",
        "export type Perpetuals = ",
    ):
        if stripped.startswith(prefix):
            stripped = stripped[len(prefix) :]
            break
    first_brace = stripped.find("{")
    if first_brace > 0:
        stripped = stripped[first_brace:]
    depth = 0
    in_string = False
    escaped = False
    end_index = None
    for index, char in enumerate(stripped):
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                end_index = index + 1
                break
    if end_index is not None:
        stripped = stripped[:end_index]
    if stripped.endswith(";"):
        stripped = stripped[:-1]
    parsed = json.loads(stripped)
    normalized = json.dumps(parsed, sort_keys=True, separators=(",", ":"))
    return normalized, hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def decode_anchor_idl_account(data: bytes) -> dict[str, Any]:
    attempts: list[dict[str, Any]] = []
    for offset_name, offset in [
        ("anchor_account_discriminator_authority_vec", 8 + 32),
        ("authority_vec_no_discriminator", 32),
        ("raw_vec", 0),
    ]:
        if len(data) < offset + 4:
            continue
        length = struct.unpack_from("<I", data, offset)[0]
        start = offset + 4
        end = start + length
        compressed = data[start:end]
        if end > len(data):
            attempts.append({"format": offset_name, "ok": False, "reason": "vec_length_exceeds_account"})
            continue
        try:
            inflated = zlib.decompress(compressed)
        except zlib.error as error:
            attempts.append({"format": offset_name, "ok": False, "reason": str(error)})
            continue
        text = inflated.decode("utf-8")
        normalized, normalized_sha256 = normalize_idl_text(text)
        authority = None
        discriminator_sha256 = None
        if offset_name == "anchor_account_discriminator_authority_vec":
            discriminator_sha256 = hashlib.sha256(data[:8]).hexdigest()
            authority = b58encode(data[8:40])
        elif offset_name == "authority_vec_no_discriminator":
            authority = b58encode(data[:32])
        return {
            "decode_format": offset_name,
            "idl_authority": authority,
            "account_discriminator_sha256": discriminator_sha256,
            "compressed_idl_len": length,
            "compressed_idl_sha256": hashlib.sha256(compressed).hexdigest(),
            "inflated_idl_len": len(inflated),
            "inflated_idl_sha256": hashlib.sha256(inflated).hexdigest(),
            "normalized_idl_sha256": normalized_sha256,
            "idl": json.loads(normalized),
            "attempts": attempts + [{"format": offset_name, "ok": True}],
        }
    raise RuntimeError({"message": "could not decode anchor IDL account", "attempts": attempts})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", default=".env", help="Local env file containing HELIUS_RPC_URL.")
    parser.add_argument(
        "--out",
        default="target/oprs-jupiter-onchain-idl/latest.json",
        help="Scrubbed evidence output path.",
    )
    parser.add_argument(
        "--idl-out",
        default="target/oprs-jupiter-onchain-idl/jupiter-perps-idl.json",
        help="Local decoded IDL JSON output path.",
    )
    args = parser.parse_args()

    load_dotenv(Path(args.env))
    rpc_url = os.environ.get("HELIUS_RPC_URL")
    if not rpc_url:
        raise SystemExit("HELIUS_RPC_URL is required in local .env or environment")

    derivation = anchor_idl_address(JUPITER_PERPS_PROGRAM_ID)
    result = rpc_call(
        rpc_url,
        "getAccountInfo",
        [
            derivation["idl_address"],
            {"encoding": "base64", "commitment": "finalized"},
        ],
    )
    value = result.get("value")
    if value is None:
        raise SystemExit(f"No onchain IDL account found at {derivation['idl_address']}")

    account_data = base64.b64decode(value["data"][0])
    decoded = decode_anchor_idl_account(account_data)
    idl = decoded.pop("idl")
    idl_name = idl.get("name") or idl.get("metadata", {}).get("name")
    account_names = [account.get("name") for account in idl.get("accounts", [])]
    account_names_lower = {name.lower(): index for index, name in enumerate(account_names) if name}
    instruction_names = [ix.get("name") for ix in idl.get("instructions", [])]
    type_names = [typ.get("name") for typ in idl.get("types", [])]
    candidate_raw = fetch_url_bytes(PUBLIC_GITHUB_IDL_CANDIDATE)
    _, candidate_normalized_sha256 = normalize_idl_text(candidate_raw.decode("utf-8"))

    evidence = {
        "schema_version": "oprs.jupiter_onchain_idl_probe.v0",
        "generated_at_unix": int(time.time()),
        "generated_by": "scripts/fetch_jupiter_onchain_idl.py",
        "program_id": JUPITER_PERPS_PROGRAM_ID,
        "anchor_idl_derivation": derivation,
        "rpc": {
            "commitment": "finalized",
            "rpc_url_committed": False,
            "api_key_committed": False,
        },
        "account_info": {
            "owner": value.get("owner"),
            "lamports": value.get("lamports"),
            "executable": value.get("executable"),
            "rent_epoch": value.get("rentEpoch"),
            "data_len": len(account_data),
            "account_data_sha256": hashlib.sha256(account_data).hexdigest(),
        },
        "idl_summary": {
            "name": idl_name,
            "address": idl.get("address") or idl.get("metadata", {}).get("address"),
            "version": idl.get("version") or idl.get("metadata", {}).get("version"),
            "account_count": len(account_names),
            "instruction_count": len(instruction_names),
            "type_count": len(type_names),
            "has_position_account": "position" in account_names_lower,
            "has_position_request_account": "positionrequest" in account_names_lower
            or "position_request" in account_names_lower,
            "position_account_index": account_names_lower.get("position"),
            "position_request_account_index": account_names_lower.get("positionrequest")
            or account_names_lower.get("position_request"),
            "selected_accounts": [
                name for name in account_names if name and name.lower() in {"position", "positionrequest", "custody", "pool"}
            ],
            "selected_instruction_prefixes": [
                name
                for name in instruction_names
                if any(fragment in name.lower() for fragment in ["position", "liquidat", "tpsl", "request"])
            ][:80],
            "selected_types": [
                name
                for name in type_names
                if any(fragment in name.lower() for fragment in ["position", "request", "side", "change"])
            ][:80],
        },
        "idl_hashes": decoded,
        "comparison": {
            "docs_linked_candidate_url": PUBLIC_GITHUB_IDL_CANDIDATE,
            "docs_linked_candidate_normalized_sha256": candidate_normalized_sha256,
            "onchain_matches_docs_linked_candidate": decoded["normalized_idl_sha256"]
            == candidate_normalized_sha256,
        },
        "authority_status": "onchain_anchor_idl_hashable",
        "binary_decode_authorized": True,
        "verified_lifecycle_pairing_authorized": False,
        "claim_boundary": {
            "allowed": [
                "onchain_anchor_idl_account_exists",
                "idl_hash_pinned_locally",
                "field_planning_from_onchain_idl",
                "source_authorized_account_layout_decode",
            ],
            "blocked": [
                "verified_request_fulfillment_pair_claim",
                "liquidation_replay_claim",
                "signing_or_transaction_submission",
            ],
        },
        "forbidden_actions": [
            "sign",
            "submit_transaction",
            "load_keypair",
            "call_order_endpoint",
            "call_execute_endpoint",
            "call_build_endpoint",
            "call_submit_endpoint",
            "call_auth_endpoint",
            "keeper_operation",
        ],
    }

    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    idl_path = Path(args.idl_out)
    idl_path.parent.mkdir(parents=True, exist_ok=True)
    idl_path.write_text(json.dumps(idl, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"Wrote Jupiter onchain IDL evidence to {output_path}")
    print(f"Wrote local decoded IDL JSON to {idl_path}")
    print("No RPC URL, API key, wallet, signer, or raw transaction data was committed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
