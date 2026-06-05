# Jupiter Perps Target Discovery Checkpoint: 2026-06-05

This checkpoint is the resume point after adding the first Jupiter Perps read-only target discovery command.

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Railway proof pack: `https://refreshing-art-production-86de.up.railway.app/`
- Railway dashboard: `https://refreshing-art-production-86de.up.railway.app/apps/dashboard/`
- GitHub Pages fallback:
  - `https://jf-cmyk.github.io/open-perps-reliability-stack/`
  - `https://jf-cmyk.github.io/open-perps-reliability-stack/apps/dashboard/`
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

- Added `scripts/discover_jupiter_perps_readonly_targets.py`.
- The command loads `HELIUS_RPC_URL` from local `.env`, never prints it, and writes scrubbed live output under `target/oprs-jupiter-perps-readonly-targets/latest.json`.
- It resolves Jupiter Perps targets from current official Jupiter docs:
  - Jupiter Perpetuals program account.
  - SOL/ETH/BTC/USDC/USDT custody accounts.
  - SOL/ETH/BTC/USDC/USDT documented oracle accounts.
- Added `examples/datasets/jupiter_perps_readonly_targets_example.json`.
- Updated README, docs index, Helius proof plan, protocol targets, MVP proof checklist, grant docs, local MVP checks, and hosted smoke checks.

## Current Proof Level

Confirmed:

- Drift program metadata: `target_discovered`
- Drift state account metadata: `target_discovered`
- Selected Drift perp/spot market metadata: `target_discovered`
- Selected Drift oracle metadata: `target_discovered`
- Jupiter Perps program metadata: `target_discovered`
- Jupiter Perps documented custody metadata: `target_discovered`
- Jupiter Perps documented oracle metadata: `target_discovered`

Not yet claimed:

- Drift binary account decoding.
- Drift historical liquidation reconstruction.
- Jupiter Perps binary account decoding.
- Jupiter Perps request/fulfillment lifecycle reconstruction.
- Jupiter Perps canonical IDL/source revision pin.
- Production execution, signing, custody, or capital deployment.

## Solana Expert Agent Context

The Solana Expert agent confirmed the distinction that drives the next work:

- Drift is stronger for source-pinned decoder provenance today because the public Drift repo and IDL revision are pinned.
- Jupiter official docs are strong enough for program/custody/oracle target discovery.
- Jupiter should not claim binary decode until a canonical IDL/source revision is captured and hashed.
- Jupiter request/fulfillment proof should use public transaction history only and exclude `/order`, `/execute`, `/build`, `/submit`, API-key/auth paths, keeper operation, RFQ/order routing, signing, and wallet access.

## Recommended Next Development Queue

Can continue without access:

1. Run the live Jupiter Perps target discovery command and inspect scrubbed output under `target/`.
2. Pin Jupiter Perps canonical IDL/source provenance if an authoritative source can be confirmed.
3. Add a Drift binary decode-safe snapshot mode for account discriminator, account type, and public market fields only.
4. Add Jupiter request/fulfillment transaction-history proof for public signatures only after target metadata is stable.

Needs access or founder confirmation:

1. Branded domain/DNS and Railway service naming decision.
2. Final grant submission approval/details.

## New Window Kickoff Prompt

Use this prompt in a fresh Codex window:

```text
Continue development for the Blocksize Open Perps Reliability Stack.

Repo: /Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack
Checkpoint: docs/checkpoints/2026-06-05-jupiter-perps-targets-checkpoint.md

Read the checkpoint first. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

Railway is the canonical reviewer URL:
https://refreshing-art-production-86de.up.railway.app/

GitHub Pages is the equivalent fallback:
https://jf-cmyk.github.io/open-perps-reliability-stack/

The static Railway service should not receive HELIUS_RPC_URL. Helius is local or future worker-only.

Current proof level: Drift program/state/selected market/selected oracle metadata discovery works, Drift decoder provenance is pinned, and Jupiter Perps program/custody/oracle metadata target discovery is implemented. Binary account decoding, historical liquidation replay, and Jupiter request/fulfillment reconstruction are not yet claimed.

Run `scripts/run_mvp_checks.sh` before committing. For hosted checks, run both:
scripts/run_hosted_smoke_checks.sh https://refreshing-art-production-86de.up.railway.app
scripts/run_hosted_smoke_checks.sh https://jf-cmyk.github.io/open-perps-reliability-stack

Continue with live Jupiter target validation, Jupiter canonical IDL/source provenance, or Drift public-field binary decode proof.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation
```
