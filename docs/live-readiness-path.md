# Live Readiness Path

This document defines how the Open Perps Reliability Stack moves from the current hosted MVP toward live services without weakening the read-only and dry-run boundary.

## Current Status

As of 2026-09-01, the project has a hosted static proof-pack MVP on Railway and GitHub Pages. It provides public docs, schemas, examples, synthetic fixtures, static dashboard views, Drift guardrail evidence, Jupiter onchain-IDL layout decode evidence, a Jupiter lifecycle role-map probe contract, Phoenix telemetry planning, and validation commands.

The MVP is useful for grant review, protocol conversations, and early commercial discovery. It is not a production trading system.

Allowed today:

- Public static proof pack.
- Public static dashboard.
- Local read-only RPC probes.
- Source-governed adapter research.
- Synthetic dry-run replay fixtures.
- Scrubbed examples and public package contracts.

Blocked today:

- Production trading.
- Live transaction submission.
- Signing, wallet loading, custody, or capital deployment.
- Priority-fee bidding or block-engine submission.
- Autonomous liquidator execution.
- Claims that Drift liquidation absence, Jupiter lifecycle pairing, or Phoenix replay is proven.

## Definitions Of Live

The word "live" has three different meanings in this initiative. They must stay separate.

### Live Public Proof Pack

Status: active.

This is the current Railway and GitHub Pages deployment. It is public, hosted, and reviewer-facing, but inert. It serves checked-in files only and has no RPC, secrets, signer, wallet, custody, or transaction-submission capability.

### Live Read-Only Service

Status: next commercial/grant-safe service lane.

This is a server-side service that periodically fetches public Solana data, decodes protocol state, computes reliability metrics, and publishes scrubbed outputs. It can support paid diagnostics, protocol reports, dashboards, and integration support without touching funds or submitting transactions.

This is the safest path to revenue before execution.

Current worker boundary: Railway service `oprs-readonly-worker` exists as an empty, no-secret service. It is not operationally live until source, command, schedule, retention, alerting, validation, and a 7-day soak are complete.

### Live Execution Pilot

Status: blocked until a separate approval package exists.

This is any system that builds, signs, submits, retries, prioritizes, or routes transactions. It requires security review, legal review, capital approval, key-management design, incident response, monitoring, circuit breakers, and explicit founder approval before implementation or deployment.

See [Execution pilot scope](execution-pilot-scope.md) for the exact future approval package.

## Path To Bring This Live

### Phase 0: Static MVP

Goal: make the project credible to reviewers and prospective partners.

Current status: mostly complete.

Required gates:

- `scripts/run_mvp_checks.sh` passes locally.
- Railway serves the proof pack and dashboard.
- GitHub Pages fallback serves the same public artifact.
- Hosted smoke checks pass on Railway and GitHub Pages.
- Grant proposal and proof-pack links are current.
- Checkpoint docs describe exactly where to resume.

Exit signal:

- A reviewer can inspect the hosted proof pack, reproduce local validation, and understand the no-execution boundary.

### Phase 1: Post-MVP Alpha

Goal: turn static proof into repeatable read-only evidence.

Required gates:

- Add a scheduled read-only worker design with no secrets in public outputs.
- Use [Railway read-only worker service plan](railway-readonly-worker-service-plan.md) before configuring or deploying the hosted worker service.
- Run at least one source-backed replay-adjacent dataset through the public package contract.
- Continue Drift liquidation-history pagination until a source-backed candidate is found or the search boundary is revised.
- Convert Jupiter lifecycle role-map output into a verified-pairing validator design, while keeping pairing claims blocked until before/after state evidence exists.
- Choose the next protocol lane: Drift-only depth, Jupiter pairing, or Phoenix account-level telemetry.
- Record every material source decision in `docs/source-review-records.md`.

Exit signal:

- The project can regenerate scrubbed evidence from public Solana data on demand and explain exactly which claims are proven, partial, or blocked.

### Phase 2: Live Read-Only Service

Goal: operate a hosted diagnostics service without execution capability.

Required gates:

- Deploy a backend worker/service separate from the static proof pack.
- Add Railway variables only for read-only infrastructure, such as `HELIUS_RPC_URL`.
- Keep the public static proof-pack service free of secrets.
- Add API authentication before exposing non-public diagnostics.
- Add source, slot, provider, freshness, checksum, and scrub metadata to every generated dataset.
- Add monitoring for worker success, provider failures, schema drift, stale oracle inputs, and data-quality downgrades.
- Run [continuous read-only jobs for at least 7 days](read-only-soak-runbook.md) without secret leakage or unchecked output drift.

Exit signal:

- A protocol, market maker, builder, or grant reviewer can rely on fresh read-only reliability diagnostics, while the service still cannot sign or submit transactions.

### Phase 3: Commercial Diagnostics

Goal: earn revenue before execution by selling reliability intelligence, integration support, and protocol-specific proof packs.

