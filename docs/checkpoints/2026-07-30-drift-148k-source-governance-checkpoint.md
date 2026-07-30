# Development Checkpoint: 2026-07-30 Drift 148k Source Governance

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Latest pushed commit before this slice: `bdb5e0c`
- Local untracked items to ignore: none expected after commit

## Scope Lock

- Read-only: yes
- Dry-run/replay: dry-run only
- No signing/custody/submission/capital: yes
- OSS/commercial boundary changes: none

## What Changed Since Previous Checkpoint

- Integrated background Solana research output that advanced the legacy Drift liquidation-history scan from 147,000 to 148,000 finalized transactions.
- Current Drift scan boundary: July 22 back through slot `418069879` at `2026-05-07T00:06:06Z`.
- Current resume cursor: `DihdLBQh1PPFor1cfKAtEYYe6bo1L2BKVjK7gBdF2eoMSjuVHuo9hkvgBW12cGAX7MURkwBD1R9etSZ4USVD9LL`.
- Current result: zero log messages matching `Instruction: Liquidate` across the bounded scan.
- Updated `docs/drift-liquidation-scan-boundary.md`, active grant/application materials, and local/hosted smoke assertions from 147k to 148k.

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
/Users/johannfocke/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/johannfocke/.codex/plugins/cache/openai-primary-runtime/documents/26.727.11326/skills/documents/render_docx.py "deliverables/Open Perps Reliability Stack - Solana Foundation Proposal.docx" --output_dir target/docx-render/proposal-148k --emit_pdf
scripts/run_mvp_checks.sh
git diff --check
```

Result summary:

- Research `state.json` and `evidence.ndjson` parse cleanly.
- Word proposal regenerated and rendered for visual QA.
- Rendered proposal pages 6 and 7 were visually inspected and are clean.
- MVP checks passed.
- `git diff --check` passed.

## Files/Areas Touched

- `docs/drift-liquidation-scan-boundary.md`
- `docs/checkpoints/README.md`
- `docs/checkpoints/2026-07-30-drift-148k-source-governance-checkpoint.md`
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

- Protocol: keep Drift no-match scans as bounded queue progress only.
- Data: preserve exact scan counts, slot/time bounds, and resume cursor without committing raw transaction/log bodies.
- Liquidator/SDK: no live execution, signing, custody, or capital deployment.
- Grant: update proof-of-work language while preserving claim boundaries.

## Current State

- Drift scan has advanced to 148,000 finalized transactions with zero matching `Instruction: Liquidate` logs.
- This does not prove liquidations were absent or that every liquidation path emits the searched log shape.
- Jupiter canonical current IDL/source and verified request/fulfillment pairing remain blocked.
- Phoenix account-level decode, exact oracle-input identity, and liquidation replay remain blocked.

## Next Queue

Can continue without access:

1. Run full local validation for the 148k slice.
2. Commit, push, watch CI/Pages, and rerun hosted smoke checks.
3. Redeploy Railway and verify it serves the 148k Drift boundary plus Phoenix/Hawkeye validator-plan links.
4. Resume Drift legacy liquidation scan from cursor `DihdLBQh1PPFor1cfKAtEYYe6bo1L2BKVjK7gBdF2eoMSjuVHuo9hkvgBW12cGAX7MURkwBD1R9etSZ4USVD9LL`.
5. Add Phoenix exact-input/oracle identity gates as a dashboard/proof-pack card if reviewer visibility still feels thin.

Needs access or founder confirmation:

1. Jupiter canonical current IDL/source confirmation from the protocol team or authoritative repository.
2. Approval to send external Jupiter/Phoenix/Termina outreach.
3. Approval to submit the Solana Foundation grant application.
4. Any scope expansion beyond read-only and dry-run.

## Fresh-Window Kickoff Prompt

```text
Continue development for the Blocksize Open Perps Reliability Stack.

Repo: /Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack
Checkpoint: docs/checkpoints/2026-07-30-drift-148k-source-governance-checkpoint.md

Read the checkpoint first, then read docs/checkpoints/context-map.md only for the workstream being touched. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation
```
