# Development Checkpoint: 2026-06-03

This checkpoint is the resume point for continuing Open Perps Reliability Stack development in a fresh Codex window.

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Latest pushed commit at checkpoint time: `7cc1ed3 Add development checkpoint`
- Local untracked item to ignore: `deliverables/~$en Perps Reliability Stack - Solana Foundation Proposal.docx`

## Scope Lock

Current execution scope is strict:

- Read-only only.
- Dry-run/replay only.
- No production trading.
- No custody.
- No private-key handling.
- No live transaction submission.
- No capital deployment.
- No signer, wallet, keypair, block-engine submission, or execution-router surface in OSS v0.

OSS and commercial tracks are both in scope, but commercial execution/private telemetry remain separated from the grant-funded OSS v0.

## Latest Commits

```text
7cc1ed3 Add development checkpoint
eb9b910 Add reviewer proof pack index
dc15793 Validate fixture content checksums
0ebdf85 Validate public API examples
7e2a6b7 Use typed JSON fixture validation
2e94e9e Expand fixture coverage and API examples
80b7ddb Add deterministic fixture validation
bd9b31b Add grant proposal doc and dashboard fixtures
71939b0 Add Solana grant application package
30bef6d Add read-only adapter and dry-run contracts
f180ac2 Add architecture v0 and Rust workspace scaffold
```

## What Is Built

- Rust workspace with core crates:
  - `oprs-core`
  - `oprs-adapter`
  - `oprs-risk`
  - `oprs-data`
  - `oprs-replay`
  - `oprs-dry-run`
  - `oprs-api-types`
- Read-only fixture-backed Drift adapter spike:
  - `adapters/drift-readonly`
- Pyth-aware risk primitives and tests.
- Dry-run/replay contracts and typed fixture validation.
- Six synthetic Drift fixture cases:
  - `drift_synthetic_margin_001`
  - `drift_synthetic_stale_oracle_001`
  - `drift_synthetic_wide_confidence_001`
  - `drift_synthetic_missing_oracle_001`
  - `drift_synthetic_oracle_divergence_001`
  - `drift_synthetic_adapter_version_mismatch_001`
- Fixture catalog:
  - `datasets/sample/fixture_catalog.json`
- API response examples:
  - `examples/api/*.json`
- API example validator:
  - `cargo run -p oprs-api-types --example validate_api_examples`
- Fixture validator with SHA-256 content checksum checks:
  - `cargo run -p oprs-replay --example validate_fixtures`
- Static dashboard:
  - `apps/dashboard/index.html`
- Reviewer proof-pack index:
  - `index.html`
- Solana Foundation grant docs:
  - `docs/solana-foundation-application-fields.md`
  - `docs/solana-foundation-developer-tooling-proposal.md`
  - `deliverables/Open Perps Reliability Stack - Solana Foundation Proposal.docx`

## Validation Commands

Run these before committing any future development wave:

```bash
cargo fmt
cargo check
cargo test
cargo run -p oprs-replay --example validate_fixtures
cargo run -p oprs-api-types --example validate_api_examples
git diff --check
```

For frontend proof-pack/dashboard changes, also run a local static server and Browser QA:

```bash
python3 -m http.server 8791 --bind 127.0.0.1
```

Then inspect:

- `http://127.0.0.1:8791/index.html`
- `http://127.0.0.1:8791/apps/dashboard/index.html`

Stop the server after QA.

## Established Agent Threads

Use these established agent threads for coordination when needed:

- Coordinator / PM: `019e8a3b-5f29-7172-8138-bf5ff637a867`
- Architecture: `019e8a3b-7710-7212-b6f7-ca48d90f3217`
- Protocol: `019e8a3b-8eb0-7a11-969f-624b03d8d903`
- Data: `019e8a3b-a177-7220-993b-0448c092497b`
- Liquidator/SDK: `019e8a3b-b77c-7812-85b6-ba503200239d`
- Grant Positioning: `019e8a3b-cc8c-79a2-b231-5114cf5e56bd`

Recent agent guidance:

- Architecture prioritized API/schema validation, dataset validation, proof-pack index, then service-boundary docs.
- Data prioritized manifest/schema validation, deterministic checksums, scrub-policy tests, DQ gate hardening, and invalid failure fixtures.
- Liquidator/SDK prioritized stronger reason-code coverage, gate-result validation, dry-run summary invariants, and tx-plan guardrails.
- Protocol prioritized Drift fixture shape fidelity: metadata, IDL/source basis, account-shape caveats, market/oracle/position/margin fixture coverage.
- Grant prioritized a reviewer-ready read-only proof pack and warned not to overclaim current synthetic fixtures as real Drift decode proof.

## GitHub Issues

Open issue at checkpoint time:

- `#3 M0: Confirm scope lock and founder decision queue`

Keep this open until founder decisions are confirmed.

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
Checkpoint: docs/checkpoints/2026-06-03-development-checkpoint.md

Read the checkpoint first, then continue the no-access development queue. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation

Use the established agent threads when helpful:
- Architecture: 019e8a3b-7710-7212-b6f7-ca48d90f3217
- Protocol: 019e8a3b-8eb0-7a11-969f-624b03d8d903
- Data: 019e8a3b-a177-7220-993b-0448c092497b
- Liquidator/SDK: 019e8a3b-b77c-7812-85b6-ba503200239d
- Grant: 019e8a3b-cc8c-79a2-b231-5114cf5e56bd

Start with the next no-access item: dataset/scrub-policy failure fixtures and scrub checks.
```