Required gates:

- Package a paid diagnostics API or private dashboard around read-only outputs.
- Define customer-facing terms that exclude custody, trading advice, execution guarantees, and profit guarantees.
- Define support packages for protocol adapters, proof-pack production, data-quality review, and incident retrospectives.
- Add billing/auth only after founder approval of the commercial scope.
- Keep grant-funded OSS artifacts public and non-privatized.
- Start from [Commercial diagnostics brief](commercial-diagnostics-brief.md) and validate scope with a specific buyer before publishing pricing.
- Use [Commercial diagnostics pricing](commercial-diagnostics-pricing.md) as the current structural price test.

Exit signal:

- The company can sell read-only reliability deliverables without operating a liquidator or touching capital.

### Phase 4: Execution Readiness Candidate

Goal: decide whether an execution pilot should exist at all.

Required gates:

- Threat model and security review.
- Legal and compliance review.
- Explicit wallet, signer, custody, and capital policy.
- Isolated hot-wallet design with capped funds.
- Circuit breakers for oracle confidence, stale data, mark divergence, adapter mismatch, liquidity, transaction failures, and venue-specific risk.
- Runbooks for incident response, pausing, alerting, rollback, and postmortems.
- Testnet/devnet rehearsal where available.
- Dry-run-to-live equivalence tests.
- Founder approval for the exact protocol, venue, wallet, limits, operators, and pilot duration.

Exit signal:

- The team has enough evidence and controls to consider a narrow execution pilot. This still does not authorize production trading by default.

## When We Are Ready To Move Past MVP

The project is ready to move past MVP into post-MVP alpha when all of the following are true:

- Static MVP validation and hosted smoke checks pass.
- Current grant and proof-pack docs reflect the latest evidence.
- At least one protocol lane has a credible next evidence target that does not require production execution.
- The next read-only worker or validator can run locally with `.env` secrets and commit only scrubbed outputs.
- The checkpoint and context map identify the exact next command or validator to run.

The project is ready to move into a live read-only service when all of the following are true:

- Post-MVP alpha outputs are repeatable from public Solana sources.
- Secret handling is isolated to Railway variables or local `.env` files and never copied into public artifacts.
- A backend service exists separately from the static proof pack.
- Dataset generation includes source, slot, provider, freshness, checksum, and scrub metadata.
- The service has alerting and runbooks for provider failures, schema drift, stale data, and bad outputs.
- A 7-day continuous read-only soak produces useful results without secret leakage or unexplained data drift.

The project is ready to discuss an execution pilot only when all of the following are true:

- Live read-only service is stable.
- Source-backed replay evidence exists for the target venue.
- Security, legal, capital, signer, monitoring, incident-response, and operator approvals are complete.
- Founder approves a written execution pilot scope.

## Access Or Confirmation Needed

Needed now:

- Confirm the first post-MVP live lane: read-only diagnostics API, private protocol dashboard, or protocol-specific proof-pack support.
- Provide the exact custom domain when a branded public URL is desired.
- Create the private Slack incoming webhook outside the repo and store it as `OPRS_ALERT_WEBHOOK_URL`.
- Confirm the first worker command, run schedule, and retention policy before deploying source to `oprs-readonly-worker`.

Why these require consent:

- Separate Railway worker service: creates a new hosted process that may hold read-only RPC credentials, run on a schedule, generate private outputs, and incur cloud usage. Even without execution, that changes the operational and secret-handling boundary.
- First post-MVP commercial lane: determines what Blocksize sells first, what claims can be made publicly, how grant-funded OSS stays separated from paid work, and which customer evidence should be collected.
- Production custom domain: changes the public canonical URL, brand surface, reviewer links, DNS ownership, and maintenance burden.
- Monitoring destination: routes operational alerts into Slack. Alerts can contain protocol names, failure metadata, and private operational context, so the channel and webhook should be intentionally private.
- Execution pilot: introduces signing, wallet, custody, transaction-submission, capital, legal, and security risk. It needs a separate written approval package and is not implied by any read-only worker or diagnostics launch.

Not needed now:

- Private keys.
- Seed phrases.
- Signer configuration.
- Wallet files.
- Capital.
- Block-engine credentials.
- Priority-fee policy.

Do not paste secrets into chat. Use local `.env` for development and Railway variables for hosted read-only services.

## Recommended Next Build Tasks

1. Keep Railway static proof pack canonical and GitHub Pages as fallback.
2. Add a separate read-only worker service plan before adding any server-side secrets.
3. Add a 7-day read-only soak checklist and runbook before deploying any recurring worker.
4. Continue Drift liquidation-history pagination from the current cursor.
5. Turn the Jupiter role-map probe into a verified-pairing validator design, but keep lifecycle proof blocked until before/after state evidence exists.
6. Validate the commercial diagnostics brief with a specific buyer profile and package scope.
7. Configure alerts and custom domain using [Access and operations setup](access-ops-setup.md).
