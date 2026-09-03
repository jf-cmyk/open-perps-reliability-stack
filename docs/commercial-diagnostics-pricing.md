# Commercial Diagnostics Pricing

This is a structural pricing note for Blocksize's Open Perps Reliability Stack commercial lane. It uses current public vendor pricing as of 2026-09-03, but it is not yet a customer-validated price book.

## Evidence Posture

Known:

- Railway charges for compute by usage and offers Hobby at a $5 minimum and Pro at a $20 minimum. Railway also lists service variables, custom domains, logs, metrics, alerts, and webhooks as platform capabilities. Source: https://railway.com/pricing
- Helius lists Free, Developer, Business, Professional, and Enterprise plans. Developer is $49/month, Business is $499/month, Professional is $999/month, and LaserStream is included with Business and higher. Source: https://www.helius.dev/pricing
- Goldsky has a $100 starter credit, usage-based Scale, custom Enterprise, Edge RPC at $5 per 1M requests on Scale, and Turbo pipelines at $0.10 per worker hour plus event usage after the included tier. Source: https://goldsky.com/pricing
- Dune bills API usage with credits. The Queries endpoint is available on Plus and Enterprise, webhooks vary by plan, and exports consume credits per MB. Source: https://docs.dune.com/api-reference/overview/billing
- QuickNode's Solana flat-rate RPS tiers start at $1,199/month for 75 RPS, then $2,299/month for 150 RPS and $2,925/month for 250 RPS. Source: https://support.quicknode.com/articles/7155954804-flat-rate-rps-billing
- Retool cloud pricing lists Team at $10/month per builder and $5/month per internal user, Business at $50/month per builder and $15/month per internal user, with external-user pricing starting on Business for the first 50 external users at free and then tiered. Source: https://retool.com/pricing

Inferred:

- Helius is the default near-term read-only RPC provider because the founder already has Helius access and the repo already supports a `HELIUS_RPC_URL` boundary.
- Goldsky or Dune can become supplemental historical/indexed data providers if direct RPC scans are too slow or too costly.
- QuickNode flat-rate Solana RPS is a production-scale alternative when fixed-capacity RPC economics matter more than low-cost alpha validation.
- A self-built Railway dashboard/API is better than Retool for the first OSS-aligned product surface because the current proof pack is already deployed on Railway and needs transparent public artifacts.

Missing:

- Customer willingness to pay.
- Target customer size and SLA requirements.
- Required retention window, request volume, and number of protocols per private dashboard.
- Whether public API access is free, metered, sponsor-funded, or bundled with a grant.

## Recommended Package Lanes

### 1. Public Proof-Pack And API Lane

Customer:

- Solana Foundation reviewers, protocols, integrators, researchers, and ecosystem builders.

Deliverables:

- Public proof-pack docs, schemas, examples, and fixture contracts.
- Public static dashboard.
- Public read-only API examples.
- Public source-review records and claim-boundary notes.
- Optional low-volume public API after the worker has a safe publishing path.

Infrastructure assumption:

- Railway `refreshing-art` remains canonical.
- GitHub Pages remains a mirror.
- Helius Hobby/Developer-level RPC can support local and low-volume read-only proof generation, but no secret goes to the static service.

Suggested pricing posture:

- Public OSS artifact: free.
- Grant-funded build/support ask: price by milestone, not API calls.
- Sponsored public API, if added later: $0 for limited public use with hard rate limits, or sponsor-funded at roughly $500-$2,500/month to cover hosting, RPC, monitoring, and maintenance.

Why this works:

- It strengthens the grant narrative.
- It keeps public goods public.
- It creates distribution before commercial lock-in.

Why this is not enough for revenue:

- Public access alone does not pay for protocol-specific support, private dashboards, SLA, or custom adapter work.

### 2. Private Dashboard And Read-Only API Lane

Customer:

- Perps protocols, market makers, integrators, and infrastructure teams that need private reliability visibility without exposing strategy.

Deliverables:

- Authenticated private dashboard.
- Private read-only API.
- Protocol-specific adapters and decode confidence matrix.
- Freshness, schema drift, oracle health, liquidation-history, and replay-readiness indicators.
- Weekly reliability summary and incident/postmortem support.

