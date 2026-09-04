# Read-Only Decode Worker

The read-only decode worker is a future local worker shape, not a production service. Its first contract is a one-shot command that loads a local read-only RPC URL, fetches allowlisted public protocol accounts, decodes only reviewed public fields, and emits scrubbed artifacts under `target/`.

## Current Status

- Lifecycle: `local_probe` and `scrubbed_example`
- Protocol scope: Drift v2 first, Jupiter role-map contrast, and Phoenix public telemetry companion
- Hosting scope: not deployed
- Railway scope: static proof pack only; no worker secrets
- Output scope: public account identity, metadata, guardrail labels, source refs, hashes, readiness flags

## Allowed Inputs

- A local read-only HTTPS RPC URL from `.env`
- Public program IDs and allowlisted account targets
- Pinned protocol source commits, IDL hashes, and source file refs
- Commitment level and bounded target set

## Allowed Outputs

- Worker run manifest
- Source provenance
- Provider label without credential value
- Slot/context metadata
- Anchor discriminator checks
- Account data length and SHA-256
- Decoded public fields
- Source-backed semantic labels
- Validation failures and readiness flags

## Required False Flags

Every worker run must keep these false until a separate founder-approved scope change:

- `raw_account_data_committed=false`
- `user_state_decoded=false`
- `market_economics_decoded=false`
- `replay_ready=false`
- `signing_enabled=false`
- `transaction_submission_enabled=false`
- `priority_fee_bidding_enabled=false`
- `keypair_loading_enabled=false`
- `custody_enabled=false`
- `capital_management_enabled=false`

## Forbidden

- Signing
- Transaction submission
- Transaction retry
- Priority-fee bidding
- Block-engine submission
- Keypair loading
- Custody or inventory management
- Capital management
- Raw account byte export
- RPC URL, API key, bearer token, local path, wallet, signer, or private route leakage

## Contract Files

- Schema: `schemas/datasets/readonly-decode-worker-run-v0.json`
- Example: `examples/datasets/drift_readonly_decode_worker_run_example.json`
- Local one-shot wrapper: `scripts/run_readonly_worker_once.py`
- Private run envelope schema: `schemas/datasets/readonly-worker-run-envelope-v0.json`
- Private run envelope example: `examples/datasets/readonly_worker_run_envelope_example.json`
- Private run envelope builder: `scripts/build_readonly_worker_run_envelope.py`
- Private run envelope validator: `scripts/validate_readonly_worker_run_envelope.py`
- Public candidate schema: `schemas/datasets/readonly-worker-public-candidate-v0.json`
- Public candidate example: `examples/datasets/readonly_worker_public_candidate_example.json`
- Public candidate builder: `scripts/build_readonly_worker_public_candidate.py`
- Public candidate validator: `scripts/validate_readonly_worker_public_candidate.py`

The example is a scrubbed public artifact. It describes the worker contract and current Drift guardrail proof shape without committing live target output or raw account bytes.

## Local Wrapper

The local one-shot wrapper is the pre-Railway worker command surface:

```bash
scripts/run_readonly_worker_once.py --job drift-state-smoke --plan
scripts/run_readonly_worker_once.py --job jupiter-role-map-smoke --plan
scripts/run_readonly_worker_once.py --job phoenix-telemetry-smoke --plan
scripts/run_readonly_worker_once.py --job slack-sample-dry-run --execute
```

`--plan` is the default. Use `--execute` only for an intentional bounded run. Outputs stay under `target/oprs-worker-runs/`, and live worker output must not be sent to Slack until a separate payload builder and validator exist.

## Latest Local Smoke

Date: 2026-09-03

Executed locally with `scripts/run_readonly_worker_once.py --execute` and validated:

- `drift-state-smoke`
- `jupiter-role-map-smoke`
- `phoenix-telemetry-smoke`

Outputs were written under `target/oprs-worker-runs/` and were not committed or published. This proves the local wrapper can run bounded read-only probes across the current priority venues; it does not create a hosted worker deployment, scheduled job, public output promotion, or execution scope.

## Private Run Envelope

After local worker outputs validate, build a private envelope:

```bash
scripts/build_readonly_worker_run_envelope.py
scripts/validate_readonly_worker_run_envelope.py target/oprs-worker-run-envelopes/latest.json
```

The envelope records paths, checksums, byte lengths, protocol labels, validator status, and promotion policy. It does not copy worker payload bodies, raw account data, raw transactions, RPC URLs, API keys, Slack webhooks, signer settings, custody settings, or capital settings.

The checked-in example is public documentation of the envelope shape only. Generated envelopes under `target/oprs-worker-run-envelopes/` remain private target output until founder review, validator pass, and scrub pass.

## Public Candidate Summary

After the private envelope validates, build a public-safe candidate summary:

```bash
scripts/build_readonly_worker_public_candidate.py
scripts/validate_readonly_worker_public_candidate.py target/oprs-worker-public-candidates/latest.json
```

By default, the candidate status is `blocked_pending_founder_review`. It includes protocol names, dataset names, artifact hashes, validator status, and false replay/execution flags. It excludes private artifact paths and payload bodies.
