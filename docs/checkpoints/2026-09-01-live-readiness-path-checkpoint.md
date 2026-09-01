# 2026-09-01 Live Readiness Path Checkpoint

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Latest pushed commit before this slice: `265616a Validate Jupiter role map probe outputs`
- Local untracked items to ignore: none observed before this slice

## Scope Lock

- Read-only: yes
- Dry-run/replay: yes
- No signing/custody/submission/capital: yes
- OSS/commercial boundary changes: clarified only; no production execution or custody scope added

## What Changed Since Previous Checkpoint

- Added `docs/live-readiness-path.md` to define what "live" means before execution.
- Split live maturity into static proof pack, live read-only service, commercial diagnostics, and execution-readiness candidate.
- Added explicit gates for moving past MVP, launching a hosted read-only service, selling diagnostics, and later discussing an execution pilot.
- Linked the live-readiness path from the README, docs index, public proof-pack index, and dashboard.
- Added M7 live read-only service readiness to the roadmap.
- Extended service boundaries with a live read-only diagnostics service lane.
- Added local and hosted smoke markers for the new live-readiness page.
- Updated the proof-pack replay test count from 19 to 22.

## Validation Results

Commands run:

```bash
scripts/run_mvp_checks.sh
```

Result summary:

- Passed fixture replay validation.
- Passed public API example validation.
- Passed Rust tests, including 22 `oprs-replay` tests.
- Passed schema JSON validation and public package validators.
- Passed static proof-pack marker checks.
- Passed public artifact boundary checks.
- Confirmed local `HELIUS_RPC_URL` is present without printing it.

## Files/Areas Touched

- `docs/live-readiness-path.md`
- `docs/roadmap.md`
- `docs/service-boundaries.md`
- `README.md`
- `docs/README.md`
- `index.html`
- `apps/dashboard/index.html`
- `scripts/run_mvp_checks.sh`
- `scripts/run_hosted_smoke_checks.sh`
- `docs/checkpoints/README.md`
- `docs/checkpoints/context-map.md`

## Agent Guidance Used

- Architecture: keep static proof-pack service, read-only worker, commercial services, and execution surfaces separated.
- Protocol: keep Drift, Jupiter, and Phoenix claims independently gated; Jupiter lifecycle pairing and Phoenix replay remain blocked.
- Data: require source, slot, provider, freshness, checksum, and scrub metadata before live read-only service claims.
- Liquidator/SDK: keep execution disabled; dry-run/replay and diagnostics can advance before signer or transaction-surface work.
- Grant: position the hosted proof pack and future read-only diagnostics as public-good/revenue-adjacent infrastructure without claiming production trading.

## Current State

- Hosted static MVP is the current live surface.
- The project is ready to plan post-MVP alpha around repeatable read-only evidence.
- The safest revenue path before execution is read-only diagnostics, private dashboards, protocol proof-pack support, and integration support.
- Execution pilot remains blocked until a separate security, legal, signer, capital, monitoring, runbook, and founder approval package exists.

Known limitations:

- Drift historical liquidation reconstruction still needs a source-backed candidate.
- Jupiter lifecycle request/fulfillment pairing is still unverified.
- Phoenix account decode and replay are not claimed.
- No recurring hosted read-only worker exists yet.
- No commercial auth/billing service exists yet.

## Next Queue

Can continue without access:

1. Design the separate Railway read-only worker service plan and variable boundary.
2. Add a 7-day read-only soak checklist and runbook.
3. Continue Drift legacy pagination from cursor `2fhTXQqs9qnyX4mBrcKAuTLipxnWyfLG7kj7YRn3EpRNBQoRLignDCCVxCRx1ckfntdhYsSuC6deefgTLS9ghYKm`.
4. Design the Jupiter verified-pairing validator using the local lifecycle role-map output while keeping proof claims blocked.
5. Draft the commercial diagnostics offer around read-only outputs, private dashboards, and proof-pack support.
6. Keep Railway and GitHub Pages mirrors equivalent after every public proof-pack change.

Needs access or founder confirmation:

1. Confirm the first post-MVP live lane: read-only diagnostics API, private protocol dashboard, or protocol-specific proof-pack support.
2. Confirm whether Railway should host a separate read-only worker service in addition to the static proof pack.
3. Provide a production custom domain decision if one is desired.
4. Provide an alert destination later for the read-only service, such as email, Slack, PagerDuty, or another route.
5. Any execution pilot still needs a separate written approval package before implementation.

## Fresh-Window Kickoff Prompt

```text
Continue development for the Blocksize Open Perps Reliability Stack.

Repo: /Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack
Checkpoint: docs/checkpoints/2026-09-01-live-readiness-path-checkpoint.md

Read this checkpoint first, then read docs/checkpoints/context-map.md only for the workstream being touched. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

Start with the no-access queue: design the separate Railway read-only worker service plan, add a 7-day read-only soak checklist/runbook, continue Drift pagination from the current cursor, or design the Jupiter verified-pairing validator without claiming lifecycle proof.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation
```
