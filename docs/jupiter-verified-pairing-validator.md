# Jupiter Verified Pairing Validator Contract

This contract defines the next Jupiter Perps evidence gate after the lifecycle role-map probe. It is a design and validation target only. It does not claim that request/fulfillment pairing, keeper semantics, liquidation replay, or execution readiness is already proven.

## Current Evidence

Current Jupiter evidence:

- Public target discovery identifies the Jupiter Perps program, custody accounts, and oracle-style surfaces.
- The live onchain Anchor IDL is hash-pinned and used for account-layout decode.
- `Position` and `PositionRequest` account-layout decode is source-authorized through the onchain IDL.
- The local lifecycle role-map probe binds sampled public transaction account indexes to onchain-IDL instruction roles.

Current blocker:

- A role map proves that an observed instruction account index corresponds to an IDL role name. It does not prove that one position request became one fulfilled position transition, that a keeper completed the lifecycle, or that a dry-run replay can reconstruct the market state.

## Validator Goal

The verified-pairing validator should answer one narrow question:

Can a bounded public Jupiter transaction sample show a source-backed lifecycle pair where a `PositionRequest` or equivalent request-state account is observed before and after a fulfillment path, with the observed instruction roles matching the onchain IDL?

The answer can be:

- `verified_pair`: evidence is sufficient for a narrow pairing claim.
- `candidate_pair`: related accounts and roles are observed, but before/after state or source authority is incomplete.
- `rejected_pair`: evidence is weak, malformed, or violates claim boundaries.

## Required Inputs

Allowed inputs:

- read-only RPC transaction history
- read-only account snapshots
- onchain Anchor IDL
- official Jupiter documentation URLs
- hash-only signature and account identifiers in committed examples
- local `target/` files that may contain private raw fetch details before scrubbing

Forbidden inputs:

- private keys
- signer configuration
- wallet files
- private route strategy
- custody inventory
- transaction submission endpoints
- priority-fee or block-engine strategy

## Required Evidence

A validator candidate must include:

- onchain IDL hash and source timestamp
- instruction discriminator and IDL instruction name
- role bindings for request, position, owner/authority, custody, oracle, and program-owned state where present
- hashed signature identifiers
- hashed account identifiers
- pre-state slot and post-state slot when available
- account owner checks
- account discriminator checks when applicable
- before/after state-transition fields only if source-reviewed
- explicit confidence and rejection reasons

## Promotion Gates

Promote to `verified_pair` only if all gates pass:

- onchain IDL hash is present
- observed instructions match onchain-IDL discriminators
- role bindings include a request-like account and a position-like or fulfillment target account
- pre-state and post-state are both present from read-only public data
- source-reviewed fields show a lifecycle transition
- account owners and discriminators match expected Jupiter-owned surfaces
- raw transaction bodies, raw instruction bytes, and raw account bytes are not committed
- signer, custody, capital, transaction-submission, and execution flags are false
- validator reports no blocking data-quality failures

Keep as `candidate_pair` when:

- roles match but pre/post state is missing
- only one side of the lifecycle is observed
- source-reviewed state-transition fields are not available
- account identity is hashed but sufficient state evidence is incomplete

Reject as `rejected_pair` when:

- source authority is invalid
- account owners or discriminators conflict with expected surfaces
- role bindings do not include request or fulfillment surfaces
- raw private data or execution markers appear
- the evidence would require live transaction submission or signer access

## Output Contract

The future machine-readable output should include:

- `schema_version`
- `dataset_name`
- `protocol`
- `chain_id`
- `source_authority`
- `query`
- `pairing_candidates`
- `readiness`
- `known_limitations`
- `forbidden_actions`

Current fixture contract:

- Schema: `schemas/datasets/jupiter-verified-pairing-fixture-v0.json`
- Rejected fixture: `examples/datasets/jupiter_verified_pairing_rejected_fixture.json`
- Synthetic positive fixture: `examples/datasets/jupiter_verified_pairing_synthetic_positive_fixture.json`
- Validator: `scripts/validate_jupiter_verified_pairing_fixture.py`

The rejected fixture models the current role-map-only state. The synthetic positive fixture proves the gate behavior for a complete pair, but it still sets `mainnet_verified_pairing_claimed=false` and `public_claims_allowed=false`.

Required false flags until a verified pair exists:

- `verified_request_fulfillment_pair_claimed=false`
- `position_request_state_transition_claimed=false`
- `keeper_semantics_claimed=false`
- `liquidation_replay_claimed=false`
- `execution_claimed=false`
- `raw_transaction_committed=false`
- `raw_instruction_data_committed=false`
- `raw_account_bytes_committed=false`
- `account_pubkeys_committed=false`

## First Implementation Step

Build the validator as a local-only script that consumes `target/oprs-jupiter-lifecycle-role-map/latest.json` and a future bounded account-snapshot file. The first version should only classify candidates and explain missing evidence.

It should not fetch more data by default. Fetching belongs to a separate read-only probe command so the validator remains deterministic and testable.

## Success Definition

Short-term success:

- The validator can reject the current role-map output as not yet pair-verified for explicit reasons.
- The validator can accept a synthetic positive fixture only when all promotion gates are present.
- The public proof pack can show the validator contract without claiming Jupiter replay readiness.

Production success:

- Not in scope. This validator is an evidence gate for read-only and dry-run claims only.
