# Blocksize VAT And BLS Readiness

Date: 2026-07-22

## Sources

- Official upgrade status: https://solana.com/upgrades/bls-pubkey-vat
- VAT feature account: https://explorer.solana.com/address/VAT9huvhPjRN9cyrPytq9rwvEJ3J4ADtjdncgZRyANJ/feature-gate?cluster=mainnet-beta
- Blocksize vote account: https://explorer.solana.com/address/HMk1qny4fvMnajErxjXG5kT89JKV4cx1PKa9zhQBF9ib?cluster=mainnet-beta

## Verified Snapshot

- VAT mainnet status: pending. The official page says BLS pubkeys are live and VAT is pending ahead of Agave 4.3; its detailed status still says VAT is not yet activated on mainnet.
- BLS registration: present for the Blocksize vote account.
- Compressed BLS pubkey: `6Q4cRD6c2BiFheEQ8xfnNqiLYYA9WE16hN9tC8brzauNCYy3eV97uAbFd1TmkWzoAA`.
- Vote status: current and voting.
- Commission: 5 percent.
- Activated stake: approximately 193,492.7404 SOL.
- Snapshot stake rank: approximately 290th among current vote accounts.

The snapshot used finalized public mainnet RPC. The vote account's JSON-parsed state exposed `blsPubkeyCompressed`; `getVoteAccounts` supplied current status and activated stake. Rank was calculated by sorting current vote accounts by activated stake.

## Conclusion

Blocksize is BLS-registered and currently well inside the prospective top-2,000 threshold. Because VAT is not active on mainnet, this is readiness and current stake-position evidence, not formal admission. Rank and eligibility remain epoch-dependent.

## Follow-Up

1. Monitor the VAT feature account for activation.
2. Recompute stake rank and current/delinquent status at each material network change.
3. Track validator client version and SFDP/delegation criteria alongside VAT readiness.
4. Package the read-only method as a validator-readiness brief without labeling other validators as dying.
