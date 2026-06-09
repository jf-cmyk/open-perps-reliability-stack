# Public Dataset Contract

Public datasets in this repo are small, scrubbed proof-pack artifacts. They are not raw data exports and they are not production monitoring feeds.

## Shared Package Rules

Each public dataset package must include:

- `manifest.json`
- one or more payload files
- `dq.json`
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

The first package profile is `drift-guardrails-v0`.

It intentionally remains specialized until another package type applies pressure to the shared contract. Generalization should happen only after a second package type, such as replay fixtures or oracle snapshots, shares most of the same validation logic.
