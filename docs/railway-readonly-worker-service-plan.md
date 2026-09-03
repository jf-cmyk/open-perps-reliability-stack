# Railway Read-Only Worker Service Plan

This plan defines the first server-side service that can move Open Perps Reliability Stack beyond the static MVP while preserving the read-only and dry-run scope.

Current Railway worker boundary: `oprs-readonly-worker`.

Status: created as an empty Railway service with no source, no public URL, no deployment, and no variables. Keep it empty until the first worker command, schedule, and retention policy are selected.

## Purpose

The read-only worker service periodically fetches public Solana data, decodes reviewed protocol surfaces, validates data quality, and emits scrubbed reliability outputs for private diagnostics and later public proof packs.

It must never sign, build, submit, retry, prioritize, or route transactions.

## Service Separation

The current Railway service, `refreshing-art`, remains the canonical static proof-pack service. It serves checked-in public artifacts only.

The worker must remain a separate Railway service, `oprs-readonly-worker`, with its own variables, deploy logs, monitoring, and failure policy.

Static proof-pack service:

- Public.
- No secrets.
- No RPC.
- No background jobs.
- No server-side decoding.
- No private outputs.

Read-only worker service:

- Private or restricted by default.
- May use read-only RPC credentials.
- Runs bounded scheduled jobs.
- Writes only scrubbed outputs.
- Publishes public artifacts only after validation and review.

## Initial Service Shape

Runtime:

- Python worker first, because current read-only probes are Python scripts.
- One command per bounded job.
- No web server required for the first worker iteration unless Railway requires a health surface.

Initial job candidates:

1. Drift target/state scan using `scripts/discover_drift_readonly_state.py`.
2. Drift liquidation-history pagination using `scripts/discover_drift_liquidation_history.py`.
3. Jupiter lifecycle role-map probe using `scripts/discover_jupiter_lifecycle_role_map.py`.
4. Phoenix market telemetry probe using `scripts/discover_phoenix_market_telemetry.py`.

Initial outputs:

- Worker run envelope.
- Probe-specific JSON under a private output location.
- Scrubbed public candidate only after validator pass.
- Summary line with no secrets, raw account bytes, raw transaction bodies, wallet inventory, or private routes.

## Railway Variables

Required for worker only:

- `HELIUS_RPC_URL`: read-only Solana HTTPS RPC endpoint.
- `OPRS_WORKER_MODE`: set to `read_only`.
- `OPRS_OUTPUT_MODE`: set to `private_target` for the first hosted runs.
- `OPRS_TARGET_PROTOCOLS`: comma-separated allowlist, initially `drift,jupiter,phoenix`.
- `OPRS_RUN_LIMIT`: bounded per-run item limit, initially low.

Optional later:

- `OPRS_ALERT_WEBHOOK_URL`: alert destination for failed or stale runs.
- `OPRS_PUBLIC_OUTPUTS_ENABLED`: default `false`; public publishing needs review.
- `OPRS_RUN_INTERVAL_MINUTES`: desired scheduler interval if Railway scheduling is used.
- `OPRS_RETENTION_DAYS`: private output retention target.

Forbidden variables:

- private keys
- seed phrases
- wallet files
- signer config
- custody config
- capital limits
- block-engine endpoints
- priority-fee strategy
- transaction submission endpoints
- trading inventory or route strategy

## Railway Setup Sequence

Founder has approved creating the separate worker boundary. The service exists, but source deployment, variables, schedule, public outputs, and retention still require the exact worker command and operational policy.

1. Keep `refreshing-art` linked to the static proof pack.
2. Use `oprs-readonly-worker` for worker variables and worker status.
3. Add only read-only variables to the worker service.
4. Configure the worker command with a low bounded run limit.
5. Run once manually and inspect logs for secret leakage.
6. Validate the generated output locally before committing any scrubbed artifact.
7. Enable scheduled runs only after the 7-day soak runbook is ready.

## First Manual Run Contract

The first hosted worker run should target a tiny bounded probe, such as:

```bash
scripts/discover_jupiter_lifecycle_role_map.py --signature-limit 10 --transaction-limit 5 --out target/oprs-jupiter-lifecycle-role-map/railway-smoke.json
```

Acceptance criteria:

- Job exits successfully.
- Logs do not include `HELIUS_RPC_URL` or the RPC URL value.
- Logs do not include API keys, bearer tokens, private keys, seed phrases, or wallet paths.
- Output includes source, slot/signature metadata, provider label, checksum or hash fields, and claim-boundary flags.
- Output stays private until a validator produces a scrubbed public candidate.

The 7-day soak summary must follow `schemas/datasets/readonly-soak-summary-v0.json` and pass `scripts/validate_readonly_soak_summary.py`.

## Output Promotion Gates

A worker output can move from private run output to public proof-pack candidate only after:

- probe-specific validator passes
- secret-marker scan passes
- raw account bytes are absent
- raw transaction bodies are absent unless a later source-reviewed schema explicitly allows them
- signer, custody, capital, and submission flags are false
- source references and hashable provenance are present
- claim boundary is explicit
- checkpoint records the run and next queue

## Failure Policy

Fail closed:

- If source authority is ambiguous, mark the output partial.
- If provider errors occur, mark freshness degraded.
- If schema validation fails, do not publish.
- If secret markers appear, stop the worker and rotate affected credentials.
- If transaction-surface markers appear, treat it as a scope violation and block promotion.

## Ready-To-Build Criteria

We are ready to implement the worker service when:

- The founder confirms the first worker command, schedule, and retention policy.
- `docs/read-only-soak-runbook.md` exists and is linked.
- Static proof-pack hosted smoke checks pass.
- At least one local worker probe has a passing validator.
- The exact first worker command and run limit are selected.

Until then, keep `oprs-readonly-worker` as an empty, private, no-secret service boundary.

See [Access and operations setup](access-ops-setup.md) for safe variable commands, alert destination rules, and custom-domain setup.
