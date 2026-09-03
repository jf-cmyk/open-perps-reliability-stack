# Execution Pilot Scope

This document answers what an execution pilot would mean for OPRS. It does not authorize execution and does not add execution code.

## Short Answer

An execution pilot is a narrow, written, time-boxed mainnet or testnet experiment where the system is allowed to build, sign, and submit specific transactions under strict controls.

That is fundamentally different from the current MVP and the next live read-only service. The current stack observes, decodes, validates, and dry-runs. An execution pilot would touch wallets, signing, submission, fees, risk controls, incident response, and legal/compliance review.

## What Changes In An Execution Pilot

Current MVP:

- static proof pack
- read-only data
- synthetic dry-run replay
- scrubbed public examples
- no wallet
- no signing
- no transaction submission
- no capital

Execution pilot:

- selected wallet or signer
- transaction construction
- simulation and preflight policy
- transaction submission path
- retry/expiry policy
- priority-fee or landing policy, if approved
- live monitoring and kill switch
- incident runbook
- capital cap and loss policy

## Minimum Written Scope

Before any execution implementation begins, the founder should approve a written scope with:

| Area | Required Decision | Why It Matters |
| --- | --- | --- |
| Venue | Exact protocol and program surface | Prevents broad or accidental execution across venues |
| Action | Exact instruction/action type | Separates observation from capital-moving behavior |
| Environment | Devnet, testnet, or mainnet | Determines real-funds risk |
| Wallet | Signer owner and custody model | Controls who can move funds |
| Capital | Maximum funds, token types, and loss cap | Limits downside |
| Duration | Start, stop, and extension policy | Keeps pilot time-boxed |
| Operator | Human on-call owner | Defines who pauses or approves changes |
| Risk Controls | Circuit breakers and thresholds | Stops unsafe submissions |
| Monitoring | Alert destination and escalation | Makes failures visible quickly |
| Logs | Retention and scrub rules | Enables review without leaking secrets |
| Legal | Jurisdiction and compliance review | Avoids accidentally becoming a regulated trading operation |
| Rollback | Disable and revoke path | Ensures the pilot can be shut down |

## Reasonable First Execution Pilot Shape

If the project ever moves past read-only, the first responsible scope would be:

- One protocol.
- One low-risk action type.
- One isolated hot wallet.
- Mainnet only after devnet/testnet or simulator equivalence gates pass.
- Tiny capital cap.
- Manual human enablement.
- No autonomous scaling.
- No third-party funds.
- No discretionary trading strategy.
- No profit guarantee.
- Automatic disable on any oracle, schema, freshness, adapter, simulation, or landing anomaly.

For OPRS specifically, a safer progression is:

1. Execution design document only.
2. Local transaction-plan builder that cannot sign or submit.
3. Devnet/testnet rehearsal where the venue supports it.
4. Mainnet shadow mode that simulates but does not submit.
5. Capped mainnet pilot with a human-controlled signer.

## Explicitly Out Of Scope Until Separately Approved

- Production liquidator operation.
- Autonomous liquidation execution.
- Cross-venue arbitrage.
- Market making.
- Custody of customer or third-party funds.
- Private key storage in the repo, public dashboard, CI, or static Railway service.
- Use of a founder personal wallet as an unattended hot wallet.
- Jito/block-engine submission.
- Priority-fee bidding policy.
- Transaction retry loops.
- Dynamic capital allocation.
- MEV strategy.
- Any claim that OPRS improves profitability.

## Required Gates Before Discussion

The project is not ready for an execution pilot discussion until:

- Live read-only service runs stably.
- Seven-day read-only soak passes.
- Target protocol source authority is strong enough for replay-adjacent evidence.
- Dry-run-to-live equivalence tests exist.
- Private dashboard/API access controls exist.
- Alert destination is live.
- Secret handling is proven on the worker service.
- Commercial and legal boundaries are reviewed.

## Current Decision

Current status: execution pilot is future-scope only.

Next approved movement: continue read-only worker, alerting, custom domain, and commercial diagnostics packaging.
