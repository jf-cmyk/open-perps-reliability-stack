# BlazeStake Blocksize Eligibility

Observed: 2026-07-22

## Finding

BlazeStake's public Custom Liquid Staking API returned 1,292 eligible validators and included Blocksize vote account `HMk1qny4fvMnajErxjXG5kT89JKV4cx1PKa9zhQBF9ib`. BlazeStake documents CLS as directing stake to a selected validator while maintaining a 1:1 relationship with bSOL controlled by the user, including supported DeFi positions.

The public Custom Validators page also lists `BLOCKSIZE`, links to Blocksize's Solana validator page, and exposes a Stake action. That action resolves to `/app/?validator=HMk1qny4fvMnajErxjXG5kT89JKV4cx1PKa9zhQBF9ib` and renders `Support BLOCKSIZE`, verifying the public user path and identity binding without connecting a wallet or invoking a transaction.

## Target Versus Applied Stake

The developer documentation exposes `cls_user_target`, keyed by user address, and returns target allocations by validator vote account. It warns that target calculations may lag by up to one epoch and may not be applied exactly if the user does not control enough bSOL to back them. No aggregate per-validator CLS target or realized-balance endpoint is documented.

The same page documents `cls_stake` and `cls_unstake` transaction-submission endpoints. This research did not call them and does not need to: any balance or retention evidence must remain read-only and distinguish user target state from realized onchain delegation.

## Blocksize Opportunity

Blocksize may already have a user-directed liquid-staking route without launching a bespoke LST. A read-only surface could expose eligibility, validator performance, bSOL coverage, and delegation retention, and compare this path with native delegation and a potential Sanctum LST.

## Claim Boundary

API membership and the selector establish eligibility and public interface visibility only. A user target does not establish applied stake, and the documented endpoint cannot by itself establish an aggregate Blocksize balance. Public evidence does not yet establish deposits, delegated balance, users, fees, revenue, continuing eligibility, endorsement, current endpoint behavior, or partnership.

## Sources

- https://stake.solblaze.org/api/v1/cls_eligible_validators
- https://stake.solblaze.org/validators
- https://stake.solblaze.org/app/?validator=HMk1qny4fvMnajErxjXG5kT89JKV4cx1PKa9zhQBF9ib
- https://stake-docs.solblaze.org/features/custom-liquid-staking
- https://stake-docs.solblaze.org/developers/custom-liquid-staking-apis
