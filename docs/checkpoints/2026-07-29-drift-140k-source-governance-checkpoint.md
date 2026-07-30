# Development Checkpoint: 2026-07-29 Drift 140k Source Governance

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Latest pushed commit before this slice: `097c8f2`
- Local untracked items to ignore: none expected after commit

## Scope Lock

- Read-only: yes
- Dry-run/replay: yes
- No signing/custody/submission/capital: yes
- OSS/commercial boundary changes: none

## What Changed Since Previous Checkpoint

- Integrated the Solana research loop output that advanced legacy Drift liquidation-history pagination from 115,000 to 140,000 finalized program transactions.
- Current Drift scan boundary: July 22 back through slot `418377065` at `2026-05-08T10:16:02Z`.
- Current resume cursor: `5HhhArgFV7fnKFpvZyucZTpMJYDUtvyWydmzhQvRJq12Na43ELDrzjLArSywM3kyhF1TReEJ4V7AgKMPQ9oPMM2z`.
- Added a public source-governance note explaining why no-match liquidation scans are bounded queue progress only and do not prove absence.
- Refreshed grant/application wording and regenerated the local Word proposal so reviewer-facing materials cite the 140,000-transaction scan with the correct caveat.
- Left the 115k checkpoint unchanged as historical project memory.

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
/Users/johannfocke/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/johannfocke/.codex/plugins/cache/openai-primary-runtime/documents/26.727.11326/skills/documents/render_docx.py "deliverables/Open Perps Reliability Stack - Solana Foundation Proposal.docx" --output_dir target/docx-render/proposal-140k --emit_pdf
/Users/johannfocke/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -c 'from docx import Document; p="deliverables/Open Perps Reliability Stack - Solana Foundation Proposal.docx"; text="\n".join(x.text for x in Document(p).paragraphs); print("has_140k", "140,000" in text); print("has_slot", "418377065" in text); print("stale_115_finalized", "115,000 finalized" in text); print("stale_slot", "418676295" in text)'
scripts/run_mvp_checks.sh
git diff --check
```

Result summary:

- `research/solana-ecosystem/state.json` is valid JSON.
- `research/solana-ecosystem/evidence.ndjson` parses cleanly.
- Word proposal regenerated successfully and rendered to 7 PNG pages plus PDF for visual QA.
- Proposal text contains `140,000` and `418377065`; it does not contain stale `115,000 finalized` or `418676295`.
- MVP checks passed, including Rust tests, fixture replay validation, public API example validation, public package validators, public artifact boundary checks, and local Helius config detection.
- `git diff --check` passed.

## Files/Areas Touched

- `research/solana-ecosystem/state.json`
- `research/solana-ecosystem/evidence.ndjson`
- `research/solana-ecosystem/roadmap.md`
- `docs/drift-liquidation-scan-boundary.md`
- `docs/README.md`
- `docs/grant-application-draft.md`
- `docs/solana-foundation-application-fields.md`
- `docs/solana-foundation-developer-tooling-proposal.md`
- `deliverables/Open Perps Reliability Stack - Solana Foundation Proposal.docx`
- `scripts/build_solana_grant_docx.py`
- `scripts/run_mvp_checks.sh`

## Agent Guidance Used

- Architecture: preserve source-governance boundaries and avoid historical replay overclaims.
- Protocol: treat Drift no-match liquidation pages as scanner progress only until source-backed candidate promotion.
- Data: keep evidence append-only, scrubbed, and parse-validated.
- Liquidator/SDK: no live execution, no signing, no custody, no capital deployment.
- Grant: update reviewer-facing proof-of-work language while keeping caveats prominent.

## Current State

- Latest built artifacts: regenerated local Word proposal and rendered QA output under `target/docx-render/proposal-140k`.
- Known limitations: no historical Drift liquidation candidate has been promoted; Jupiter canonical current IDL/source and verified request/fulfillment pairing remain blocked; Phoenix account-level decode and liquidation replay are not claimed.
- Known local residue: `target/` render and build artifacts are local QA output and should remain uncommitted unless a specific artifact is intentionally promoted.

## Next Queue

Can continue without access:

1. Resume Drift legacy liquidation scan from cursor `5HhhArgFV7fnKFpvZyucZTpMJYDUtvyWydmzhQvRJq12Na43ELDrzjLArSywM3kyhF1TReEJ4V7AgKMPQ9oPMM2z`.
2. Add a Phoenix/Hawkeye account-level validator plan and scrubbed fixture contract without claiming live replay.
3. Tighten the dashboard/proof-pack wording so the new scan-boundary note is easy for reviewers to find.
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
Checkpoint: docs/checkpoints/2026-07-29-drift-140k-source-governance-checkpoint.md

Read the checkpoint first, then read docs/checkpoints/context-map.md only for the workstream being touched. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation
```
