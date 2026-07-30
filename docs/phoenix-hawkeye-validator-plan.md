# Phoenix / Hawkeye Validator Plan

This plan defines the next Phoenix/Rise implementation step for OPRS: a local, read-only Hawkeye validator path that can later accept scrubbed fixtures without promoting account-level decode, liquidation replay, or execution claims.

## Source Anchor

The source anchor remains `docs/phoenix-source-authority.md`:

- Rise public commit: `09f59aaf06037ecff395a6c47eea7440f9eef7c2`
- Source Phoenix commit named by release: `6051225fb045fbb5b6a454bd445e7fc2e31e5722`
- Production Phoenix/Rise program: `EtrnLzgbS7nMMy5fbD42kXiUzGg8XQzJ972Xtk1cjWih`
- Production log authority: `GdxfTLSsdSY37G6fZoYtdGDSfgFnbT2EmRpuePZxWShS`
- Production global configuration: `2zskx2iyCvb6Stg7RBZkt1f6MrF4dpYtMG3yMvKwqtUZ`
- Hawkeye program: `RiSeVw3ZjNfsaXPRb4mgaqYaEEt41pNNJoDvVh7pgQj`
- Hawkeye return version: `1`

## Validator Contract

The checked-in contract lives at `examples/datasets/phoenix_hawkeye_validator_plan_example.json` and is validated against `schemas/datasets/phoenix-hawkeye-validator-plan-v0.json`.

It requires:

- Source constants pinned to the Rise public commit above.
- Hawkeye view coverage for margin, asset, liquidation price, BBO, and funding.
- Negative cases for beta-program confusion, raw-return-data leakage, and premature replay claims.
- Scrub policy flags proving raw account data, raw return data, trader addresses, and credentials are not committed.
- Readiness flags keeping local validator implementation, public regression fixtures, account decode, replay, and execution marked false until a later implementation actually earns them.

## Claim Boundary

This plan allows OPRS to say that a Phoenix/Hawkeye validator contract exists and encodes the next gates. It does not allow OPRS to claim:

- Phoenix account-level decode is ready.
- Exact oracle input identity is verified.
- Liquidation replay is ready.
- Any instruction builder, order operation, signing, submission, asset control, or funded execution is in scope.
- Raw Hawkeye return bytes or trader-specific data are safe to publish.

## Local Validation

Run:

```bash
scripts/validate_phoenix_hawkeye_validator_plan.py
```

The validator checks the schema, source constants, blocked readiness claims, scrub flags, and negative self-tests.

## Promotion Gate

The next implementation may add a scrubbed public regression fixture only after:

1. Local validator logic is implemented.
2. Fixture shapes are synthetic or scrubbed.
3. Raw account data and raw return data remain excluded.
4. Exact oracle input identity remains clearly labeled as unverified unless independently proven.
5. Replay and execution readiness remain false unless separate source-backed evidence justifies promotion.
