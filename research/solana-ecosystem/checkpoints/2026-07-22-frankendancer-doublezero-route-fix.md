# Frankendancer DoubleZero Route Fix

Observed: 2026-07-22

## Verified Fact

Firedancer labels Frankendancer `v0.1006.40100`, published July 14, 2026, as mainnet-ready. Its release notes say it fixes outgoing packet loss with large route tables and name DoubleZero as an example. The official five-commit comparison includes a route-update change that replicates routing tables to net tiles through message passing and an XDP change supporting up to four GRE tunnels.

Sources:

- https://github.com/firedancer-io/firedancer/releases/tag/v0.1006.40100
- https://github.com/firedancer-io/firedancer/compare/v0.1005.40100...v0.1006.40100

## Blocksize Implication

Any controlled DoubleZero transport benchmark should record the validator client, exact release, route-table state, GRE configuration, packet drops, route-update timing, latency, jitter, shred gaps, and transaction landing outcomes. Results should be stratified by client version before attributing an effect to DoubleZero or the public-internet control.

## Evidence Boundary

The release does not show that Blocksize uses Frankendancer, ran an affected version, experienced packet loss, deployed the fix, or obtained a performance improvement. It also does not establish a DoubleZero network fault. Those points require current Blocksize configuration evidence and a controlled read-only benchmark.

## Next Action

Verify Blocksize's current validator client/version and DoubleZero connectivity. If Frankendancer is relevant, include pre/post-`v0.1006.40100` client cohorts or otherwise hold the client version constant in the benchmark.
