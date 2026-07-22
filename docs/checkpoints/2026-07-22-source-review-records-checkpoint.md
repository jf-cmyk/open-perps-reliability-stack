# Checkpoint: Source Review Records

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Latest pushed commit before this slice: `18d25e4`
- Pre-existing/local work not owned by this slice:
  - `deliverables/Open Perps Reliability Stack - Solana Foundation Proposal.docx`
  - `docs/roadmap.md`
  - `research/`
  - `scripts/discover_drift_liquidation_history.py`

## Scope Lock

- Read-only: yes.
- Dry-run/replay: yes.
- No signing/custody/submission/capital: yes.
- Production execution: out of scope.

## What Changed Since Previous Checkpoint

- Added [Jupiter position authority outbound note](../jupiter-position-authority-outbound.md).
- Added [Source review records](../source-review-records.md).
- Added `schemas/datasets/source-review-record-v0.json`.
- Added source-review examples:
  - `examples/datasets/jupiter_position_authority_source_review_example.json`
  - `examples/datasets/drift_public_field_source_review_template.json`
- Added `scripts/validate_source_review_records.py`.
- Wired source-review validation into `scripts/run_mvp_checks.sh`.
- Linked source-review records from the docs index, MVP proof checklist, Jupiter confirmation doc, and Drift source-review checklist.

## Claim Boundary

Allowed:

- Jupiter authority record remains `blocked`.
- Drift source-review record remains a `pending` template.
- Source-review records can make future source decisions machine-readable.

Blocked:

- Any approved decode record without all approval gates true.
- Any forbidden claim flag set to true.
- Jupiter source authority promotion while `docs_linked_example_not_canonical`.
- Drift public-field expansion without a concrete review row and local validator pass.

## Validation Run

```bash
scripts/validate_source_review_records.py
scripts/run_mvp_checks.sh
cargo fmt --check
git diff --check
```

Results: all passed locally before commit.

## Next Queue

Can continue without access:

1. Add source-review IDs to future Drift/Jupiter local target outputs once real approved records exist.
2. Add negative source-review fixtures if source-review records become public package artifacts.
3. Continue package-validator hardening without expanding decode or pairing claims.

Needs access or founder confirmation:

1. Send the Jupiter confirmation ask through a real Jupiter contact/channel.
2. Decide whether to incorporate or commit the separate `research/` and Drift liquidation-history work.
3. Decide whether to refresh the modified Word proposal.
4. Final grant submission timing and ask confirmation.

## Fresh-Window Kickoff Prompt

```text
Continue development for the Blocksize Open Perps Reliability Stack.

Repo: /Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack
Checkpoint: docs/checkpoints/2026-07-22-source-review-records-checkpoint.md

Read the checkpoint first, then read docs/checkpoints/context-map.md only for the workstream being touched. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation
```

