# 2026-09-01 Jupiter Role Map And Drift 318k Checkpoint

## Status

This slice moved two no-access workstreams forward without changing the read-only and dry-run boundary.

Jupiter Perps now has a local-only lifecycle role-map probe. The probe uses the hash-pinned onchain Anchor IDL and recent public transaction samples to bind observed instruction account indexes to IDL role names. It stores only hashed signatures/account identifiers under `target/` and does not publish raw transactions, raw instruction data, account bytes, wallet data, signers, or credentials.

The first live run sampled 40 recent Jupiter Perps program signatures and 20 transaction bodies. It found 34 Jupiter instruction observations, with 21 matched to onchain-IDL roles using IDL-name and snake-case IDL-name Anchor discriminator derivations. Matched instruction names included `closePositionRequest2`, `instantCreateLimitOrder`, `instantCreateTpsl`, `instantDecreasePosition`, `instantIncreasePosition`, `instantIncreasePositionPreSwap`, `refreshAssetsUnderManagement`, `setTokenLedger`, and `swap2`.

Legacy Drift liquidation-history pagination advanced from 308,000 to 318,000 finalized program transactions. The latest bounded tranche covered slots `415272965` through `415091952`, from `2026-04-24T04:25:56Z` through `2026-04-23T08:31:20Z`, and found zero logs beginning with `Program log: Instruction: Liquidate`.

## Files Added

- `scripts/discover_jupiter_lifecycle_role_map.py`
- `schemas/datasets/jupiter-lifecycle-role-map-probe-v0.json`
- `examples/datasets/jupiter_lifecycle_role_map_probe_example.json`

## Files Updated

- `docs/jupiter-perps-provenance.md`
- `docs/jupiter-source-authority-resolution.md`
- `docs/proof-pack-changelog.md`
- `docs/drift-liquidation-scan-boundary.md`
- `docs/solana-foundation-application-fields.md`
- `docs/grant-application-draft.md`
- `docs/solana-foundation-developer-tooling-proposal.md`
- `research/solana-ecosystem/state.json`
- `research/solana-ecosystem/roadmap.md`
- `research/solana-ecosystem/evidence.ndjson`
- `scripts/run_mvp_checks.sh`
- `scripts/run_hosted_smoke_checks.sh`
- `scripts/build_solana_grant_docx.py`

## Claim Boundary

Allowed:

- Jupiter source-authorized account-layout decode.
- Jupiter structural instruction role-map inspection from onchain IDL and public transactions.
- Bounded Drift public transaction pagination progress.
- Local-only target outputs and public-safe summaries.

Blocked:

- Verified Jupiter request/fulfillment pairing.
- Jupiter before/after lifecycle-state proof.
- Keeper semantics.
- Historical liquidation replay.
- Liquidation absence claims.
- Signing, transaction submission, order building, priority-fee bidding, custody, capital deployment, and production execution.

## Validation Queue

Before committing, run:

```bash
scripts/run_mvp_checks.sh
```

After public deploy, run hosted smoke checks against both canonical Railway and GitHub Pages.

## Next Queue

1. Refresh the local Solana Foundation DOCX from the updated grant script and visually QA it.
2. Commit and push this slice.
3. Deploy the updated static proof pack to Railway and verify GitHub Pages after Actions complete.
4. Continue Drift legacy pagination from cursor `2fhTXQqs9qnyX4mBrcKAuTLipxnWyfLG7kj7YRn3EpRNBQoRLignDCCVxCRx1ckfntdhYsSuC6deefgTLS9ghYKm`.
5. Use the Jupiter role-map output to design a local verified-pairing validator, but keep it blocked until before/after state evidence and source-review gates are defined.
6. Consider the Phoenix source-backed adapter/proof-package spike once Jupiter lifecycle pairing hits the current blocker.

## Resume Prompt

Continue the Open Perps Reliability Stack from `docs/checkpoints/2026-09-01-jupiter-role-map-drift-318k-checkpoint.md`. Preserve read-only and dry-run scope. First run `git status --short`, then run the validation queue if it has not passed. If validation passes, refresh the DOCX, commit, push, deploy Railway, and smoke both Railway and GitHub Pages. Continue no-access development with Drift pagination from cursor `2fhTXQqs9qnyX4mBrcKAuTLipxnWyfLG7kj7YRn3EpRNBQoRLignDCCVxCRx1ckfntdhYsSuC6deefgTLS9ghYKm` or the Jupiter verified-pairing validator design, without claiming live replay or execution readiness.
