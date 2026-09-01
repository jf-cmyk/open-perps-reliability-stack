# Service Boundaries

This document separates the current static MVP from future server-side services. The boundary is intentionally conservative: the public grant MVP stays read-only and dry-run only.

## Current Static Proof-Pack Service

Host: Railway static Docker/Nginx service.

Purpose:

- Serve the proof-pack index.
- Serve the static dashboard.
- Serve public docs, schemas, examples, and sample datasets.

Allowed inputs:

- Checked-in repository files copied into the Docker image.
- Railway-injected `PORT`.

Required variables:

- None.

Forbidden variables and capabilities:

- `HELIUS_RPC_URL`
- private RPC URLs
- API keys
- bearer tokens
- private keys
- seed phrases
- wallet files
- signer configuration
- transaction submission endpoints
- block-engine endpoints
- custody, inventory, or capital settings

The static proof-pack service must never fetch private data, submit transactions, sign messages, or expose privileged controls.

## Future Read-Only Decode Worker

Purpose:

- Fetch account, transaction, block, log, or oracle data from read-only Solana sources.
- Decode protocol state for provenance and dataset generation.
- Attach source, slot, commitment, provider, retention, and reconstruction metadata.
- Emit scrubbed public outputs for fixtures, replay inputs, API examples, or dashboard aggregates.

Allowed inputs:

- `HELIUS_RPC_URL` or another read-only RPC URL.
- Public program IDs and account addresses.
- Public slot ranges, signatures, or market identifiers.
- Checked-in adapter schemas and decoder code.

Allowed outputs:

- decoded account summaries
- read-only target discovery reports
- data reconstruction envelopes
- adapter health summaries
- oracle freshness and confidence summaries
- dry-run/replay input datasets
- scrubbed public datasets

Current contract files:

- `docs/read-only-decode-worker.md`
- `schemas/datasets/readonly-decode-worker-run-v0.json`
- `examples/datasets/drift_readonly_decode_worker_run_example.json`

Worker lifecycle states:

- `local_probe`: live output stays under `target/`.
- `scrubbed_example`: committed public examples with no raw bytes or secrets.
- `public_dataset_candidate`: candidate public datasets after manifest, checksum, DQ, and scrub validation.
- `replay_candidate`: future status only when public snapshots are sufficient for deterministic replay; current Drift guardrail outputs remain `replay_ready=false`.

Current local proof command:

```bash
scripts/discover_readonly_targets.py --out target/oprs-readonly-target-discovery/latest.json
```

The command loads `HELIUS_RPC_URL` locally, never prints the URL, probes only public read-only Solana metadata, and writes scrubbed output under `target/`, which is not committed.

If Helius returns `Unauthorized`, the command reached the provider but the local RPC URL is not accepted. Check that `.env` contains the full HTTPS endpoint from the Helius dashboard, including the API key query parameter, and that the key is active for Solana mainnet RPC access. Do not paste the key into chat or commit it.

Forbidden outputs:

- private RPC URL values
- API keys or bearer tokens
- private routing metadata
- wallet balances tied to Blocksize-controlled inventory
- private strategy fields
- signer, custody, capital, or execution configuration

Forbidden capabilities:

- signing
- transaction submission
- transaction retry
- priority-fee bidding
- block-engine submission
- liquidation execution
- wallet or keypair loading
- custody or inventory management
- validator routing
- block-propagation optimization
- skip-rate optimization
- XDP or kernel tuning
- private validator telemetry
- priority-fee or block-engine strategy

## Future Commercial Services

Commercial services may later provide managed integrations, private analytics, premium APIs, or controlled execution tooling. They must stay outside the grant-funded OSS MVP unless a separate founder approval package and scope decision explicitly says otherwise.

Commercial services cannot privatize grant-funded deliverables such as public schemas, public docs, fixture formats, or read-only replay methodology.

Commercial-adjacent ideas from Solana ecosystem research, such as payment/settlement observability or validator readiness assessments for 100M CU, XDP, skip-rate, and block-propagation reporting, are future product lanes only. They are not current OPRS grant deliverables and cannot be described as running services until separate scope, data-access, and claim-boundary decisions are approved.

See [Live readiness path](live-readiness-path.md) for the staged path from static MVP to live read-only diagnostics, commercial diagnostics, and any later execution-readiness candidate.

## Future Live Read-Only Diagnostics

Live read-only diagnostics are the preferred post-MVP service lane because they can support grants, protocol partnerships, and early revenue without adding signer, custody, transaction-submission, or capital risk.

Allowed capabilities:

- scheduled read-only worker runs
- authenticated diagnostics APIs
- private protocol dashboards
- source-backed data-quality reports
- adapter integration support
- incident and reliability retrospectives built from public data

Required gates:

- separate Railway service or equivalent backend boundary
- Railway variables limited to read-only infrastructure
- no secrets in static proof-pack hosting
- source, slot, provider, freshness, checksum, and scrub metadata on generated outputs
- monitoring and runbooks for provider failure, schema drift, stale inputs, and bad outputs
- at least 7 days of continuous read-only operation before treating the service as operationally live

## Promotion Rule

A component can move from local experiment to public OSS only after it passes all of these gates:

- no signer or transaction-submission surface
- no private key, wallet, custody, or capital dependency
- no secret leakage in inputs, outputs, logs, examples, or docs
- deterministic fixture or read-only source provenance
- documented data reconstruction limitations
- scrub-policy validation
- dry-run/replay semantics only
