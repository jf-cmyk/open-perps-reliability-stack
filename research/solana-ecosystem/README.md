# Solana Ecosystem Research Loop

This directory is the durable memory for continuous Solana ecosystem research supporting Blocksize business development and the Open Perps Reliability Stack (OPRS).

The loop is read-only. It must not request or use private keys, custody access, signing access, capital deployment, live execution, or production trading authority.

## Memory Model

- `state.json` is hot memory. Read it every run. Keep it small and overwrite it only when a material fact, priority, cursor, or decision changes.
- `opportunities.csv` is the ranked Blocksize opportunity pipeline. Update an existing row before adding a duplicate.
- `evidence.ndjson` is the append-only source ledger. One line represents one source-backed finding.
- `roadmap.md` defines the iterative resolution order and acceptance criteria.
- `checkpoints/` contains dated syntheses. Read a checkpoint only when the active queue points to it.

Do not reread all historical checkpoints or the full expert-task transcript on routine runs.

## Five-Minute Run Contract

1. Read `state.json`, the first unresolved roadmap item, and only the relevant opportunity rows.
2. Select one lane using the current five-minute bucket. Do not research every lane on every run.
3. Check at most two primary sources. Use one additional secondary source only for discovery or corroboration.
4. Compare against the stored source URL, publication date, and fact fingerprint. Do not re-summarize unchanged material.
5. If there is no material delta, return `DONT_NOTIFY` and do not create storage churn.
6. If there is a material delta, append one evidence record, update the affected opportunity and hot state, then return a compact digest.
7. Resolve at most one queued question per run. Re-rank the queue after resolution.

Every twelfth run may perform a broader scan across up to four primary sources. The normal run remains narrow.

## Token Policy

- Routine no-delta run: target 250 input-context words beyond tool results and no prose outside the heartbeat XML.
- Material-delta run: target 500 words or fewer in the user digest.
- Store URLs and short fact fingerprints, not copied articles.
- Preserve facts, inferences, confidence, and grant-safety separately.
- Use source-specific cursors and dates instead of restating the full research history.
- Promote only durable conclusions into checkpoints; archive resolved queue items there.

## Source Priority

1. Solana Foundation, Solana official docs, protocol docs, official GitHub releases and proposals.
2. Public onchain/RPC data and protocol-maintained dashboards.
3. Independent analytics with explicit methodology.
4. Media, directories, and social posts for discovery only until primary confirmation.

## Lane Rotation

The twelve five-minute buckets in each hour rotate through:

1. Solana Foundation initiatives and calls to action.
2. Open perps, derivatives, and market structure.
3. Top protocols and developer activity.
4. Whale, liquidity, and capital-flow signals.
5. Validators, client releases, and network pressure.
6. Delegation, stake pools, and validator programs beyond Jito and Marinade.
7. DoubleZero, Alpenglow, Firedancer, Agave, and transport changes.
8. Partnerships and ecosystem infrastructure providers.
9. Tokenized assets, payments, and institutional rails.
10. New Solana business cases.
11. Blocksize partner/account research.
12. Evidence quality, contradiction checks, and grant-safety review.

