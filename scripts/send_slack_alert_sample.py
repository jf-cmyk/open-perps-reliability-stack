#!/usr/bin/env python3
"""Send or dry-run the checked-in Slack alert sample payload.

The default mode is dry-run. Network delivery requires --send and a webhook
value in the payload's declared environment variable.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from public_package_contract import load_json
from validate_slack_alert_payload import DEFAULT_PATH, validate_payload


DEFAULT_TIMEOUT_SECONDS = 10


def _slack_message(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "text": payload["text"],
        "blocks": payload["blocks"],
    }


def _webhook_env_name(payload: dict[str, Any]) -> str:
    return payload.get("delivery", {}).get("webhook_variable", "OPRS_ALERT_WEBHOOK_URL")


def _validate_webhook_url(webhook_url: str) -> bool:
    return webhook_url.startswith(
        ("https://hooks.slack.com/services/", "https://hooks.slack-gov.com/services/")
    )


def _post_to_slack(message: dict[str, Any], webhook_url: str, timeout_seconds: int) -> None:
    request = urllib.request.Request(
        webhook_url,
        data=json.dumps(message, separators=(",", ":")).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "oprs-readonly-worker-slack-smoke/0",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        body = response.read(256).decode("utf-8", errors="replace").strip()
        if response.status < 200 or response.status >= 300 or body != "ok":
            raise RuntimeError(f"Slack webhook returned HTTP {response.status}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--payload",
        type=Path,
        default=DEFAULT_PATH,
        help=f"Slack payload contract to send or dry-run. Default: {DEFAULT_PATH}",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and summarize without network delivery. This is the default.",
    )
    mode.add_argument("--send", action="store_true", help="Post the scrubbed sample to Slack.")
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"Slack HTTP timeout for --send. Default: {DEFAULT_TIMEOUT_SECONDS}",
    )
    args = parser.parse_args()

    failures = validate_payload(args.payload)
    if failures:
        print("Slack alert sample validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    payload = load_json(args.payload)
    message = _slack_message(payload)
    source_event = payload["source_event"]

    if not args.send:
        print("PASS Slack alert sample dry-run")
        print(f"payload={args.payload}")
        print(f"service={source_event['service_name']}")
        print(f"protocol={source_event['protocol']}")
        print(f"status={source_event['status']}")
        print(f"alert_class={source_event['alert_class']}")
        print(f"blocks={len(message['blocks'])}")
        return 0

    webhook_env_name = _webhook_env_name(payload)
    webhook_url = os.environ.get(webhook_env_name, "")
    if not webhook_url:
        print(f"Missing required environment variable: {webhook_env_name}", file=sys.stderr)
        return 2
    if not _validate_webhook_url(webhook_url):
        print(f"{webhook_env_name} does not look like a Slack incoming webhook URL", file=sys.stderr)
        return 2

    try:
        _post_to_slack(message, webhook_url, args.timeout_seconds)
    except urllib.error.URLError as exc:
        print(f"Slack sample delivery failed: {exc.reason}", file=sys.stderr)
        return 1
    except RuntimeError as exc:
        print(f"Slack sample delivery failed: {exc}", file=sys.stderr)
        return 1

    print("PASS Slack alert sample sent")
    print(f"payload={args.payload}")
    print(f"service={source_event['service_name']}")
    print(f"protocol={source_event['protocol']}")
    print(f"status={source_event['status']}")
    print(f"alert_class={source_event['alert_class']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
