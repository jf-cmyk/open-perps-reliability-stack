# 2026-09-02 Soak Summary And Jupiter Validator Checkpoint

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Latest pushed commit before this slice: `989ceb8 Plan read-only worker launch path`
- Local untracked or modified items not owned by this slice: `research/solana-ecosystem/evidence.ndjson`, `research/solana-ecosystem/roadmap.md`, `research/solana-ecosystem/state.json`

## Scope Lock

- Read-only: yes
- Dry-run/replay: yes
- No signing/custody/submission/capital: yes
- OSS/commercial boundary changes: no execution scope added; consent explanations were clarified

## What Changed Since Previous Checkpoint

- Added `schemas/datasets/readonly-soak-summary-v0.json`.
- Added `examples/datasets/readonly_soak_summary_example.json`.
- Added `scripts/validate_readonly_soak_summary.py`.
- Added `docs/jupiter-verified-pairing-validator.md`.
- Linked soak summary and Jupiter validator artifacts from README, docs index, proof-pack index, dashboard, runbook, and worker plan.
- Added local and hosted smoke markers for the new artifacts.
- Updated `docs/live-readiness-path.md` with explanations for why the remaining access/confirmation items require founder consent.
- Updated `docs/proof-pack-changelog.md` with the new post-MVP promotion-gate artifacts.

## Validation Results

Commands run:

```bash
scripts/validate_readonly_soak_summary.py
git diff --check
python3 -m json.tool schemas/datasets/readonly-soak-summary-v0.json
python3 -m json.tool examples/datasets/readonly_soak_summary_example.json
PYTHONPYCACHEPREFIX=target/pycache python3 -m py_compile scripts/validate_readonly_soak_summary.py
scripts/run_mvp_checks.sh
```

Result summary:

- Dedicated soak summary validator passed.
- JSON and Python compile checks passed.
- `git diff --check` passed.
- `scripts/run_mvp_checks.sh` passed.
- Fixture replay validation passed.
- Public API examples passed.
- Rust tests passed, including 22 `oprs-replay` tests.
- Public package validators passed.
- Static proof-pack markers passed.

## Files/Areas Touched

- `schemas/datasets/readonly-soak-summary-v0.json`
- `examples/datasets/readonly_soak_summary_example.json`
- `scripts/validate_readonly_soak_summary.py`
- `docs/jupiter-verified-pairing-validator.md`
- `docs/live-readiness-path.md`
- `docs/read-only-soak-runbook.md`
- `docs/railway-readonly-worker-service-plan.md`
- `docs/proof-pack-changelog.md`
- `README.md`
- `docs/README.md`
- `index.html`
- `apps/dashboard/index.html`
- `scripts/run_mvp_checks.sh`
- `scripts/run_hosted_smoke_checks.sh`
- `docs/checkpoints/README.md`
- `docs/checkpoints/context-map.md`

## Agent Guidance Used

- Architecture: keep the read-only worker deterministic and separate from the static proof pack.
- Protocol: Jupiter pairing remains a validator target, not a proven lifecycle claim.
- Data: make the soak summary schema machine-checkable before launching recurring hosted runs.
- Liquidator/SDK: keep all execution and transaction surfaces explicitly false.
- Grant: show funders that post-MVP promotion gates are objective and conservative.

## Current State

- Static MVP remains the only hosted live service.
- The 7-day soak now has a schema, example, and validator.
- Jupiter has a written verified-pairing validator contract, but no verified pair is claimed.
- Remaining access items now include written consent rationale in `docs/live-readiness-path.md`.

Known limitations:

- No separate Railway worker service has been created.
- No 7-day soak has started.
- Drift historical liquidation reconstruction still needs a source-backed candidate.
- Jupiter verified request/fulfillment pairing remains blocked until before/after state evidence exists.
- Existing modified `research/solana-ecosystem/*` files were not reviewed or committed in this slice.

## Next Queue

Can continue without access:

1. Add a local-only worker command wrapper that can run bounded probes and emit soak-compatible summaries without creating a hosted service.
2. Add a synthetic Jupiter pairing-validator fixture and validator script that rejects missing before/after state and accepts only fully gated examples.
3. Continue Drift legacy pagination from cursor `2fhTXQqs9qnyX4mBrcKAuTLipxnWyfLG7kj7YRn3EpRNBQoRLignDCCVxCRx1ckfntdhYsSuC6deefgTLS9ghYKm`.
4. Review the modified Solana research files and decide whether they contain source-backed updates to commit.
5. Refine the commercial diagnostics brief into a founder-review package with package scope and exclusions.
6. Keep Railway and GitHub Pages mirrors equivalent after every public proof-pack change.

Needs access or founder confirmation:

1. Confirm whether to create a separate Railway worker service. This is needed because the service would hold read-only credentials, run scheduled jobs, create private outputs, and incur cloud usage.
2. Confirm the first commercial lane. This is needed because it controls customer-facing claims, pricing discovery, and OSS/commercial separation.
3. Provide alert destination later. This is needed because worker alerts can include protocol names, failure metadata, and private operational context.
4. Provide custom domain decision if desired. This is needed because it changes the public canonical URL, DNS ownership, and reviewer links.
5. Any execution pilot still needs separate written founder approval, security review, legal review, signer/capital policy, monitoring, and runbooks because it introduces signing, wallet, custody, transaction-submission, and capital risk.

## Fresh-Window Kickoff Prompt

```text
Continue development for the Blocksize Open Perps Reliability Stack.

Repo: /Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack
Checkpoint: docs/checkpoints/2026-09-02-soak-summary-jupiter-validator-checkpoint.md

Read this checkpoint first, then read docs/checkpoints/context-map.md only for the workstream being touched. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

Start with the no-access queue: add a local-only worker command wrapper, add a synthetic Jupiter pairing-validator fixture and validator script, continue Drift pagination from the current cursor, or review the modified Solana research files.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation, with the reason consent is required
```
