# Development Checkpoint: 2026-07-30 Dashboard Drift Boundary Link

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Latest pushed commit before this slice: `2964e07`
- Local untracked items to ignore: none expected after commit

## Scope Lock

- Read-only: yes
- Dry-run/replay: yes
- No signing/custody/submission/capital: yes
- OSS/commercial boundary changes: none

## What Changed Since Previous Checkpoint

- Integrated background Solana research output that advanced the legacy Drift liquidation-history scan from 146,000 to 147,000 finalized transactions.
- Current Drift scan boundary: July 22 back through slot `418112580` at `2026-05-07T04:50:23Z`.
- Current resume cursor: `4G34hATTFfnDRTRt3GHkGYExfU5we2RVtArD128jD8fSEh46dWKGhsMnpcf347gNdEsQ8CxxjLXhE8reVNGLD3Y8`.
- Added direct reviewer links to `docs/drift-liquidation-scan-boundary.md` from the proof-pack index and dashboard.
- Added local MVP and hosted smoke assertions for the scan-boundary link and 147k caveat text.
- Refreshed active grant/application wording and regenerated the local Word proposal so reviewer-facing materials cite the 147,000-transaction scan with the correct caveat.

## Validation Results

Commands run:

```bash
python3 -m json.tool research/solana-ecosystem/state.json
python3 - <<'PY'
import json
from pathlib import Path
for i,line in enumerate(Path('research/solana-ecosystem/evidence.ndjson').read_text().splitlines(), 1):
    if line.strip():
        json.loads(line)
print('PASS evidence.ndjson')
PY
/Users/johannfocke/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_solana_grant_docx.py
/Users/johannfocke/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/johannfocke/.codex/plugins/cache/openai-primary-runtime/documents/26.727.11326/skills/documents/render_docx.py "deliverables/Open Perps Reliability Stack - Solana Foundation Proposal.docx" --output_dir target/docx-render/proposal-147k --emit_pdf
scripts/run_mvp_checks.sh
git diff --check
```

Result summary:

- Research `state.json` and `evidence.ndjson` parse cleanly.
- Word proposal regenerated and rendered for visual QA.
- MVP checks passed.
- `git diff --check` passed.

## Files/Areas Touched

- `index.html`
- `apps/dashboard/index.html`
- `docs/drift-liquidation-scan-boundary.md`
- `docs/checkpoints/README.md`
- `docs/grant-application-draft.md`
- `docs/solana-foundation-application-fields.md`
- `docs/solana-foundation-developer-tooling-proposal.md`
- `deliverables/Open Perps Reliability Stack - Solana Foundation Proposal.docx`
- `research/solana-ecosystem/state.json`
- `research/solana-ecosystem/evidence.ndjson`
- `research/solana-ecosystem/roadmap.md`
- `scripts/build_solana_grant_docx.py`
- `scripts/run_mvp_checks.sh`
- `scripts/run_hosted_smoke_checks.sh`

## Agent Guidance Used

- Architecture: make source-governance limitations visible in the reviewer-facing proof-pack.
- Protocol: keep Drift no-match scans as bounded queue progress only.
- Data: preserve exact scan counts, slot/time bounds, and resume cursor without committing raw transaction/log bodies.
- Liquidator/SDK: keep all live execution, signing, custody, and capital deployment out of scope.
- Grant: update proof-of-work language while preserving claim boundaries.

## Current State

- Latest built artifacts: regenerated local Word proposal and rendered QA output under `target/docx-render/proposal-147k`.
- Known limitations: no historical Drift liquidation candidate has been promoted; Jupiter canonical current IDL/source and verified request/fulfillment pairing remain blocked; Phoenix account-level decode and liquidation replay are not claimed.
- Known local residue: `target/` contains local QA/research outputs and should remain uncommitted.

## Next Queue

Can continue without access:

1. Add a Phoenix/Hawkeye account-level validator plan and scrubbed fixture contract without claiming live replay.
2. Resume Drift legacy liquidation scan from cursor `4G34hATTFfnDRTRt3GHkGYExfU5we2RVtArD128jD8fSEh46dWKGhsMnpcf347gNdEsQ8CxxjLXhE8reVNGLD3Y8`.
3. Add a compact dashboard/proof-pack card for Phoenix exact-input/oracle identity gates.
4. Keep the grant draft warm but do not submit until the founder confirms the running MVP is ready.

Needs access or founder confirmation:

1. Jupiter canonical current IDL/source confirmation from the protocol team or authoritative repository.
2. Approval to send external Jupiter/Phoenix/Termina outreach.
3. Approval to submit the Solana Foundation grant application.
4. Any scope expansion beyond read-only and dry-run.

## Fresh-Window Kickoff Prompt

```text
Continue development for the Blocksize Open Perps Reliability Stack.

Repo: /Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack
Checkpoint: docs/checkpoints/2026-07-30-dashboard-drift-boundary-link-checkpoint.md

Read the checkpoint first, then read docs/checkpoints/context-map.md only for the workstream being touched. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation
```