Infrastructure assumption:

- Railway Pro should be the first paid hosting baseline once this is customer-facing because it gives higher limits, team collaboration, longer log history, and production posture than Hobby.
- Helius Business is the first serious read-only streaming/RPC budget line if LaserStream or higher limits are required.
- Goldsky/Dune are optional indexed-data accelerators.
- Retool is an optional internal-dashboard shortcut, but not the canonical public artifact path.

Suggested pricing posture:

| Package | Setup | Monthly | Best Fit | Notes |
| --- | ---: | ---: | --- | --- |
| Private Alpha Dashboard | $7,500-$15,000 | $1,500-$3,500 | One protocol, narrow metrics, weekly review | Mostly Railway plus Helius Developer/Business depending volume |
| Protocol Reliability Pack | $15,000-$35,000 | $3,500-$8,000 | Protocol or market maker needing adapter and reliability review | Includes source authority, private dashboard/API, support, and proof-pack output |
| Reliability Ops Retainer | $25,000-$60,000 | $8,000-$20,000 | Multi-venue or higher-SLA customer | Requires clearer support scope, alerting, retention, and provider budget |

Commercial terms should exclude custody, trading advice, execution guarantees, profit guarantees, capital control, and emergency trading operations.

### 3. Enterprise Or High-Volume API Lane

Customer:

- Larger trading teams, analytics providers, infrastructure vendors, or protocols that need higher request volumes, stronger support, custom retention, or multi-region resilience.

Deliverables:

- Dedicated customer API.
- SLA-backed data freshness target.
- Private retention and export policy.
- Custom source-governance records.
- Optional indexed data lake or warehouse export.

Infrastructure assumption:

- Helius Professional or Enterprise, or QuickNode flat-rate Solana RPS, depending on load profile.
- Railway Pro or Enterprise if compliance, SSO, longer audit/log retention, or higher support is required.
- Goldsky/Dune for indexed history when direct RPC scans are too expensive.

Suggested pricing posture:

- Paid discovery/design: $10,000-$25,000.
- Implementation: $40,000-$120,000.
- Monthly platform/support: $15,000-$50,000 plus pass-through infrastructure above an agreed cap.

This lane should not be sold until a buyer confirms volume, uptime, support, and data-retention requirements.

## Public Vs Private Access Model

Public access:

- Static docs, schemas, fixture examples, and a public dashboard.
- Public API can expose only scrubbed, rate-limited, non-customer-specific data.
- No private customer labels, strategy thresholds, wallets, raw account bytes, raw transaction bodies, or internal incident notes.

Private access:

- Authenticated dashboard and API.
- Customer-specific protocols, watchlists, incidents, freshness labels, and run history.
- Strict secret isolation in Railway worker variables or another server-side secrets manager.
- Customer-specific outputs stay private unless explicitly promoted.

## Recommended First Price Test

Lead with a paid "Protocol Reliability Pack":

- Two-week fixed-scope sprint.
- One target venue or protocol lane.
- Deliver source-authority review, adapter/read-only probe, private dashboard sketch, public proof-pack candidate, and final reliability memo.
- Price test: $15,000 fixed fee.
- Optional follow-on: $3,500/month for weekly refresh, source drift monitoring, and proof-pack maintenance.

The reason to start here is simple: it sells the artifact quality already built, does not require execution, and can produce both commercial value and public-good outputs.

## Validation Questions For First Buyer

1. Which venue or protocol do they need independent reliability evidence for?
2. What decision does the evidence support: grant, listing, integration, market-making, incident review, or internal risk?
3. How fresh must data be: hourly, daily, weekly, or on-demand?
4. Which output matters most: public proof pack, private dashboard, API, or memo?
5. What must remain private?
6. What is their budget owner: engineering, risk, growth, market ops, foundation/ecosystem, or protocol leadership?

## Pricing Guardrails

- Do not sell execution.
- Do not promise liquidation coverage.
- Do not sell profit improvement.
- Do not imply audited protocol safety.
- Do not expose customer-private findings in grant-funded OSS artifacts.
- Do not put API keys in public dashboards or client-side code.
