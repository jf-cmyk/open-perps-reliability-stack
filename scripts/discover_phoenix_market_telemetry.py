#!/usr/bin/env python3
"""Run a bounded read-only Phoenix/Rise public market telemetry probe.

The probe uses only public HTTP market-data surfaces and writes a scrubbed
summary under target/. It intentionally does not persist the raw response body,
does not use auth, and does not touch trader, instruction-builder, or order
operation routes.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_API_URL = "https://perp-api.phoenix.trade"
SNAPSHOT_PATH = "/v1/exchange/snapshot"
SOURCE_REFS = [
    "https://docs.phoenix.trade/api",
    "https://docs.phoenix.trade/api/exchange/get-exchange-snapshot",
    "https://docs.phoenix.trade/api/websocket",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="target/oprs-phoenix-market-telemetry/latest.json")
    parser.add_argument("--api-url", default=DEFAULT_API_URL)
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--max-markets", type=int, default=8)
    args = parser.parse_args()

    if args.timeout <= 0:
        raise SystemExit("--timeout must be positive")
    if args.max_markets <= 0 or args.max_markets > 25:
        raise SystemExit("--max-markets must be between 1 and 25")

    api_url = args.api_url.rstrip("/")
    if api_url != DEFAULT_API_URL:
        raise SystemExit("Only the default public Phoenix API URL is allowed for the checked probe")

    url = urllib.parse.urljoin(api_url + "/", SNAPSHOT_PATH.lstrip("/"))
    started_at = time.time()
    payload, http_status = fetch_json(url, timeout=args.timeout)
    elapsed_ms = int((time.time() - started_at) * 1000)

    summary = build_summary(
        payload=payload,
        http_status=http_status,
        elapsed_ms=elapsed_ms,
        timeout=args.timeout,
        max_markets=args.max_markets,
    )
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote scrubbed Phoenix market telemetry probe to {out_path}")
    return 0


def fetch_json(url: str, *, timeout: float) -> tuple[dict[str, Any], int]:
    request = urllib.request.Request(
        url,
        method="GET",
        headers={
            "Accept": "application/json",
            "User-Agent": "oprs-readonly-phoenix-probe/0.1",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(2_000_000)
            status = response.status
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"Phoenix public HTTP probe failed with status {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Phoenix public HTTP probe failed: {exc.reason}") from exc

    try:
        decoded = json.loads(body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit("Phoenix public HTTP probe returned non-JSON data") from exc
    if not isinstance(decoded, dict):
        raise SystemExit("Phoenix public HTTP probe returned a non-object JSON payload")
    return decoded, status


def build_summary(
    *,
    payload: dict[str, Any],
    http_status: int,
    elapsed_ms: int,
    timeout: float,
    max_markets: int,
) -> dict[str, Any]:
    markets = payload.get("markets")
    if not isinstance(markets, list):
        raise SystemExit("Phoenix snapshot payload did not include a markets array")

    exchange = payload.get("exchange")
    if not isinstance(exchange, dict):
        exchange = {}

    sample_markets = []
    for market in markets[:max_markets]:
        if not isinstance(market, dict):
            continue
        sample_markets.append(
            {
                "symbol": string_or_unknown(market.get("symbol")),
                "asset_id_present": "assetId" in market,
                "market_status": string_or_unknown(market.get("marketStatus")),
                "funding_config_present": isinstance(market.get("fundingConfig"), dict),
                "risk_factors_present": isinstance(market.get("riskFactors"), dict),
                "mark_price_parameters_present": isinstance(market.get("markPriceParameters"), dict),
            }
        )

    return {
        "schema_version": "oprs.phoenix_market_telemetry_probe.v0",
        "dataset_name": "phoenix_market_telemetry_probe_local",
        "protocol": "phoenix_rise",
        "chain_id": "solana-mainnet-beta",
        "generated_at_unix": int(time.time()),
        "source_refs": SOURCE_REFS,
        "query": {
            "base_url": "https://perp-api.phoenix.trade",
            "method": "GET",
            "path": SNAPSHOT_PATH,
            "timeout_ms": int(timeout * 1000),
            "max_markets": max_markets,
        },
        "response_summary": {
            "http_status": http_status,
            "elapsed_ms": elapsed_ms,
            "top_level_keys": sorted(str(key) for key in payload.keys()),
            "slot_present": "slot" in payload,
            "slot_index_present": "slotIndex" in payload,
            "version_present": "version" in payload,
            "sequence_number_present": "sequenceNumber" in payload,
            "exchange_active_present": "active" in exchange,
            "exchange_active": bool(exchange.get("active")),
            "exchange_gated_present": "gated" in exchange,
            "exchange_gated": bool(exchange.get("gated")),
            "program_id_present": "programId" in exchange,
            "market_count": len(markets),
            "sample_market_count": len(sample_markets),
            "sample_markets": sample_markets,
        },
        "readiness": {
            "live_public_http_probe_claimed": True,
            "auth_used": False,
            "trader_state_used": False,
            "instruction_builder_used": False,
            "order_operation_used": False,
            "raw_response_committed": False,
            "execution_claimed": False,
            "replay_ready": False,
        },
        "scrub": {
            "raw_response_committed": False,
            "account_addresses_committed": False,
            "credential_material_committed": False,
        },
        "known_limitations": [
            "Local target output only; not served in the public proof pack.",
            "Records capped market summaries and shape presence only, not raw response bodies.",
            "Does not use WebSocket, trader-state, auth, instruction-builder, order, signing, or submission paths.",
        ],
    }


def string_or_unknown(value: object) -> str:
    return value if isinstance(value, str) and value else "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
