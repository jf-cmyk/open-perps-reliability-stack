# Development Checkpoint: 2026-07-29 Drift 145k Source Governance

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Latest pushed commit before this slice: `069c955`
- Local untracked items to ignore: none expected after commit

## Scope Lock

- Read-only: yes
- Dry-run/replay: yes
- No signing/custody/submission/capital: yes
- OSS/commercial boundary changes: none

## What Changed Since Previous Checkpoint

- Ran a bounded 5-page Helius-backed Drift scan from cursor `5HhhArgFV7fnKFpvZyucZTpMJYDUtvyWydmzhQvRJq12Na43ELDrzjLArSywM3kyhF1TReEJ4V7AgKMPQ9oPMM2z`.
- The tranche scanned 5,000 additional finalized legacy Drift program transactions.
- Tranche bounds: slot `418377037` at `2026-05-08T10:15:50Z` through slot `418197785` at `2026-05-07T14:17:35Z`.
- Result: zero logs containing `Instruction: Liquidate`.
- Cumulative scan advanced from 140,000 to 145,000 finalized transactions.
- New resume cursor: `2yH8SddMi7BK2aMdjHF5pdFSbQ621Z5zjoDGPsTyRVYBEwem2G9oZZxs4ExNj1qDCXL278DdmACM6YyAunJRzSUT`.
- Updated research state, evidence ledger, active proposal docs, public scan-boundary note, and regenerated the local Word proposal.

## Validation Results

Commands run:

```bash
set -a && source .env && set +a && scripts/discover_drift_liquidation_history.py --before 5HhhArgFV7fnKFpvZyucZTpMJYDUtvyWydmzhQvRJq12Na43ELDrzjLArSywM3kyhF1TReEJ4V7AgKMPQ9oPMM2z --pages 5 --out target/oprs-drift-liquidation-history-probe/latest.json
python3 -m json.tool target/oprs-drift-liquidation-history-probe/latest.json
scripts/validate_drift_liquidation_history_probe.py target/oprs-drift-liquidation-history-probe/latest.json
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
/Users/johannfocke/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/johannfocke/.codex/plugins/cache/openai-primary-runtime/documents/26.727.11326/skills/documents/render_docx.py "deliverables/Open Perps Reliability Stack - Solana Foundation Proposal.docx" --output_dir target/docx-render/proposal-145k --emit_pdf
/Users/johannfocke/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -c 'from docx import Document; p="deliverables/Open Perps Reliability Stack - Solana Foundation Proposal.docx"; text="\n".join(x.text for x in Document(p).paragraphs); print("has_145k", "145,000" in text); print("has_slot", "418197785" in text); print("stale_140_finalized", "140,000 finalized" in text); print("stale_slot", "418377065" in text)'
```

Result summary:

- Drift scan output validated against the local probe schema.
- Research `state.json` and `evidence.ndjson` parse cleanly.
- Word proposal regenerated successfully and rendered to 7 PNG pages plus PDF for visual QA.
- Proposal text contains `145,000` and `418197785`; it does not contain stale `140,000 finalized` or `418377065`.

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

- Architecture: preserve the proof-pack as a reviewer-facing artifact, not an execution service.
- Protocol: Drift no-match scans remain bounded discovery, not absence proof.
- Data: append evidence with exact slot/time bounds and keep raw logs/transactions out of the repo.
- Liquidator/SDK: do not promote any replay or liquidation capability without a validated public candidate.
- Grant: keep proof-of-work current while making limitations visible.

## Current State

- Latest built artifacts: regenerated local Word proposal and rendered QA output under `target/docx-render/proposal-145k`.
- Known limitations: no historical Drift liquidation candidate has been promoted; Jupiter canonical current IDL/source and verified request/fulfillment pairing remain blocked; Phoenix account-level decode and liquidation replay are not claimed.
- Known local residue: `target/oprs-drift-liquidation-history-probe/latest.json` and `target/docx-render/proposal-145k/` are local QA/research outputs and should remain uncommitted.

## Next Queue

Can continue without access:

1. Resume Drift legacy liquidation scan from cursor `2yH8SddMi7BK2aMdjHF5pdFSbQ621Z5zjoDGPsTyRVYBEwem2G9oZZxs4ExNj1qDCXL278DdmACM6YyAunJRzSUT`.
2. Add a Phoenix/Hawkeye account-level validator plan and scrubbed fixture contract without claiming live replay.
3. Add a reviewer-visible link from the dashboard/proof-pack UI to the Drift scan-boundary note.
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
Checkpoint: docs/checkpoints/2026-07-29-drift-145k-source-governance-checkpoint.md

Read the checkpoint first, then read docs/checkpoints/context-map.md only for the workstream being touched. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation
```
