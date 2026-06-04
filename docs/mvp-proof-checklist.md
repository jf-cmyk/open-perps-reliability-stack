# MVP Proof Checklist

This checklist maps current reviewer-facing claims to public artifacts, validation commands, and known caveats.

## Reviewer URLs

| Surface | URL | Role |
| --- | --- | --- |
| Railway proof pack | `https://refreshing-art-production-86de.up.railway.app/` | Canonical reviewer URL |
| Railway dashboard | `https://refreshing-art-production-86de.up.railway.app/apps/dashboard/` | Canonical dashboard |
| GitHub Pages proof pack | `https://jf-cmyk.github.io/open-perps-reliability-stack/` | Equivalent fallback mirror |
| GitHub Pages dashboard | `https://jf-cmyk.github.io/open-perps-reliability-stack/apps/dashboard/` | Equivalent fallback dashboard |

## Claims And Evidence

| Claim | Evidence | Validation |
| --- | --- | --- |
| The MVP is read-only and dry-run only. | ADR-0001, dashboard markers, dry-run docs, adapter capabilities. | `scripts/run_mvp_checks.sh` checks `Read-only`, `Dry-run`, `No live execution`, `ExecutionDisabledDryRun`, and execute-disabled adapter tests. |
| The public dashboard/API contract exists. | `schemas/api/public-api-v0.json`, `schemas/dashboard/public-dashboard-v0.json`, `examples/api/`. | `cargo run -p oprs-api-types --example validate_api_examples` |
| Dry-run/replay outputs are deterministic and guarded. | `datasets/sample/*`, `crates/oprs-replay`, `docs/liquidation-dry-run.md`. | `cargo run -p oprs-replay --example validate_fixtures` and `cargo test` |
| Pyth-aware risk primitives are implemented as policy helpers. | `crates/oprs-risk/src/lib.rs` and unit tests. | `cargo test -p oprs-risk` or full `cargo test` |
| Data reconstruction provenance is specified. | `schemas/datasets/data-reconstruction-envelope-v0.json`, `examples/datasets/data_reconstruction_envelope.json`. | `scripts/run_mvp_checks.sh` validates JSON and `oprs-data` tests enforce scrub rules. |
| Solana runtime failure modes are modeled for dry-run explanation. | Expanded `RiskReasonCode` variants and `docs/liquidation-dry-run.md`. | `cargo test -p oprs-replay` covers expanded reason-code fixture coverage. |
| Drift is first, Jupiter Perps is second, and Phoenix/Rise is third. | `docs/protocol-targets.md` and decision log. | Manual review of `docs/protocol-targets.md`; Helius live decode proof is still pending. |
| Public reviewer artifacts exclude internal project memory and deployment configs. | `scripts/build_public_artifact.sh`, `.dockerignore`, `docs/public-artifact-boundary.md`. | Hosted smoke checks assert 404 for checkpoints, `.env.example`, `Dockerfile`, `railway.json`, and Railway Nginx config. |
| Railway and GitHub Pages remain equivalent reviewer surfaces. | Railway static deployment and Pages filtered artifact workflow. | `scripts/run_hosted_smoke_checks.sh` against both hosted URLs; `.github/workflows/hosted-smoke.yml` runs hourly and on manual dispatch. |

## Commands

Run the full local validation suite:

```bash
scripts/run_mvp_checks.sh
```

Run hosted smoke checks:

```bash
scripts/run_hosted_smoke_checks.sh https://refreshing-art-production-86de.up.railway.app
scripts/run_hosted_smoke_checks.sh https://jf-cmyk.github.io/open-perps-reliability-stack
```

Build the filtered public artifact used by GitHub Pages:

```bash
scripts/build_public_artifact.sh target/public-proof-pack
```

Run the local read-only target discovery proof after the Helius endpoint is corrected:

```bash
scripts/discover_readonly_targets.py --out target/oprs-readonly-target-discovery/latest.json
```

## Deferred Claims

Do not claim these until evidence lands:

- Historical Drift liquidation reconstruction from live Helius reads.
- Jupiter Perps pool/custody account decode proof.
- Perps market-share or revenue claims without timestamped source snapshots.
- Production liquidation reliability, live execution, priority-fee bidding, custody, signing, or capital deployment.

## Current Helius Status

Local Helius access is confirmed for the first read-only target discovery command. The command writes scrubbed live output under `target/` and does not print the RPC URL. The next blocker is not credentials; it is resolving public Drift market/oracle account targets and Jupiter Perps pool/custody/oracle targets for deeper decode proof.
