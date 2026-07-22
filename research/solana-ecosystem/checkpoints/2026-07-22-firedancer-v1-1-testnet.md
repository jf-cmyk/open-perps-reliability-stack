# Firedancer v1.1 Testnet Milestone

Observed: 2026-07-22

## Verified

Firedancer v1.1.0 was published July 15, 2026 and is explicitly labeled a testnet release not suggested for Mainnet Beta. Its release notes describe a new accounts database, memory consumption reduced to approximately 350 GiB, a repair server, XDP busy polling, improved DoubleZero/GRE tunnel support, and support for Agave v4.2 feature gates including shorter slots. The July 16 v1.1.1 patch remains testnet-only and fixes incorrectly reported version information.

Sources:

- https://github.com/firedancer-io/firedancer/releases/tag/v1.1.0
- https://github.com/firedancer-io/firedancer/releases/tag/v1.1.1

## Blocksize And OPRS Implication

Transport and execution-reliability tests must distinguish full Firedancer v1.1.x testnet from Frankendancer v0.1006.40100, which the project labels mainnet-ready. Client, release, deployment stage, accounts implementation, memory, XDP mode, route table, GRE tunnels, slot timing, and public-internet control are separate benchmark dimensions. This is relevant to Blocksize's verified historical DoubleZero use but does not establish its current client or participation in Firedancer testing.

## Claim Boundary

Do not claim mainnet recommendation or activation, Blocksize deployment, reproduced memory reduction, improved DoubleZero performance, production readiness, or direct comparability with Frankendancer without controlled measurements.

## Next Action

Confirm Blocksize's current client/version and any testnet test posture. Design separate, read-only benchmark matrices for Frankendancer mainnet-ready and full Firedancer testnet paths before attributing transport or execution gains.
