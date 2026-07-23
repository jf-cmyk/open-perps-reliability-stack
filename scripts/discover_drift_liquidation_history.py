#!/usr/bin/env python3
"""Page public Drift transactions for liquidation instruction logs.

The command is read-only and writes scrubbed public metadata. It never prints or
writes the RPC URL or credentials supplied through HELIUS_RPC_URL, and it does
not persist raw transaction bodies or raw logs.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
from pathlib import Path
import urllib.error
import urllib.request
from typing import Any


DRIFT_PROGRAM_ID = "dRiftyHA39MWEi3m9aunc5MzRF1JYuBsbn6VPcn33UH"
LIQUIDATION_LOG_PREFIX = "Program log: Instruction: Liquidate"
DEFAULT_OUT = "target/oprs-drift-liquidation-history-probe/latest.json"


def rpc(url: str, payload: Any, retries: int = 4) -> Any:
    body = json.dumps(payload, separators=(",", ":")).encode()
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code != 429 or attempt == retries - 1:
                raise
            time.sleep(2**attempt)
    raise RuntimeError("RPC retry loop exhausted")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--before")
    parser.add_argument("--pages", type=int, default=1)
    parser.add_argument("--page-size", type=int, default=1000)
    parser.add_argument("--batch-size", type=int, default=50)
    parser.add_argument("--out", default=DEFAULT_OUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if (
        not 1 <= args.pages <= 10
        or not 1 <= args.page_size <= 1000
        or not 1 <= args.batch_size <= 50
    ):
        print(
            "pages must be 1-10, page-size must be 1-1000, and batch-size must be 1-50",
            file=sys.stderr,
        )
        return 2
    url = os.environ.get("HELIUS_RPC_URL")
    if not url:
        print("HELIUS_RPC_URL is required", file=sys.stderr)
        return 2

    before = args.before
    scanned = 0
    candidates: list[dict[str, Any]] = []
    first_slot = None
    last_slot = None
    first_block_time = None
    last_block_time = None

    for page_index in range(args.pages):
        config: dict[str, Any] = {"limit": args.page_size}
        if before:
            config["before"] = before
        response = rpc(
            url,
            {
                "jsonrpc": "2.0",
                "id": f"signatures-{page_index}",
                "method": "getSignaturesForAddress",
                "params": [DRIFT_PROGRAM_ID, config],
            },
        )
        if response.get("error"):
            raise RuntimeError(response["error"])
        signatures = response.get("result") or []
        if not signatures:
            break

        first_slot = first_slot or signatures[0].get("slot")
        first_block_time = first_block_time or signatures[0].get("blockTime")
        last_slot = signatures[-1].get("slot")
        last_block_time = signatures[-1].get("blockTime")
        before = signatures[-1]["signature"]

        for offset in range(0, len(signatures), args.batch_size):
            chunk = signatures[offset : offset + args.batch_size]
            batch = [
                {
                    "jsonrpc": "2.0",
                    "id": index,
                    "method": "getTransaction",
                    "params": [
                        row["signature"],
                        {
                            "encoding": "json",
                            "maxSupportedTransactionVersion": 0,
                            "commitment": "finalized",
                        },
                    ],
                }
                for index, row in enumerate(chunk)
            ]
            transactions = rpc(url, batch)
            if not isinstance(transactions, list):
                raise RuntimeError(
                    f"Expected a batch response list, received {type(transactions).__name__}"
                )
            by_id = {row.get("id"): row for row in transactions}
            for index, signature_row in enumerate(chunk):
                transaction = by_id.get(index, {}).get("result") or {}
                meta = transaction.get("meta") or {}
                logs = meta.get("logMessages") or []
                matching = [line for line in logs if LIQUIDATION_LOG_PREFIX in line]
                if matching:
                    candidates.append(
                        {
                            "signature": signature_row["signature"],
                            "slot": signature_row.get("slot"),
                            "block_time": signature_row.get("blockTime"),
                            "transaction_error": meta.get("err"),
                            "matching_log_count": len(matching),
                            "matching_log_labels": ["Liquidate"],
                        }
                    )
            scanned += len(chunk)

        if len(signatures) < args.page_size:
            break

    output = {
        "schema_version": "oprs.drift_liquidation_history_probe.v0",
        "dataset_name": "drift_liquidation_history_probe_local",
        "protocol": "drift",
        "chain_id": "solana-mainnet-beta",
        "program_id": DRIFT_PROGRAM_ID,
        "generated_at_unix": int(time.time()),
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "query": {
            "commitment": "finalized",
            "pages": args.pages,
            "page_size": args.page_size,
            "batch_size": args.batch_size,
            "started_before": args.before,
            "log_prefix": LIQUIDATION_LOG_PREFIX,
        },
        "scan_summary": {
            "transactions_scanned": scanned,
            "newest_scanned_slot": first_slot,
            "newest_scanned_block_time": first_block_time,
            "oldest_scanned_slot": last_slot,
            "oldest_scanned_block_time": last_block_time,
            "next_before": before,
            "liquidation_candidate_count": len(candidates),
        },
        "liquidation_candidates": candidates,
        "readiness": {
            "live_rpc_read_claimed": True,
            "auth_used": False,
            "trader_state_used": False,
            "instruction_builder_used": False,
            "order_operation_used": False,
            "raw_transaction_committed": False,
            "raw_logs_committed": False,
            "execution_claimed": False,
            "replay_ready": False,
        },
        "known_limitations": [
            "Log matches are discovery evidence only; selected transactions must be verified against pinned source before replay claims.",
            "A zero-candidate result is bounded pagination progress, not evidence that liquidations were absent.",
            "The probe does not decode account state, prove market economics, or submit transactions.",
        ],
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
