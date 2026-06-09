#!/usr/bin/env python3
"""Audit public Jupiter Perps source authority without using secrets.

This command checks official Jupiter docs markers and the docs-linked IDL
example repository. It intentionally does not authorize binary decode claims.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


JUPITER_PERPS_PROGRAM_ID = "PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu"

DOC_SOURCES = {
    "technical_reference": "https://docs.jup.ag/user-docs/trade/perps-and-jlp/technical-reference",
    "position_account": "https://developers.jup.ag/docs/perps/position-account",
    "position_request_account": "https://developers.jup.ag/docs/perps/position-request-account",
}

DOC_MARKERS = {
    "technical_reference": [
        "Request Fulfillment Model",
        "two separate transactions",
        "Keeper",
        "External References",
        "Jupiter Perps IDL parsing examples",
    ],
    "position_account": [
        "Position Account",
        "traders will always have the same Position account address",
        "owner",
        "pool",
        "custody",
        "collateralCustody",
    ],
    "position_request_account": [
        "PositionRequest Account",
        "random integer seed",
        "executed",
        "counter",
        "bump",
    ],
}

IDL_REPO = "julianfssen/jupiter-perps-anchor-idl-parsing"
IDL_PATH = "src/idl/jupiter-perpetuals-idl.ts"
GITHUB_API = "https://api.github.com"
GITHUB_RAW = "https://raw.githubusercontent.com"


def fetch_text(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "accept": "text/html,text/plain,application/json",
            "user-agent": "oprs-source-authority-audit/0.1 (+https://github.com/jf-cmyk/open-perps-reliability-stack)",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as error:
        raise SystemExit(f"Fetch failed for {url}: {error.reason}") from error


def fetch_json(url: str) -> Any:
    request = urllib.request.Request(
        url,
        headers={
            "accept": "application/vnd.github+json",
            "user-agent": "oprs-source-authority-audit/0.1 (+https://github.com/jf-cmyk/open-perps-reliability-stack)",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as error:
        raise SystemExit(f"Fetch failed for {url}: {error.reason}") from error


def audit_docs() -> dict[str, Any]:
    results = {}
    for source_id, url in DOC_SOURCES.items():
        body = fetch_text(url)
        markers = DOC_MARKERS[source_id]
        results[source_id] = {
            "url": url,
            "markers": {marker: marker in body for marker in markers},
            "all_markers_present": all(marker in body for marker in markers),
        }
    return results


def audit_idl_candidate() -> dict[str, Any]:
    commit = fetch_json(f"{GITHUB_API}/repos/{IDL_REPO}/commits/main")
    commit_sha = commit["sha"]
    contents = fetch_json(f"{GITHUB_API}/repos/{IDL_REPO}/contents/{IDL_PATH}?ref={commit_sha}")
    raw_url = f"{GITHUB_RAW}/{IDL_REPO}/{commit_sha}/{IDL_PATH}"
    raw = fetch_text(raw_url).encode("utf-8")
    verification = commit.get("commit", {}).get("verification", {})
    return {
        "repository": IDL_REPO,
        "repository_url": f"https://github.com/{IDL_REPO}",
        "commit": commit_sha,
        "commit_message": commit.get("commit", {}).get("message"),
        "commit_author_date": commit.get("commit", {}).get("author", {}).get("date"),
        "commit_verification_verified": verification.get("verified"),
        "commit_verification_reason": verification.get("reason"),
        "idl_path": IDL_PATH,
        "idl_git_blob_sha": contents.get("sha"),
        "idl_content_sha256": hashlib.sha256(raw).hexdigest(),
        "idl_size_bytes": len(raw),
        "idl_source_url": contents.get("html_url"),
    }


def build_report() -> dict[str, Any]:
    docs = audit_docs()
    idl = audit_idl_candidate()
    return {
        "schema_version": "0.1.0",
        "report_id": "jupiter_perps_source_authority_audit",
        "generated_at_unix": int(time.time()),
        "generated_by": "scripts/audit_jupiter_source_authority.py",
        "program_id": JUPITER_PERPS_PROGRAM_ID,
        "docs": docs,
        "idl_candidate": idl,
        "authority_status": "docs_linked_example_not_canonical",
        "field_planning_authorized": True,
        "binary_decode_authorized": False,
        "verified_lifecycle_pairing_authorized": False,
        "claim_boundary": {
            "allowed": [
                "target_discovery",
                "transaction_history_sampling",
                "shared_account_candidate_labeling",
                "field_planning_from_docs_linked_idl_candidate",
            ],
            "blocked": [
                "jupiter_binary_account_decode_claim",
                "verified_request_fulfillment_pair_claim",
                "position_request_decode_claim",
                "liquidation_replay_claim",
            ],
        },
        "next_authority_steps": [
            "Jupiter-owned canonical Perps IDL/source revision is published or confirmed.",
            "Docs-linked IDL is explicitly confirmed as canonical for the current onchain program.",
            "Independent onchain/program-IDL extraction is reviewed, hashed, and matched to current program semantics.",
        ],
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out",
        default="target/oprs-jupiter-source-authority/latest.json",
        help="Output path for the scrubbed Jupiter source-authority audit.",
    )
    args = parser.parse_args()

    report = build_report()
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote Jupiter source-authority audit to {output_path}")
    print("No RPC URL, wallet, signer, keypair, or secret was loaded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
