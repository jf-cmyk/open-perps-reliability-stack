# Hosted MVP Checkpoint: 2026-06-03

This checkpoint is the resume point after enabling GitHub Pages hosting for the proof-pack MVP.

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Latest implementation commit at checkpoint time: `bf3d111 Add hosted proof pack deployment`
- Hosted proof pack: `https://jf-cmyk.github.io/open-perps-reliability-stack/`
- Hosted dashboard: `https://jf-cmyk.github.io/open-perps-reliability-stack/apps/dashboard/`
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

## What Changed Since Previous Checkpoint

- Added GitHub Pages deployment workflow:
  - `.github/workflows/pages.yml`
  - `.nojekyll`
- Enabled GitHub Pages in workflow mode for the repository.
- Deployed the hosted proof-pack MVP.
- Updated `README.md` with hosted proof-pack and dashboard links.
- Updated the Solana Foundation proposal with a `Running MVP Before Submission` section.
- Added explicit Helius positioning:
  - Helius is optional and read-only.
  - RPC URL belongs in local `.env`.
  - RPC/API keys must never be committed or included in public datasets.
- Continued development with expanded dry-run reason-code validation:
  - `1ec9e5b Expand dry-run reason code coverage`
  - `17289b9 Add dataset scrub policy validation`

## Validation Commands And Results

Passed before deployment commit:

```bash
cargo run -p oprs-replay --example validate_fixtures
cargo run -p oprs-api-types --example validate_api_examples
git diff --check
```

Previous development slice also passed:

```bash
cargo test
```

GitHub Actions:

- CI passed for `bf3d111`.
- Pages deploy initially failed because Pages was not enabled yet.
- Pages was enabled with `build_type=workflow`.
- Pages deploy rerun passed.

Hosted smoke checks passed:

```bash
curl -sS -L https://jf-cmyk.github.io/open-perps-reliability-stack/
curl -sS -L https://jf-cmyk.github.io/open-perps-reliability-stack/apps/dashboard/
```

Expected markers found:

- `Open Perps Reliability Stack Proof Pack`
- `OpenPerp`
- `Read-only`
- `Dry-run only`
- `No live execution`
- `ExecutionDisabledDryRun`
- `AdapterVersionMismatch`

## Helius Setup Needed From Founder

Need only:

1. Helius HTTPS mainnet RPC URL, stored locally in `.env` as `HELIUS_RPC_URL=...`.
2. Confirmation whether the plan includes devnet as well as mainnet.
3. Hobby-plan rate-limit/credit notes if visible.
4. Permission to use read-only RPC calls such as account fetches and batch account reads.

Do not request or accept:

- private keys
- seed phrases
- wallet files
- bearer auth
- custody details
- capital or execution policy data

## Recommended Next Development Queue

No access needed:

1. Add dry-run summary and gate invariant validation.
2. Add a local MVP runner command/script for proof-pack validation.
3. Expand future service-boundary docs.
4. Keep adapting grant proposal language as the MVP hardens.

Access or confirmation needed:

1. Helius RPC URL for real Drift read-only decode proof.
2. Founder confirmation on MVP target:
   - hosted GitHub Pages proof-pack is enough, or
   - add a separate branded hosted demo.
3. Grant submission details and explicit approval.

## New Window Kickoff Prompt

Use this prompt in a fresh Codex window:

```text
Continue development for the Blocksize Open Perps Reliability Stack.

Repo: /Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack
Checkpoint: docs/checkpoints/2026-06-03-hosted-mvp-checkpoint.md

Read the checkpoint first. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

Hosted proof pack:
https://jf-cmyk.github.io/open-perps-reliability-stack/

Hosted dashboard:
https://jf-cmyk.github.io/open-perps-reliability-stack/apps/dashboard/

Continue with the next no-access item: dry-run summary and gate invariant validation. If Helius RPC is available in local `.env`, use it only for read-only decode proof work and never commit it.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation
```
