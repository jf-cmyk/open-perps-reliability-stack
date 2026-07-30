# Development Checkpoint: 2026-07-30 Phoenix Hawkeye Validator Plan

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Latest pushed commit before this slice: `23eff35`
- Local untracked items to ignore: none expected after commit

## Scope Lock

- Read-only: yes
- Dry-run/replay: dry-run planning only
- No signing/asset-control/submission/funded execution: yes
- OSS/commercial boundary changes: none

## What Changed Since Previous Checkpoint

- Added a Phoenix/Rise Hawkeye validator-plan contract as the next no-access development step after the Drift 147k boundary link.
- Added `schemas/datasets/phoenix-hawkeye-validator-plan-v0.json` for the local plan artifact.
- Added `examples/datasets/phoenix_hawkeye_validator_plan_example.json` with pinned source constants, planned Hawkeye view coverage, negative cases, scrub flags, and readiness gates.
- Added `scripts/validate_phoenix_hawkeye_validator_plan.py` to enforce the schema, source constants, blocked beta-program confusion, scrub policy, and no premature replay/execution claims.
- Added `docs/phoenix-hawkeye-validator-plan.md` and linked it from `docs/README.md`, the root proof-pack index, and the dashboard.
- Updated local MVP and hosted smoke checks so GitHub Pages/Railway must expose the Phoenix/Hawkeye validator-plan link and example artifact.

## Validation Results

Commands run before checkpoint creation:

```bash
python3 -m json.tool schemas/datasets/phoenix-hawkeye-validator-plan-v0.json
python3 -m json.tool examples/datasets/phoenix_hawkeye_validator_plan_example.json
scripts/validate_phoenix_hawkeye_validator_plan.py
```

Result summary:

- Schema parses cleanly.
- Example artifact parses cleanly.
- Phoenix/Hawkeye validator-plan script passes.
- Full MVP, CI, Pages, Railway, and hosted smoke results are pending for the commit that lands this checkpoint.

## Files/Areas Touched

- `index.html`
- `apps/dashboard/index.html`
- `docs/README.md`
- `docs/phoenix-hawkeye-validator-plan.md`
- `docs/checkpoints/README.md`
- `docs/checkpoints/2026-07-30-phoenix-hawkeye-validator-plan-checkpoint.md`
- `examples/datasets/phoenix_hawkeye_validator_plan_example.json`
- `schemas/datasets/phoenix-hawkeye-validator-plan-v0.json`
- `scripts/run_mvp_checks.sh`
- `scripts/run_hosted_smoke_checks.sh`
- `scripts/validate_phoenix_hawkeye_validator_plan.py`

## Agent Guidance Used

- Protocol: treat Phoenix/Hawkeye as source-anchored validator planning, not account-level decode.
- Data: only publish scrubbed fixture-shape contracts and negative readiness gates.
- Liquidator/SDK: no instruction building, signing, submission, asset control, or funded execution.
- Grant: keep Phoenix/Rise as a proof-of-work expansion while avoiding replay or live-market correctness claims until implemented.

## Current State

- Phoenix/Hawkeye has a public validator-plan artifact and local validator.
- It does not claim account-level decode, exact oracle input identity, liquidation replay, instruction builder readiness, or execution readiness.
- Drift scan remains at the last integrated 147,000 finalized transactions unless the background research state has advanced after this checkpoint.
- Railway deployment may still be serving the prior successful image until a new Railway deployment completes and hosted smoke checks pass.

## Next Queue

Can continue without access:

1. Run full local MVP checks and `git diff --check`.
2. Commit, push, watch GitHub CI/Pages, and rerun hosted smoke checks.
3. Retry/verify Railway deployment and confirm Railway serves the same Phoenix/Hawkeye dashboard links as GitHub Pages.
4. Add a dashboard/proof-pack card for Phoenix exact-input/oracle identity gates if the current Phoenix/Hawkeye link needs more reviewer visibility.
5. Resume Drift legacy liquidation scan from the latest checked research cursor.

Needs access or founder confirmation:

1. Jupiter canonical current IDL/source confirmation from the protocol team or authoritative repository.
2. Approval to send external Jupiter/Phoenix/Termina outreach.
3. Approval to submit the Solana Foundation grant application.
4. Any scope expansion beyond read-only and dry-run.

## Fresh-Window Kickoff Prompt

```text
Continue development for the Blocksize Open Perps Reliability Stack.

Repo: /Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack
Checkpoint: docs/checkpoints/2026-07-30-phoenix-hawkeye-validator-plan-checkpoint.md

Read the checkpoint first, then read docs/checkpoints/context-map.md only for the workstream being touched. Scope remains read-only and dry-run only: no production execution, no signing, no asset control, no live transaction submission, and no funded execution.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation
```
