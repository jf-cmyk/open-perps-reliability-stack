# Checkpoint: Jupiter Position Authority Confirmation

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Latest pushed commit before this slice: `f7c8330`
- Local residue to ignore unless explicitly refreshed: `deliverables/Open Perps Reliability Stack - Solana Foundation Proposal.docx`

## Scope Lock

- Read-only: yes.
- Dry-run/replay: yes.
- No signing/custody/submission/capital: yes.
- Production execution: out of scope.

## What Changed Since Previous Checkpoint

- Added [Jupiter position authority confirmation](../jupiter-position-authority-confirmation.md).
- Made the Jupiter ask narrow and binary around mainnet program `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu`.
- Split the unblock criteria into:
  - decode unlock: canonical source/IDL, discriminators, account sizes, offsets, enum encodings, PDA seeds, bump/counter encoding
  - pairing unlock: source-backed lifecycle/account-role map, shared `PositionRequest`, corresponding `Position`, request closure/execution semantics, TP/SL behavior, token-account roles, and public mainnet signature pairs for regression fixtures
- Linked the confirmation package from Jupiter provenance, Jupiter source-authority audit, protocol targets, context map, docs index, and the public Jupiter authority-gap README.
- Updated the Jupiter authority-gap public report and manifest checksum to reflect the sharper source requirements.

## Agent Guidance Used

- Protocol/Jupiter explorer: keep the ask focused on canonical source authority for `PositionRequest` and `Position`; do not promote from candidate lifecycle evidence to verified pairing until Jupiter confirms source/IDL and account-role semantics.

## Claim Boundary

Allowed:

- Jupiter program, custody, oracle target discovery.
- Public transaction-history sampling.
- `candidate_pair_unverified` lifecycle evidence.
- Contacting Jupiter for source-authority confirmation.

Blocked:

- Jupiter binary account decode.
- Decoded `Position` or `PositionRequest` support.
- Verified request/fulfillment pairing.
- Keeper execution verification.
- Historical Jupiter liquidation replay.
- Jupiter adapter readiness beyond read-only target discovery and unverified lifecycle candidates.

## Validation Run

```bash
scripts/validate_public_jupiter_authority_gap.py
scripts/run_mvp_checks.sh
git diff --check
```

Results: all passed locally before commit.

## Next Queue

Can continue without access:

1. Prepare a founder-ready outbound Jupiter confirmation note from the contact template.
2. Keep Jupiter decode and verified pairing blocked in docs and fixtures.
3. Continue no-access hardening around public-package validators or source-review metadata.

Needs access or founder confirmation:

1. Send the Jupiter confirmation ask through a Jupiter contact, issue, Discord, Telegram, or email route.
2. Decide whether to refresh the modified Word proposal.
3. Final grant submission timing and ask confirmation.

## Fresh-Window Kickoff Prompt

```text
Continue development for the Blocksize Open Perps Reliability Stack.

Repo: /Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack
Checkpoint: docs/checkpoints/2026-06-29-jupiter-position-authority-checkpoint.md

Read the checkpoint first, then read docs/checkpoints/context-map.md only for the workstream being touched. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation
```

