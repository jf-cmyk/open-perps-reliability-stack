# Drift Source Repository Migration

Date: 2026-07-22

Primary evidence:

- Repository: https://github.com/velocity-exchange/protocol-v2
- Migration commit: https://github.com/velocity-exchange/protocol-v2/commit/b516f71e05527e9c735164a069345ee3f6e8a57b
- OPRS-pinned source commit: https://github.com/velocity-exchange/protocol-v2/commit/0ae3e3b1db782a6765c3525b3dec38ad4d9d3a62

## Finding

Requests for `drift-labs/protocol-v2` now resolve to a repository whose canonical GitHub `full_name` is `velocity-exchange/protocol-v2`. The June 23 migration commit rewrote workflow dispatch targets, dependency URLs, SDK/documentation links, and repository metadata from `drift-labs` to `velocity-exchange`.

The immutable commit currently pinned by OPRS, `0ae3e3b1db782a6765c3525b3dec38ad4d9d3a62`, remains present in the migrated repository. Existing decode semantics are therefore not invalidated by the organization move.

## OPRS Impact

The workspace still contains multiple `github.com/drift-labs/protocol-v2` references in discovery scripts, decoder-provenance documentation, and example datasets. Redirects may keep them functional today, but canonical source governance should not depend on an undocumented redirect.

Required follow-up:

1. Preserve the pinned commit SHA.
2. Change canonical source URLs to `velocity-exchange/protocol-v2`.
3. Record the former repository path as migration provenance where useful.
4. Re-run public-package and read-only-state validators after the mechanical URL update.
5. Do not describe this evidence as a protocol shutdown, product rebrand, or ownership change without separate primary confirmation.
