# Public Dataset Contract

Public datasets in this repo are small, scrubbed proof-pack artifacts. They are not raw data exports and they are not production monitoring feeds.

## Shared Package Rules

Each public dataset package must include:

- `manifest.json`
- one or more payload files
- `dq.json`
- an entry in `examples/public/contract-index.json`
- package-local relative paths only
- deterministic SHA-256 checksums for every listed payload
- row counts for every listed payload
- `capability=read_only_dry_run`
- scrub status and blocking-failure count
- known limitations

## DQ Severity

DQ checks use three severities:

- `block_publish`: must pass before the package can be served publicly.
- `warn_public`: may be public if the limitation is disclosed.
- `internal_only`: not allowed in the public proof pack.

The public package status is mechanically blocked if any `block_publish` gate fails.

## Scrub Rules

Public packages must not contain provider credentials, local machine paths, raw byte payloads, private route labels, privileged account controls, execution-resource controls, user-state claims, custody fields, or capital-management fields.

Allowed public content includes public program IDs, public account addresses, public source links, pinned commits, synthetic fixture labels, deterministic hashes, source limitations, and read-only/dry-run readiness flags.

## Current Package Profiles

The first package profile is `drift-guardrails-v0`. The second package profile is `jupiter-authority-gap-v0`. The third package profile is `jupiter-onchain-decode-v0`. The fourth package profile is `phoenix-market-telemetry-v0`. The fifth package profile is `slot-regime-benchmark-v0`.

`readonly-worker-candidate-template-v0` is a promotion template, not a public dataset package. It defines the future manifest and DQ gates for a selected read-only worker public candidate, while keeping public-output promotion blocked until founder review, final scrub, checksum binding, zero blocking DQ failures, and contract-index review are complete.

Validators intentionally remain specialized until another package type applies pressure to the shared contract. Generalization should happen only when multiple package types share most of the same validation logic without weakening their domain-specific claim boundaries.

The public contract index is intentionally small. It records package IDs, payload schema paths, validators, publishability, and claim boundaries so future packages can share discovery and review conventions without forcing a generic validator too early.

The shared validator helper in `scripts/public_package_contract.py` owns mechanical checks only: JSON loading, bounded JSON Schema validation for the checked-in schema subset, safe relative paths, blocked public-text patterns, contract-index lookup, payload schema-version agreement, checksums, row counts, and manifest/DQ publish gates. Package-specific validators still own semantic claims such as Drift guardrail readiness or Jupiter verified-pairing blockers.

Invalid package fixtures live under `tests/fixtures/public-packages/invalid/`. They are not served publicly; they mutate otherwise valid packages to prove validators reject replay-readiness overclaims, raw-payload leaks, checksum drift, local path leaks, malformed schema shape, Jupiter verified-pairing overclaims, unsafe evidence refs, secret markers, and contract-index drift.

`phoenix-market-telemetry-v0` is a source-backed static package for Phoenix/Rise public market-data readiness. It maps public HTTP and WebSocket telemetry surfaces for exchange snapshots, market configuration, L2 orderbook snapshots, market-statistics history, funding-rate history, and live L2 streams. It does not commit live API response bodies, trader state, authenticated flows, instruction builders, order operations, signing, transaction submission, or historical replay readiness.

`slot-regime-benchmark-v0` is a source-backed static package for Solana runtime benchmark windows around the 400ms-to-350ms slot-time activation at slot `440208000`. It records pre/post reference windows for future normalization only. It does not claim achieved slot duration, faster confirmations, better landing, lower replay pressure, venue-level market-quality improvement, Blocksize validator readiness, signing, transaction submission, or replay readiness.

`jupiter-onchain-decode-v0` is a source-authorized read-only package for Jupiter Perps account-layout decode. It pins the live program's onchain Anchor IDL address and normalized IDL hash, records that the prior docs-linked third-party candidate does not match the onchain IDL, and publishes scrubbed decode evidence for `Position` and `PositionRequest`. It does not claim verified request/fulfillment pairing, historical liquidation replay, keeper behavior, signing, transaction submission, or production execution.
