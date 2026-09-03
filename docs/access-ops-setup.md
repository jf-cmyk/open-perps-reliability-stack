# Access And Operations Setup

This note records the approved post-MVP operations items and the exact setup path for alerting, the Railway worker boundary, and custom domains.

## Current Consent State

Approved:

- Alert destination setup: Slack.
- Separate Railway worker service.
- Commercial lane pricing research for private dashboards and public API access.
- Custom domain setup.

Still not approved by this document:

- Signing.
- Custody.
- Wallet loading.
- Private-key storage.
- Live transaction submission.
- Capital deployment.
- Autonomous liquidation execution.

## Railway Services

Current service split:

| Service | Purpose | Secrets | Public URL |
| --- | --- | --- | --- |
| `refreshing-art` | Canonical static proof pack and dashboard | None | `https://refreshing-art-production-86de.up.railway.app` |
| `oprs-readonly-worker` | Empty worker boundary for future read-only jobs | `HELIUS_RPC_URL` plus non-secret mode variables | None |

The `oprs-readonly-worker` service was created as an empty service. It has no deployment source and no public URL. Its read-only RPC secret is stored only as a Railway worker variable, and non-secret guardrail variables are set: `OPRS_WORKER_MODE`, `OPRS_OUTPUT_MODE`, `OPRS_TARGET_PROTOCOLS`, `OPRS_RUN_LIMIT`, and `OPRS_ALERT_DESTINATION=slack`.

Keep the local Railway link on `refreshing-art` for ordinary static proof-pack deploys:

```bash
railway service link refreshing-art
```

Use explicit `--service oprs-readonly-worker` flags for worker variables and worker status so the static site never receives read-only RPC credentials.

## Safe Variable Setup

Use Railway variables only on `oprs-readonly-worker`.

Do not paste secrets into chat. Do not put secret values in docs. Do not use `railway variable list --json` or `railway variable list --kv` in shared output because those modes can reveal raw values.

Recommended non-secret variable commands:

```bash
railway variable set OPRS_WORKER_MODE=read_only --service oprs-readonly-worker --skip-deploys
railway variable set OPRS_OUTPUT_MODE=private_target --service oprs-readonly-worker --skip-deploys
railway variable set OPRS_TARGET_PROTOCOLS=drift,jupiter,phoenix --service oprs-readonly-worker --skip-deploys
railway variable set OPRS_RUN_LIMIT=10 --service oprs-readonly-worker --skip-deploys
railway variable set OPRS_ALERT_DESTINATION=slack --service oprs-readonly-worker --skip-deploys
```

Read-only RPC secret setup command, already approved and applied for `oprs-readonly-worker`:

```bash
printf "%s" "PASTE_HELIUS_RPC_URL_HERE" | railway variable set HELIUS_RPC_URL --stdin --service oprs-readonly-worker --skip-deploys
```

Slack webhook secret, after the founder creates a Slack incoming webhook:

```bash
read -r -s OPRS_ALERT_WEBHOOK_URL
printf "%s" "$OPRS_ALERT_WEBHOOK_URL" | railway variable set OPRS_ALERT_WEBHOOK_URL --stdin --service oprs-readonly-worker --skip-deploys
unset OPRS_ALERT_WEBHOOK_URL
```

Why stdin matters: it avoids putting key material directly in the shell command. The variable value can still exist in terminal scrollback if pasted visibly, so paste only at the prompt or from a password manager.

## Alert Destination

Selected alert destination:

- Slack incoming webhook.

Do not use a public channel for worker alerts. Alerts can mention protocol names, run status, error classes, data-quality downgrades, and freshness issues.

See [Slack alerting](slack-alerting.md) for the setup guide, schema, example payload, and local validator.

Initial alert payload should include only:

- service name
- run id
- protocol
- status
- error class
- freshness label
- checksum presence flag
- link to Railway deployment/logs, if available

Initial alert payload must exclude:

- RPC URL
- API keys
- bearer tokens
- private route metadata
- raw transaction bodies
- raw account bytes
- wallet addresses tied to Blocksize-controlled inventory
- signer, custody, capital, or execution policy fields

## Custom Domain

Railway supports generated `*.up.railway.app` service domains and custom domains. Railway's CLI docs say adding a custom domain returns the required DNS records; custom domains require both a CNAME and TXT record, and DNS propagation can take up to 72 hours.

Source: https://docs.railway.com/cli/domain

Recommended command after the founder selects the domain:

```bash
railway domain YOUR_DOMAIN_HERE --service refreshing-art --json
```

Then add the returned DNS records at the domain registrar:

- CNAME record: routes traffic.
- TXT record: verifies ownership.

Check status:

```bash
railway domain status YOUR_DOMAIN_HERE
railway domain list --service refreshing-art
```

Do not attach the custom public domain to `oprs-readonly-worker` unless the worker later exposes a deliberately authenticated API. The public reviewer domain should point to `refreshing-art`.

## Immediate Next Safe Steps

1. Add worker variables using stdin only after the first worker command is selected.
2. Create a Slack incoming webhook outside the repo and store it as `OPRS_ALERT_WEBHOOK_URL`.
3. Select the public domain name for the proof pack.
4. Run hosted smoke checks after domain verification.
5. Keep `oprs-readonly-worker` private and source-less until the worker command, schedule, and retention policy are explicit.
