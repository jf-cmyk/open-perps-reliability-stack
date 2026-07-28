# Development Checkpoint: 2026-07-28 Drift 115k Grant Refresh

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Latest pushed commit: `3610cde Advance Drift liquidation scan evidence`
- Local untracked items to ignore: none observed after commit and deploy.

## Scope Lock

- Read-only: yes.
- Dry-run/replay: yes.
- No signing/custody/submission/capital: yes.
- OSS/commercial boundary changes: none. Commercial services remain future/out-of-scope and cannot privatize grant-funded artifacts.

## What Changed Since Previous Checkpoint

- Integrated Solana research loop output advancing legacy Drift liquidation-history pagination from 35,000 to 115,000 finalized program transactions.
- Current Drift scan boundary: July 22 back through slot `418676295` at `2026-05-09T19:41:01Z`.
- Current Drift resume cursor: `37Yf1145SE1NBcny67ufNjtBykHAzFrEXcmS26Kw7wdGvotrkbL9L86sDHUT48QvapJSS9aF9Z7abWGt5X3ETFBh`.
- No `Instruction: Liquidate` log candidates were found. This remains bounded queue progress only, not evidence that liquidations were absent.
- Refreshed grant/application wording and regenerated the local Word proposal so reviewer-facing materials cite the 115,000-transaction scan with the correct caveat.

## Validation Results

Commands run:

```bash
python3 -m json.tool research/solana-ecosystem/state.json
python3 -c 'import json, pathlib; p=pathlib.Path("research/solana-ecosystem/evidence.ndjson"); [json.loads(line) for line in p.read_text().splitlines() if line.strip()]; print("PASS evidence.ndjson")'
/Users/johannfocke/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_solana_grant_docx.py
/Users/johannfocke/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/johannfocke/.codex/plugins/cache/openai-primary-runtime/documents/26.727.11326/skills/documents/render_docx.py "deliverables/Open Perps Reliability Stack - Solana Foundation Proposal.docx" --output_dir target/docx-render/proposal-115k --emit_pdf
scripts/run_mvp_checks.sh
git diff --check
git push
gh run watch 30402945890 --exit-status
gh run watch 30402945952 --exit-status
railway up --detach
scripts/run_hosted_smoke_checks.sh https://refreshing-art-production-86de.up.railway.app
scripts/run_hosted_smoke_checks.sh https://jf-cmyk.github.io/open-perps-reliability-stack
```

Result summary:

- MVP checks passed.
- DOCX rendered to 7 pages; affected proof-of-work pages visually checked clean.
- GitHub CI passed.
- GitHub Pages deploy passed.
- Railway deployment `e6dc8a87-92b6-4898-b770-9bd01a80bfc5` succeeded.
- Hosted smoke checks passed for Railway and GitHub Pages.

## Files/Areas Touched

- `research/solana-ecosystem/evidence.ndjson`
- `research/solana-ecosystem/roadmap.md`
- `research/solana-ecosystem/state.json`
- `docs/grant-application-draft.md`
- `docs/solana-foundation-application-fields.md`
- `docs/solana-foundation-developer-tooling-proposal.md`
- `scripts/build_solana_grant_docx.py`
- `deliverables/Open Perps Reliability Stack - Solana Foundation Proposal.docx`

## Agent Guidance Used

- Protocol / Solana research: Drift legacy reconstruction must rely on public finalized transaction evidence and pinned legacy source; migrated Velocity-hosted data can be discovery or corroboration only.
- Grant positioning: treat Drift pagination as queue progress only; keep Jupiter source-authority blocked; keep Phoenix/Rise source-pinned but not account-level replay proof.
- Data / source governance: publish only scrubbed public artifacts; do not commit RPC URLs, raw account bytes, private strategy, signer/custody metadata, or live API captures.

## Current State

- Latest built artifacts: Railway proof pack and dashboard, GitHub Pages fallback, regenerated local Word proposal.
- Known limitations: no source-backed Drift historical liquidation reconstruction yet; no Jupiter canonical IDL/source authority; no Phoenix account-level decode, exact oracle input identity, liquidation replay, trader monitoring, or live execution.
- Known local residue: render QA outputs under `target/docx-render/`; these are generated and not public artifacts.

## Next Queue

Can continue without access:

1. Resume public legacy Drift pagination from cursor `37Yf1145SE1NBcny67ufNjtBykHAzFrEXcmS26Kw7wdGvotrkbL9L86sDHUT48QvapJSS9aF9Z7abWGt5X3ETFBh`.
2. Build a Phoenix/Hawkeye account-level validator plan that starts with source constants and scrubbed public fixtures, without promoting replay claims.
3. Add a compact source-governance note explaining why 115,000 no-match scans still do not prove absence.
4. Keep Railway and GitHub Pages equivalent after each public artifact change.

Needs access or founder confirmation:

1. Jupiter maintainer/source confirmation for canonical current IDL/source authority before binary decode or verified request/fulfillment pairing claims.
2. Founder approval before grant submission or any external outreach.
3. Founder approval before expanding scope into commercial APIs, managed integrations, private analytics, execution tooling, or any non-read-only service.

## Fresh-Window Kickoff Prompt

```text
Continue development for the Blocksize Open Perps Reliability Stack.

Repo: /Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack
Checkpoint: docs/checkpoints/2026-07-28-drift-115k-grant-refresh-checkpoint.md

Read the checkpoint first, then read docs/checkpoints/context-map.md only for the workstream being touched. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

The latest Drift legacy pagination state is 115,000 scanned finalized transactions through slot 418676295, with resume cursor 37Yf1145SE1NBcny67ufNjtBykHAzFrEXcmS26Kw7wdGvotrkbL9L86sDHUT48QvapJSS9aF9Z7abWGt5X3ETFBh. This is queue progress only, not proof that liquidations were absent.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation
```
