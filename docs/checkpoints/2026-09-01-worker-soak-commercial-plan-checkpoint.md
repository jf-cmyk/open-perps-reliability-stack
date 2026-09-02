# 2026-09-01 Worker Soak Commercial Plan Checkpoint

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Latest pushed commit before this slice: `f7c3a37 Document live readiness path`
- Local untracked items to ignore: none observed before this slice

## Scope Lock

- Read-only: yes
- Dry-run/replay: yes
- No signing/custody/submission/capital: yes
- OSS/commercial boundary changes: clarified pre-execution commercial diagnostics only; no execution scope added

## What Changed Since Previous Checkpoint

- Added `docs/railway-readonly-worker-service-plan.md`.
- Added `docs/read-only-soak-runbook.md`.
- Added `docs/commercial-diagnostics-brief.md`.
- Linked the new docs from README, docs index, live-readiness path, roadmap, deployment docs, service boundaries, proof-pack index, and dashboard.
- Added smoke markers for all three docs.
- Clarified that Railway static proof pack remains canonical and secret-free while any future read-only worker must be a separate service.
- Set the initial revenue motion as protocol proof-pack support, followed by read-only diagnostics after the 7-day soak proves useful output.

## Validation Results

Commands run:

```bash
git diff --check
scripts/run_mvp_checks.sh
```

Result summary:

- `git diff --check` passed.
- `scripts/run_mvp_checks.sh` passed.
- Fixture replay validation passed.
- Public API examples passed.
- Rust tests passed, including 22 `oprs-replay` tests.
- Public package validators passed.
- Static proof-pack markers passed for worker plan, soak runbook, and diagnostics brief.
- Public artifact boundary checks passed.

## Files/Areas Touched

- `docs/railway-readonly-worker-service-plan.md`
- `docs/read-only-soak-runbook.md`
- `docs/commercial-diagnostics-brief.md`
- `docs/live-readiness-path.md`
- `docs/roadmap.md`
- `docs/deployment-railway.md`
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

- Architecture: future read-only worker is a separate service with separate variables and monitoring.
- Protocol: Drift/Jupiter/Phoenix claims remain independently gated; source-backed evidence comes before replay or lifecycle claims.
- Data: live worker outputs require source, slot, provider, freshness, checksum, and scrub metadata.
- Liquidator/SDK: execution surfaces remain forbidden; diagnostics and dry-run evidence can advance first.
- Grant: commercial language stays tied to proof-pack support and read-only diagnostics, not trading or profit claims.

## Current State

- Static MVP is live and canonical on Railway.
- The repo now has a concrete plan for the next hosted read-only service.
- The repo now has a 7-day operational soak runbook.
- The repo now has a pre-execution commercial diagnostics brief.
- No worker service has been created yet.
- No Railway worker variables have been added yet.
- No execution or signer scope exists.

Known limitations:

- Drift historical liquidation reconstruction still needs a source-backed candidate.
- Jupiter verified request/fulfillment pairing remains blocked until before/after state evidence exists.
- Phoenix account decode and replay are not claimed.
- Commercial diagnostics pricing and first buyer profile are not validated.

## Next Queue

Can continue without access:

1. Design the Jupiter verified-pairing validator contract from the lifecycle role-map probe.
2. Continue Drift legacy pagination from cursor `2fhTXQqs9qnyX4mBrcKAuTLipxnWyfLG7kj7YRn3EpRNBQoRLignDCCVxCRx1ckfntdhYsSuC6deefgTLS9ghYKm`.
3. Add the read-only worker command wrapper in dry-run/local mode before any hosted service creation.
4. Add a soak-summary schema/example so the 7-day runbook has machine-checkable output.
5. Refine the commercial diagnostics brief into a founder-review package with package scope and exclusions.
6. Keep Railway and GitHub Pages mirrors equivalent after every public proof-pack change.

Needs access or founder confirmation:

1. Confirm whether to create a separate Railway worker service.
2. Confirm the first commercial lane: protocol proof-pack support, private protocol dashboard, or read-only diagnostics API.
3. Provide alert destination later for worker failures.
4. Provide custom domain decision if desired.
5. Any execution pilot still needs separate written founder approval, security review, legal review, signer/capital policy, monitoring, and runbooks.

## Fresh-Window Kickoff Prompt

```text
Continue development for the Blocksize Open Perps Reliability Stack.

Repo: /Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack
Checkpoint: docs/checkpoints/2026-09-01-worker-soak-commercial-plan-checkpoint.md

Read this checkpoint first, then read docs/checkpoints/context-map.md only for the workstream being touched. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

Start with the no-access queue: design the Jupiter verified-pairing validator contract, continue Drift pagination from the current cursor, add a local-only worker command wrapper, or add a soak-summary schema/example.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation
```
