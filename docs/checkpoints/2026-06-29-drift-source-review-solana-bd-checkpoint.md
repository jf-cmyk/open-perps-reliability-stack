# Checkpoint: Drift Source Review And Solana BD Boundary

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Latest pushed commit before this slice: `e00af4e`
- Local residue to ignore unless explicitly refreshed: `deliverables/Open Perps Reliability Stack - Solana Foundation Proposal.docx`

## Scope Lock

- Read-only: yes.
- Dry-run/replay: yes.
- No signing/custody/submission/capital: yes.
- Production execution: out of scope.

## What Changed Since Previous Checkpoint

- Added [Drift public field source review checklist](../drift-public-field-source-review-checklist.md).
- Made the checklist the required precondition before adding new Drift public-field offsets.
- Linked the checklist from Drift provenance, Helius proof plan, MVP proof checklist, docs index, and context map.
- Folded latest Solana Expert findings into BD/grant context:
  - MoneyGram joined Solana Developer Platform and became an active validator.
  - Solana's bare-metal validator article sharpened the 100M CU / XDP / skip-rate / block-propagation readiness lane.
- Updated service and OSS/commercial boundaries so validator readiness, private validator telemetry, XDP/kernel tuning, skip-rate optimization, block-propagation optimization, priority-fee strategy, and block-engine strategy remain outside the grant MVP.

## Agent Guidance Used

- Solana Expert: MoneyGram/SDP and bare-metal validator-readiness findings are useful BD context, not MVP claims.
- Architecture/Data/Protocol/Liquidator/Grant threads: preserve source-authority gates, avoid broad Drift expansion, keep Jupiter verified pairing blocked, and continue emphasizing validation discipline.
- Drift checklist explorer: require explicit source, offset derivation, type/encoding, expected-value source, semantic-label source, public-safety class, local validator pass, and no-user-state/no-market-economics/no-replay flags before any new field.
- Solana BD explorer: update BD/grant docs and service boundaries, but do not claim MoneyGram, validator, WSOP, SDP, payment, or infrastructure monitoring as current OPRS functionality.

## Claim Boundary

Allowed:

- Source-backed ecosystem context about Solana payments, institutional infrastructure, validator readiness, and execution-environment reliability.
- Future commercial/partner diligence framing around payment/settlement observability or validator readiness.
- Read-only Drift public identity, metadata, oracle identity, and guardrail fields that pass the new checklist and local validator.

Blocked:

- OPRS monitoring of MoneyGram, SDP partners, WSOP, MoonPay, validators, skip rate, block propagation, XDP, payment flows, settlements, or private validator telemetry today.
- Partnerships with Solana Foundation, MoneyGram, WSOP, MoonPay, SDP partners, validators, or infrastructure providers.
- Validator operations product, routing, hardware certification, XDP/kernel tuning, priority-fee strategy, block-engine strategy, or 100M CU certification in the grant MVP.
- Additional Drift offsets without checklist review and `scripts/validate_drift_readonly_state.py`.
- Jupiter binary decode or verified request/fulfillment pairing without canonical source authority.

## Validation To Run

```bash
scripts/run_mvp_checks.sh
cargo fmt --check
git diff --check
```

After deploy:

```bash
scripts/run_hosted_smoke_checks.sh https://refreshing-art-production-86de.up.railway.app
scripts/run_hosted_smoke_checks.sh https://jf-cmyk.github.io/open-perps-reliability-stack
```

## Next Queue

Can continue without access:

1. Run validation, commit, push, deploy Railway, and smoke-check Railway plus GitHub Pages.
2. Add no new Drift public fields until checklist rows exist for each field and the local target validator passes.
3. Continue source-backed Solana BD notes only where they remain context and do not create MVP claims.
4. Keep Railway and GitHub Pages mirrors equivalent.

Needs access or founder confirmation:

1. Jupiter canonical `PositionRequest` / `Position` source-authority confirmation.
2. Whether to refresh or regenerate the modified Word proposal.
3. Final grant submission timing and ask confirmation.

## Fresh-Window Kickoff Prompt

```text
Continue development for the Blocksize Open Perps Reliability Stack.

Repo: /Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack
Checkpoint: docs/checkpoints/2026-06-29-drift-source-review-solana-bd-checkpoint.md

Read the checkpoint first, then read docs/checkpoints/context-map.md only for the workstream being touched. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation
```

