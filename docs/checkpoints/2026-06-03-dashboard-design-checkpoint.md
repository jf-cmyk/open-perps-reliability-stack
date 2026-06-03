# Dashboard Design Checkpoint: 2026-06-03

This checkpoint is the resume point after replacing the static dashboard with the OpenPerp institutional fintech design direction.

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Latest implementation commit at checkpoint time: `8097395 Apply OpenPerp dashboard design`
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

OSS and commercial tracks are both in scope, but commercial execution/private telemetry remain separated from the grant-funded OSS v0.

## What Changed Since Previous Checkpoint

- Replaced `apps/dashboard/index.html` with the new `OpenPerp` institutional design:
  - white/charcoal/gray palette with sparse electric-purple usage
  - fixed institutional navigation
  - dashboard-first hero with safety posture
  - inline reliability control-plane visual
  - metric cards, feature cards, workflow steps, replay table, reason-code distribution, access boundaries, and OSS/commercial track cards
- Preserved the six synthetic Drift fixture cases and required DOM anchors:
  - `#metrics`
  - `#fixtureRows`
  - `#reasonBars`
  - `#features`
  - `#workflow`
  - `#replay`
  - `#access`
  - `#tracks`
- Removed old landing-style production wording from the supplied design brief:
  - no `Trading Live`
  - no `Deploy Node`
  - no `executing trades`
  - no MIT license claim
- Kept public safety markers visible:
  - `Read-only`
  - `Dry-run only`
  - `No live execution`
  - `ExecutionDisabledDryRun`
  - `AdapterVersionMismatch`
  - `Apache-2.0`

## Validation Commands And Results

Passed:

```bash
git diff --check
cargo run -p oprs-replay --example validate_fixtures
cargo run -p oprs-api-types --example validate_api_examples
cargo test
```

Local static server QA:

```bash
python3 -m http.server 8791 --bind 127.0.0.1
curl -sS http://127.0.0.1:8791/apps/dashboard/index.html
```

DOM/server checks passed:

- served HTML byte count: `38903`
- missing required markers: none
- forbidden production/license markers: none
- fixture definitions: `6`
- reason-code arrays: `6`
- required section IDs present

Pixel screenshot QA was attempted through Playwright. The bundled package was available, but the Playwright browser binary was not installed and system Chrome aborted under the current sandbox. Re-run Browser QA in a fresh window if visual inspection is required.

## Established Agent Threads

Use these established agent threads for coordination when needed:

- Coordinator / PM: `019e8a3b-5f29-7172-8138-bf5ff637a867`
- Architecture: `019e8a3b-7710-7212-b6f7-ca48d90f3217`
- Protocol: `019e8a3b-8eb0-7a11-969f-624b03d8d903`
- Data: `019e8a3b-a177-7220-993b-0448c092497b`
- Liquidator/SDK: `019e8a3b-b77c-7812-85b6-ba503200239d`
- Grant Positioning: `019e8a3b-cc8c-79a2-b231-5114cf5e56bd`
- Frontend implementation support: `019e8efb-edb6-7470-b089-a1dc01fb8f9b`

Frontend note: the frontend agent implemented the earlier technical-minimalist forest design, but the founder changed direction afterward. The local dashboard now reflects the newer OpenPerp institutional design.

## Recommended Next Development Queue

No access needed:

1. Add dataset/scrub-policy failure fixtures under a non-public test area.
2. Add scrub checks for blocked patterns:
   - RPC URLs with API keys
   - bearer tokens
   - local absolute paths
   - `.env` references
   - private keys/seed phrases
   - signer/wallet inventory metadata
   - capital limits and execution policy fields
3. Expand dry-run reason-code fixture coverage:
   - `NotLiquidatable`
   - `MissingPositionState`
   - `AdapterDecodeFailed`
   - `DataQualityLow`
   - `InsufficientLiquidity`
   - `NegativeExpectedEdge`
   - `TxBuildUnsupported`
   - `SimulationFailed`
   - `ComputeLimitRisk`
   - `ProtocolReject`
4. Add dry-run summary invariant validation:
   - counts reconcile
   - reason-code union matches summary
   - gate indexes are ordered and unique
   - rejected runs cannot have only pass gates
5. Expand service-boundary docs for future services:
   - ingest
   - indexer
   - oracle-risk
   - dry-runner
   - public-api
   - dashboard

Access or confirmation needed:

1. Real Drift read-only decode proof:
   - RPC/source access
   - official IDL/source provenance
   - public account snapshots
   - normalized adapter output
   - decode-health result
2. Grant submission:
   - shared Google Doc/proposal link
   - entity country
   - contact email
   - funding amount confirmation
   - explicit approval to submit

## New Window Kickoff Prompt

Use this prompt in a fresh Codex window:

```text
Continue development for the Blocksize Open Perps Reliability Stack.

Repo: /Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack
Checkpoint: docs/checkpoints/2026-06-03-dashboard-design-checkpoint.md

Read the checkpoint first, then continue the no-access development queue. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation

Use the established agent threads when helpful. Start with the next no-access item: dataset/scrub-policy failure fixtures and scrub checks.
```
