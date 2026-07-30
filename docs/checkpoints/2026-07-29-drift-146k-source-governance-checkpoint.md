# Development Checkpoint: 2026-07-29 Drift 146k Source Governance

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Latest pushed commit before this slice: `2aaf945`
- Local untracked items to ignore: none expected after commit

## Scope Lock

- Read-only: yes
- Dry-run/replay: yes
- No signing/custody/submission/capital: yes
- OSS/commercial boundary changes: none

## What Changed Since Previous Checkpoint

- Integrated a background Solana research page that advanced legacy Drift liquidation-history pagination from 145,000 to 146,000 finalized program transactions.
- Page bounds: slot `418197718` at `2026-05-07T14:17:10Z` through slot `418153431` at `2026-05-07T09:22:24Z`.
- Result: zero logs containing `Instruction: Liquidate`.
- New resume cursor: `3SeupC39byPe48KSdxDPpJ8YGfjCAsVCYsU5EK48ZYgaJJgtgyFowkpL7G2ihD5Dz7btpyNcATa7aLw29EoRUVFm`.
- Updated active reviewer-facing docs, public scan-boundary note, research roadmap/state/ledger, and the local Word proposal.

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
/Users/johannfocke/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/johannfocke/.codex/plugins/cache/openai-primary-runtime/documents/26.727.11326/skills/documents/render_docx.py "deliverables/Open Perps Reliability Stack - Solana Foundation Proposal.docx" --output_dir target/docx-render/proposal-146k --emit_pdf
scripts/run_mvp_checks.sh
git diff --check
```

Result summary:

- Research `state.json` and `evidence.ndjson` parse cleanly.
- Word proposal regenerated and rendered for visual QA.
- MVP checks passed.
- `git diff --check` passed.

## Files/Areas Touched

- `research/solana-ecosystem/state.json`
- `research/solana-ecosystem/evidence.ndjson`
- `research/solana-ecosystem/roadmap.md`
- `docs/drift-liquidation-scan-boundary.md`
- `docs/checkpoints/README.md`
- `docs/grant-application-draft.md`
- `docs/solana-foundation-application-fields.md`
- `docs/solana-foundation-developer-tooling-proposal.md`
- `deliverables/Open Perps Reliability Stack - Solana Foundation Proposal.docx`
- `scripts/build_solana_grant_docx.py`

## Agent Guidance Used

- Architecture: keep hosted proof-pack and Word proposal consistent with the latest committed research state.
- Protocol: preserve the no-absence-proof boundary for all Drift scan progress.
- Data: append evidence, store cursors, and avoid raw logs or raw transaction bodies.
- Liquidator/SDK: keep all liquidation work read-only and dry-run only.
- Grant: refresh proof-of-work language but avoid replay or production claims.

## Current State

- Latest built artifacts: regenerated local Word proposal and rendered QA output under `target/docx-render/proposal-146k`.
- Known limitations: no historical Drift liquidation candidate has been promoted; Jupiter canonical current IDL/source and verified request/fulfillment pairing remain blocked; Phoenix account-level decode and liquidation replay are not claimed.
- Known local residue: `target/` contains local QA/research outputs and should remain uncommitted.

## Next Queue

Can continue without access:

1. Resume Drift legacy liquidation scan from cursor `3SeupC39byPe48KSdxDPpJ8YGfjCAsVCYsU5EK48ZYgaJJgtgyFowkpL7G2ihD5Dz7btpyNcATa7aLw29EoRUVFm`.
2. Add a reviewer-visible link from the dashboard/proof-pack UI to the Drift scan-boundary note.
3. Add a Phoenix/Hawkeye account-level validator plan and scrubbed fixture contract without claiming live replay.
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
Checkpoint: docs/checkpoints/2026-07-29-drift-146k-source-governance-checkpoint.md

Read the checkpoint first, then read docs/checkpoints/context-map.md only for the workstream being touched. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation
```
