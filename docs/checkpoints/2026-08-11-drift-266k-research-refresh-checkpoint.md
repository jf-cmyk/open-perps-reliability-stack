# Development Checkpoint: 2026-08-11 Drift 266k Research Refresh

## Repo

- Local path: `/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack`
- GitHub: `https://github.com/jf-cmyk/open-perps-reliability-stack`
- Branch: `main`
- Latest pushed commit before this slice: `065f436`
- Local untracked items to ignore: none expected after commit

## Scope Lock

- Read-only: yes
- Dry-run/replay: dry-run only
- No signing/custody/submission/capital: yes
- OSS/commercial boundary changes: none

## What Changed Since Previous Checkpoint

- Integrated the Open Perps portion of the August Solana research refresh.
- Legacy Drift liquidation-history scan advanced from 148,000 to 266,000 finalized transactions.
- Current Drift scan boundary: July 22 back through slot `415904436` at `2026-04-27T01:47:05Z`.
- Current resume cursor: `5TiHF6ziX6862CLuwLJv6AJmjGgmKVQiPrGhex9Leuwfv796XPvaup9XDRk2311JJxZ3wRgYwf8BoHWoxoYcAR46`.
- Current result: zero log messages matching `Instruction: Liquidate` across the bounded scan.
- Updated `docs/drift-liquidation-scan-boundary.md`, active grant/application materials, and local/hosted smoke assertions from 148k to 266k.
- The broader Solana research refresh also adds August findings around 100M-CU activation, Firedancer v1.1.3, payment rails, Frontier Traders, USDPT, SWEEP, Circle/DefiLlama reconciliation, SFDP, and Blocksize validator state. These remain research-only or commercial-adjacent unless a separate proof-pack artifact promotes them with explicit claim boundaries.

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
/Users/johannfocke/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/johannfocke/.codex/plugins/cache/openai-primary-runtime/documents/26.805.11740/skills/documents/render_docx.py "deliverables/Open Perps Reliability Stack - Solana Foundation Proposal.docx" --output_dir target/docx-render/proposal-266k --emit_pdf
scripts/run_mvp_checks.sh
git diff --check
```

Result summary:

- Research `state.json` and `evidence.ndjson` parse cleanly.
- Word proposal regenerated and rendered for visual QA.
- Rendered proposal pages 3 and 6 were visually inspected and are clean.
- MVP checks passed.
- `git diff --check` passed.

## Files/Areas Touched

- `docs/drift-liquidation-scan-boundary.md`
- `docs/checkpoints/README.md`
- `docs/checkpoints/2026-08-11-drift-266k-research-refresh-checkpoint.md`
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

- Protocol: treat the 266k no-match scan as source-governance progress only.
- Data: preserve exact count, slot/time bound, and resume cursor; do not commit raw transaction/log payloads.
- Grant/Research Positioning: broad August research findings should not automatically become MVP claims unless promoted through a bounded public artifact.
- Liquidator/SDK: no live execution, signing, custody, or capital deployment.

## Current State

- Drift scan has advanced to 266,000 finalized transactions with zero matching `Instruction: Liquidate` logs.
- This does not prove liquidations were absent or that every liquidation path emits the searched log shape.
- Jupiter canonical current IDL/source and verified request/fulfillment pairing remain blocked.
- Phoenix account-level decode, exact oracle-input identity, and liquidation replay remain blocked.
- Broader payment, institutional rail, validator, and network findings are useful for future positioning but remain outside the grant-core MVP proof pack unless separately scoped.

## Next Queue

Can continue without access:

1. Run full local validation for the 266k slice.
2. Commit, push, watch CI/Pages, and rerun hosted smoke checks.
3. Redeploy Railway and verify it serves the 266k Drift boundary plus Phoenix/Hawkeye validator-plan links.
4. Resume Drift legacy liquidation scan from cursor `5TiHF6ziX6862CLuwLJv6AJmjGgmKVQiPrGhex9Leuwfv796XPvaup9XDRk2311JJxZ3wRgYwf8BoHWoxoYcAR46`.
5. Add a separate “research-only/commercial-adjacent” appendix if the August network/payment/institutional findings need reviewer-safe visibility.

Needs access or founder confirmation:

1. Jupiter canonical current IDL/source confirmation from the protocol team or authoritative repository.
2. Approval to send external Jupiter/Phoenix/Termina outreach.
3. Approval to submit the Solana Foundation grant application.
4. Any scope expansion beyond read-only and dry-run.

## Fresh-Window Kickoff Prompt

```text
Continue development for the Blocksize Open Perps Reliability Stack.

Repo: /Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack
Checkpoint: docs/checkpoints/2026-08-11-drift-266k-research-refresh-checkpoint.md

Read the checkpoint first, then read docs/checkpoints/context-map.md only for the workstream being touched. Scope remains read-only and dry-run only: no production execution, no signing, no custody, no live transaction submission, and no capital deployment.

After each completed task, commit and push, then report next steps split into:
- can continue without access
- needs access or founder confirmation
```
