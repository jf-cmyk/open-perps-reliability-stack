# Development Checkpoint: YYYY-MM-DD

## Repo

- Local path:
- GitHub:
- Branch:
- Latest pushed commit:
- Local untracked items to ignore:

## Scope Lock

- Read-only:
- Dry-run/replay:
- No signing/custody/submission/capital:
- OSS/commercial boundary changes:

## What Changed Since Previous Checkpoint

- 

## Validation Results

Commands run:

```bash
cargo fmt
cargo check
cargo test
cargo run -p oprs-replay --example validate_fixtures
cargo run -p oprs-api-types --example validate_api_examples
git diff --check
```

Result summary:

- 

## Files/Areas Touched

- 

## Agent Guidance Used

- Architecture:
- Protocol:
- Data:
- Liquidator/SDK:
- Grant:

## Current State

- Latest built artifacts:
- Known limitations:
- Known local residue:

## Next Queue

Can continue without access:

1. 

Needs access or founder confirmation:

1. 

## Fresh-Window Kickoff Prompt

```text
Continue development for the Blocksize Open Perps Reliability Stack.

Repo: /Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack
Checkpoint: docs/checkpoints/<this-file>.md

Read the checkpoint first, then read docs/checkpoints/context-map.md only for the workstream being touched. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation
```
