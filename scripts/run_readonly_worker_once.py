#!/usr/bin/env python3
"""Run one allowlisted read-only worker job locally.

Default mode is --plan. Use --execute only for an intentional bounded run.
All commands write under target/ and must preserve the read-only/dry-run scope.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


DEFAULT_OUT_DIR = Path("target/oprs-worker-runs")
ALLOWED_ENV_KEYS = {
    "HELIUS_RPC_URL",
    "OPRS_WORKER_MODE",
    "OPRS_OUTPUT_MODE",
    "OPRS_TARGET_PROTOCOLS",
    "OPRS_RUN_LIMIT",
    "OPRS_ALERT_DESTINATION",
}
BLOCKED_ENV_KEY_MARKERS = (
    "PRIVATE_KEY",
    "SEED",
    "KEYPAIR",
    "WALLET",
    "SIGNER",
    "CUSTODY",
    "CAPITAL",
    "BLOCK_ENGINE",
)
REDACTIONS = {
    "rpc_url": re.compile(r"https://[^\"'\s]*(helius|rpc|api-key|apikey)[^\"'\s]*", re.IGNORECASE),
    "slack_webhook": re.compile(r"https://hooks\.slack(?:-gov)?\.com/services/[a-z0-9/_-]+", re.IGNORECASE),
    "bearer": re.compile(r"bearer\s+[a-z0-9._-]+", re.IGNORECASE),
}


@dataclass(frozen=True)
class WorkerJob:
    job_id: str
    description: str
    output_file: Optional[str]
    command: tuple[str, ...]
    validators: tuple[tuple[str, ...], ...] = ()


def _job_catalog(out_dir: Path) -> dict[str, WorkerJob]:
    drift_state_out = out_dir / "drift-state-smoke.json"
    jupiter_role_map_out = out_dir / "jupiter-role-map-smoke.json"
    phoenix_out = out_dir / "phoenix-market-telemetry-smoke.json"
    return {
        "slack-sample-dry-run": WorkerJob(
            job_id="slack-sample-dry-run",
            description="Validate and preview the checked-in Slack alert sample without network delivery.",
            output_file=None,
            command=("scripts/send_slack_alert_sample.py", "--dry-run"),
        ),
        "drift-state-smoke": WorkerJob(
            job_id="drift-state-smoke",
            description="Fetch reviewed Drift public/shape fields with local read-only RPC and validate output.",
            output_file=str(drift_state_out),
            command=(
                "scripts/discover_drift_readonly_state.py",
                "--env-file",
                ".env",
                "--include-shape-snapshot",
                "--include-public-fields",
                "--out",
                str(drift_state_out),
            ),
            validators=(("scripts/validate_drift_readonly_state.py", str(drift_state_out)),),
        ),
        "jupiter-role-map-smoke": WorkerJob(
            job_id="jupiter-role-map-smoke",
            description="Sample public Jupiter Perps transactions and bind account roles to the onchain IDL.",
            output_file=str(jupiter_role_map_out),
            command=(
                "scripts/discover_jupiter_lifecycle_role_map.py",
                "--env-file",
                ".env",
                "--limit",
                "10",
                "--transaction-limit",
                "5",
                "--out",
                str(jupiter_role_map_out),
            ),
            validators=(
                ("scripts/validate_jupiter_lifecycle_role_map_probe.py", str(jupiter_role_map_out)),
            ),
        ),
        "phoenix-telemetry-smoke": WorkerJob(
            job_id="phoenix-telemetry-smoke",
            description="Fetch bounded public Phoenix market telemetry and validate the scrubbed probe.",
            output_file=str(phoenix_out),
            command=(
                "scripts/discover_phoenix_market_telemetry.py",
                "--max-markets",
                "8",
                "--out",
                str(phoenix_out),
            ),
            validators=(("scripts/validate_phoenix_market_telemetry_probe.py", str(phoenix_out)),),
        ),
    }


def _load_allowed_env(env_file: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not env_file.exists():
        return values
    for line_number, raw_line in enumerate(env_file.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip().removeprefix("export ").strip()
        value = value.strip().strip("'\"")
        if any(marker in key.upper() for marker in BLOCKED_ENV_KEY_MARKERS):
            raise ValueError(f"{env_file}:{line_number}: blocked worker env key marker: {key}")
        if key in ALLOWED_ENV_KEYS:
            values[key] = value
    return values


def _scrub_output(text: str) -> str:
    scrubbed = text
    for label, pattern in REDACTIONS.items():
        scrubbed = pattern.sub(f"[redacted_{label}]", scrubbed)
    return scrubbed


def _run_command(command: tuple[str, ...], env: dict[str, str]) -> int:
    result = subprocess.run(
        command,
        check=False,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.stdout:
        print(_scrub_output(result.stdout), end="")
    if result.stderr:
        print(_scrub_output(result.stderr), end="", file=sys.stderr)
    return result.returncode


def _plan(job: WorkerJob, execute: bool) -> dict[str, object]:
    return {
        "worker": "oprs-readonly-worker-local-wrapper",
        "mode": "one_shot_local_read_only",
        "execute": execute,
        "job": job.job_id,
        "description": job.description,
        "output_file": job.output_file,
        "command": list(job.command),
        "validators": [list(validator) for validator in job.validators],
        "safety_invariants": {
            "signing_enabled": False,
            "transaction_submission_enabled": False,
            "priority_fee_bidding_enabled": False,
            "keypair_loading_enabled": False,
            "custody_enabled": False,
            "capital_management_enabled": False,
            "live_slack_worker_output_enabled": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    parser.add_argument("--job", choices=sorted(_job_catalog(DEFAULT_OUT_DIR)), required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--plan", action="store_true", help="Print the safe job plan. This is the default.")
    mode.add_argument("--execute", action="store_true", help="Execute the allowlisted job and validators.")
    args = parser.parse_args()

    catalog = _job_catalog(args.out_dir)
    job = catalog[args.job]
    execute = bool(args.execute)
    print(json.dumps(_plan(job, execute), indent=2, sort_keys=True))
    if not execute:
        return 0

    args.out_dir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    try:
        env.update(_load_allowed_env(args.env_file))
    except ValueError as exc:
        print(f"Worker env validation failed: {exc}", file=sys.stderr)
        return 2

    code = _run_command(job.command, env)
    if code != 0:
        return code
    for validator in job.validators:
        code = _run_command(validator, env)
        if code != 0:
            return code
    print(f"PASS read-only worker job: {job.job_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
