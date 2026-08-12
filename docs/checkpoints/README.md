# Checkpoints

Checkpoints are the project memory system for continuing work across fresh Codex windows without relying on automatic context compaction.

## Current Checkpoint

- [2026-08-11 Drift 266k research refresh checkpoint](2026-08-11-drift-266k-research-refresh-checkpoint.md)
- [2026-07-30 Drift 148k source-governance checkpoint](2026-07-30-drift-148k-source-governance-checkpoint.md)
- [2026-07-30 Phoenix Hawkeye validator plan checkpoint](2026-07-30-phoenix-hawkeye-validator-plan-checkpoint.md)
- [2026-07-30 dashboard Drift boundary link checkpoint](2026-07-30-dashboard-drift-boundary-link-checkpoint.md)
- [2026-07-29 Drift 146k source-governance checkpoint](2026-07-29-drift-146k-source-governance-checkpoint.md)
- [2026-07-29 Drift 145k source-governance checkpoint](2026-07-29-drift-145k-source-governance-checkpoint.md)
- [2026-07-29 Drift 140k source-governance checkpoint](2026-07-29-drift-140k-source-governance-checkpoint.md)
- [2026-07-28 Drift 115k grant refresh checkpoint](2026-07-28-drift-115k-grant-refresh-checkpoint.md)
- [2026-07-22 source review records checkpoint](2026-07-22-source-review-records-checkpoint.md)
- [2026-06-29 Jupiter position authority checkpoint](2026-06-29-jupiter-position-authority-checkpoint.md)
- [2026-06-29 Drift source review and Solana BD boundary checkpoint](2026-06-29-drift-source-review-solana-bd-checkpoint.md)
- [2026-06-16 Phoenix market telemetry checkpoint](2026-06-16-phoenix-market-telemetry-checkpoint.md)
- Previous: [2026-06-10 public package contract v0 checkpoint](2026-06-10-public-package-contract-v0-checkpoint.md)
- Previous: [2026-06-04 hosted monitoring checkpoint](2026-06-04-hosted-monitoring-checkpoint.md)
- Previous: [2026-06-04 Railway deployed MVP checkpoint](2026-06-04-railway-deployed-checkpoint.md)
- Previous: [2026-06-04 Railway deploy-ready MVP checkpoint](2026-06-04-railway-mvp-checkpoint.md)
- Previous: [2026-06-03 hosted MVP checkpoint](2026-06-03-hosted-mvp-checkpoint.md)
- Previous: [2026-06-03 dashboard design checkpoint](2026-06-03-dashboard-design-checkpoint.md)
- Previous: [2026-06-03 development checkpoint](2026-06-03-development-checkpoint.md)

## How To Use This Folder

At the start of a new window:

1. Read the current checkpoint.
2. Read [context-map.md](context-map.md) only for the workstream being touched.
3. Run `git status --short`.
4. Continue the next no-access task unless the checkpoint marks it as access/confirmation-blocked.

At the end of a completed work slice:

1. Commit and push the code/docs change.
2. Add a new checkpoint if the completed slice changes project direction, architecture, validation contracts, agent state, grant state, or the next-task queue.
3. Keep the checkpoint short enough to read first, but concrete enough that a fresh window can resume without reading the whole thread.
4. Link the new checkpoint from this README and update `docs/README.md` if it becomes the current checkpoint.

## Checkpoint Triggers

Create a checkpoint when any of these happen:

- A meaningful commit series lands.
- The next task queue changes materially.
- A founder decision changes scope, grant positioning, protocol priority, or access.
- A new agent thread is created or an existing agent returns decisive guidance.
- Real external access is introduced, such as RPC, GitHub issue changes, grant submission, or hosted demo work.
- Before intentionally moving to a fresh Codex window.

Do not create a checkpoint for tiny edits that are fully captured by a commit message and do not change the resume path.

## Naming

Use:

```text
YYYY-MM-DD-short-topic-checkpoint.md
```

Examples:

```text
2026-06-03-development-checkpoint.md
2026-06-04-scrub-validation-checkpoint.md
2026-06-05-drift-decode-proof-checkpoint.md
```

## Required Sections

Use [template.md](template.md) for new checkpoints.

Minimum fields:

- repo path and branch
- latest pushed commit
- scope lock
- what changed since previous checkpoint
- validation commands and results
- active next queue
- access/confirmation blockers
- fresh-window kickoff prompt
