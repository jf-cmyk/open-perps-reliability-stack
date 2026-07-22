# Drift-To-Velocity Data Boundary

Date: 2026-07-22

## Verified Change

The former Drift Data API documentation redirects to Velocity Protocol. The redirected page says its proposed Velocity host is provisional and mirrors Drift's legacy host pattern. The live `data.api.drift.trade` OpenAPI endpoint still responds, but identifies itself as `Velocity Data API`.

The live specification documents per-user liquidation records with transaction signatures, slots, liquidation types, margin and collateral values, and type-specific fields. Its latest per-user endpoint is described as covering 31 days. This is a useful discovery surface, but its migrated identity prevents treating it as the sole authority for legacy Drift history.

## Bounded Onchain Check

A validated read-only paginator has scanned 6,000 transactions for legacy program `dRiftyHA39MWEi3m9aunc5MzRF1JYuBsbn6VPcn33UH`, from slot 434444514 at 2026-07-22T04:55:17Z through slot 426802213 at 2026-06-16T06:58:14Z. It found no transaction log containing an Anchor `Instruction: Liquidate*` entry. The next cursor is signature `5GRuYzsVZPxWJPWAVDmDiZ5tYx7P7i876UG3FfPpUenub5oGGbuc82CxdxZvKLdVjsVUriBTgCRwGWfdhqMrTaWj`. This is a bounded cursor result only and does not establish liquidation frequency or absence outside the scan.

The paginator is `scripts/discover_drift_liquidation_history.py`. It reads the RPC URL from the environment, limits RPC batches to 50 transactions after a payload-limit validation, and outputs only public signature, slot, timestamp, transaction status, matching logs, and the next cursor.

## Reconstruction Rule

The first OPRS historical Drift reconstruction must:

1. page backward until a public legacy `Liquidate*` transaction is found;
2. verify signature, slot, program invocation, accounts, logs, and success on Solana;
3. interpret the instruction and event using the pinned legacy program source;
4. use hosted API fields only as corroboration;
5. distinguish transaction/event facts from reconstructed pre/post-state inferences;
6. remain deterministic, read-only, non-signing, and non-executing.

## Claim Boundary

Do not call the migrated hosted API canonical for legacy Drift, assume Velocity and Drift records are interchangeable, or claim historical replay until one transaction and its state transition are independently verified.

## Sources

- https://docs.velocity.exchange/developers/data-api
- https://data.api.drift.trade/openapi.json
- Public Solana RPC for `dRiftyHA39MWEi3m9aunc5MzRF1JYuBsbn6VPcn33UH`
