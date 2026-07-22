# SFDP Criteria Snapshot

Observed: 2026-07-22

Sources:

- https://solana.org/delegation-criteria
- https://solana.org/delegation-dashboard

## Epoch 1003 Mainnet Criteria

- Vote credits: at least 97% of cluster average.
- Validator commission: at most 5%.
- Jito MEV commission: at most 10%.
- Client minimum: Agave 4.1.0-rc.1 or Frankendancer 0.1004.0-rc.40101.
- ASN/company concentration: at most 25%.
- Data-center concentration: at most 15%.
- Total stake: at most 1,000,000 SOL.
- Testnet: baseline in five of the latest ten epochs.
- Metric reporting: mainnet and testnet reporting in eight of ten epochs.
- Responsiveness: within 24 hours.
- Matching skip rate: no more than five percentage points above the cluster average over five epochs.

## Transaction Processing

SFDP requires FIFO or prioritization-fee ordering within a 50ms window, shred release every 50ms or when a full erasure batch is ready, no TPU censorship, and no TPU delay beyond the allowed batch window.

## Program Snapshot

The epoch 1003 dashboard reported 364 validators receiving approximately 20.95M SOL of Foundation stake, representing 4% of total staked SOL, across 59 locations and 25 countries.

## Forward Software Schedule And Blocksize Check

The Foundation's public required-versions API returned mainnet epochs 1005-1008 with minimum Agave `4.1.0-rc.1` and Firedancer `0.1004.0-rc.40101`, inherited from the prior epoch. The criteria page lists testnet epochs 992-993 at Agave `4.2.0-beta.0` and Firedancer `0.1005.40100`, then advances epochs 994-995 to Agave `4.2.0-beta.2` and the listed Firedancer version `0.1102.0-beta.40201`.

The public SFDP participant API returned no row whose `mainnetBetaPubkey` matched Blocksize vote account `HMk1qny4fvMnajErxjXG5kT89JKV4cx1PKa9zhQBF9ib`. This is an API snapshot non-match only. It does not establish rejection, ineligibility, absence of Foundation stake, or that Blocksize has no separately registered identity.

## Blocksize Implication

This supports an epoch-versioned, read-only validator readiness product: criteria schemas, evidence provenance, threshold alerts, concentration and client context, and transaction-processing posture. Blocksize's known 5% commission and sub-1M SOL stake are only two inputs; full SFDP eligibility is not established.

## Grant Safety

Criteria, required versions, and dashboard values change by cluster and epoch. Do not claim Blocksize participation, rejection, eligibility, compliance, or future delegation without resolving identity mapping and validator-specific evidence for every requirement.

Additional source:

- https://api.solana.org/api/community/v1/sfdp_required_versions?cluster=mainnet-beta
- https://api.solana.org/api/community/v1/sfdp_participants
