# Slack Alerting

This document defines the Slack alert path for the read-only Railway worker.

## Current Status

- Alert destination: Slack.
- Railway worker service: `oprs-readonly-worker`.
- Non-secret Railway variable set: `OPRS_ALERT_DESTINATION=slack`.
- Secret webhook variable: not set until the founder creates a Slack incoming webhook and stores it with stdin.

## Why Slack

Slack is the first alert destination because worker alerts are operational, time-sensitive, and occasionally private. A dedicated private channel makes failures visible without exposing webhook secrets, RPC credentials, private run metadata, or customer-specific findings.

## Slack Setup

Slack's official incoming webhook flow is:

1. Create a Slack app or use an existing app.
2. Enable Incoming Webhooks.
3. Add a new webhook to the workspace.
4. Select the private channel where worker alerts should appear.
5. Copy the webhook URL.

Slack notes that webhook URLs are secrets and should not be shared publicly or committed.

Sources:

- https://api.slack.com/messaging/webhooks
- https://docs.slack.dev/reference/scopes/incoming-webhook

## Recommended Channel

Create a private channel such as:

```text
#oprs-alerts
```

Invite only the founder/operator set that should see:

- protocol names
- worker run ids
- provider failure classes
- data-quality downgrades
- stale-input alerts
- source-drift alerts
- links to private Railway worker logs

## Store The Webhook In Railway

Run this from the repo root after copying the Slack webhook URL:

```bash
printf "%s" "PASTE_SLACK_WEBHOOK_URL_HERE" | railway variable set OPRS_ALERT_WEBHOOK_URL --stdin --service oprs-readonly-worker --skip-deploys
```

Do not paste the webhook into chat. Do not use `railway variable list --json` or `railway variable list --kv` after setting it because those modes can reveal raw values.

## Alert Payload Contract

Schema:

- `schemas/datasets/slack-alert-payload-v0.json`

Example:

- `examples/datasets/slack_alert_payload_example.json`

Validator:

```bash
scripts/validate_slack_alert_payload.py
```

## Allowed Payload Fields

Slack alerts may include:

- service name
- run id
- protocol
- severity
- status
- error class
- freshness label
- checksum presence flag
- source link to public docs
- private Railway log link, if available

Slack alerts must not include:

- RPC URL
- Helius key
- Jupiter key
- Slack webhook URL
- bearer token
- private key
- seed phrase
- wallet file path
- raw transaction body
- raw account bytes
- signer settings
- custody fields
- capital settings
- execution policy

## Initial Alert Types

Start with only these alert classes:

| Alert Class | Severity | Meaning |
| --- | --- | --- |
| `worker_failed_closed` | `error` | Worker exited or refused output safely. |
| `provider_failure` | `warning` | Read-only RPC/API provider failed or rate-limited. |
| `schema_validation_failed` | `error` | Output failed schema or validator checks. |
| `secret_marker_found` | `critical` | Output/log text appears to include a secret marker. |
| `execution_marker_found` | `critical` | Output/log text appears to include signing/submission/capital language. |
| `stale_input_detected` | `warning` | Source data freshness fell below the run threshold. |
| `worker_soak_passed` | `info` | Daily soak check passed without publishing private output. |

## Test Rule

The first Slack test should send only the checked-in sample payload after the webhook is configured. Do not send live worker output until the local validator passes.
