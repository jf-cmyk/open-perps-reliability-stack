# Drift Read-Only State Checkpoint: 2026-06-05

This checkpoint is the resume point after adding the second Helius-backed, read-only Drift proof command.

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Railway proof pack: `https://refreshing-art-production-86de.up.railway.app/`
- Railway dashboard: `https://refreshing-art-production-86de.up.railway.app/apps/dashboard/`
- GitHub Pages fallback:
  - `https://jf-cmyk.github.io/open-perps-reliability-stack/`
  - `https://jf-cmyk.github.io/open-perps-reliability-stack/apps/dashboard/`
- URL policy: Railway is canonical for grant reviewers; GitHub Pages remains an equivalent fallback mirror.
- Local untracked item to ignore: `deliverables/~$en Perps Reliability Stack - Solana Foundation Proposal.docx`

## Scope Lock

Current execution scope remains strict:

- Read-only only.
- Dry-run/replay only.
- No production trading.
- No custody.
- No private-key handling.
- No live transaction submission.
- No capital deployment.
- No signer, wallet, keypair, block-engine submission, or execution-router surface in OSS v0.

## What Changed

- Added `scripts/discover_drift_readonly_state.py`.
- The command loads `HELIUS_RPC_URL` from local `.env`, never prints it, and writes scrubbed live output under `target/oprs-drift-readonly-state/latest.json`.
- It derives Drift PDAs locally from public SDK seed rules:
  - `drift_state`
  - `perp_market` plus little-endian market index
  - `spot_market` plus little-endian market index
- It probes public metadata for:
  - Drift state account
  - SOL/BTC/ETH perp market accounts
  - USDC/SOL spot market accounts
  - deduplicated oracle accounts used by those markets
- Added `examples/datasets/drift_readonly_state_example.json` as a scrubbed public example.
- Updated README, docs index, protocol targets, Helius proof plan, MVP proof checklist, grant docs, and decision log.
- Updated local MVP checks to validate the new example and compile the new proof script.
- Updated hosted smoke checks to fetch the new public example and include it in public secret-marker checks.

## Validation

Passed locally:

```bash
scripts/run_mvp_checks.sh
git diff --check
scripts/discover_drift_readonly_state.py --out target/oprs-drift-readonly-state/latest.json
```

The live Drift proof output confirmed metadata access without signer or wallet access. It stayed under `target/` and was not committed.

## Helius Current Status

Local Helius access is working for read-only target discovery. Current confirmed proof level:

- Drift program metadata: `target_discovered`
- Drift state account metadata: `target_discovered`
- Selected Drift perp market metadata: `target_discovered`
- Selected Drift spot market metadata: `target_discovered`
- Selected Drift oracle account metadata: `target_discovered`

Not yet claimed:

- Drift binary account decoding
- Drift historical liquidation reconstruction
- Drift user/pre-state/transaction-history replay
- Jupiter Perps pool/custody/oracle account proof

## Recommended Next Development Queue

Can continue without access:

1. Pin Drift decoder/IDL provenance and add a public-field binary decode-safe snapshot mode.
2. Resolve Jupiter Perps public pool/custody/oracle targets from official sources.
3. Add a `decoded_snapshot` example only after the binary decode path is verified and scrubbed.
4. Keep dashboard/proof-pack wording aligned with metadata proof, not historical replay.

Needs access or founder confirmation:

1. Branded domain/DNS and Railway service naming decision.
2. Final grant submission approval/details.

## New Window Kickoff Prompt

Use this prompt in a fresh Codex window:

```text
Continue development for the Blocksize Open Perps Reliability Stack.

Repo: /Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack
Checkpoint: docs/checkpoints/2026-06-05-drift-readonly-state-checkpoint.md

Read the checkpoint first. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

Railway is the canonical reviewer URL:
https://refreshing-art-production-86de.up.railway.app/

GitHub Pages is the equivalent fallback:
https://jf-cmyk.github.io/open-perps-reliability-stack/

The static Railway service should not receive HELIUS_RPC_URL. Helius is local or future worker-only.

Current proof level: Drift program/state/selected market/selected oracle metadata discovery works through local Helius and writes scrubbed live output under target/. Binary account decoding and historical liquidation replay are not yet claimed.

Run `scripts/run_mvp_checks.sh` before committing. For hosted checks, run both:
scripts/run_hosted_smoke_checks.sh https://refreshing-art-production-86de.up.railway.app
scripts/run_hosted_smoke_checks.sh https://jf-cmyk.github.io/open-perps-reliability-stack

Continue with Drift decoder/IDL provenance and public-field binary decode proof, then Jupiter Perps public target resolution.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation
```
