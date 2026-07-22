# Termina Replay API Fit

Date: 2026-07-22

## Verified Surface

Termina's public API reference documents:

- historical slot-range discovery;
- API-key-authenticated WebSocket session control;
- sequence IDs that support reconnect and resume;
- per-session Solana-like HTTP and WebSocket RPC;
- account, program, transaction, log, and subscription reads;
- transaction simulation, session-scoped execution, account overrides, and slot advancement.

The archive is described as proprietary, and the documentation requires callers to check whether a requested slot range is available. The public surface does not establish pricing, complete historical coverage, protocol-specific support, or independent reproduction of Termina's fidelity claims.

## Simulation Provenance Boundary

The current quickstart documents a fixed per-slot order: historical block transactions execute first, followed by custom RPC transactions and then custom transactions supplied with `continue`. It also permits account-state overrides and explicitly disables signature checks, allowing simulated transactions to originate from any account.

OPRS must therefore preserve separate evidence classes: canonical public onchain signer and state evidence; historical replay output; and counterfactual output produced with custom transactions, spoofable account origins, or state overrides. The latter can test protocol behavior but cannot establish authorization or historical signer behavior.

## OPRS Fit

Termina can potentially supply historical state and a controlled simulation environment while OPRS supplies pinned Drift semantics, event interpretation, deterministic expected outputs, and a source-backed proof pack. The smallest validation design maps one public Drift liquidation signature to:

1. range availability;
2. session creation and resumability;
3. pre-event account reads;
4. transaction and log retrieval;
5. deterministic replay or simulation output;
6. comparison with canonical onchain results and OPRS interpretation.

No API call, outreach, signing, or execution is part of this research checkpoint. A future test remains blocked pending separately approved non-production access.

## Claim Boundary

Do not claim a partnership, access, public pricing, complete archive coverage, Drift/Phoenix/Jupiter compatibility, 1:1 fidelity, reproducibility, authorization, historical signer behavior from simulated transactions, or production readiness. The verified conclusion is limited to the documented API surface and its architectural complementarity with OPRS.

## Sources

- https://docs.termina.technology/documentation/tech-setup-guide/api-reference
- https://docs.termina.technology/documentation/tech-setup-guide/quickstart
- https://www.termina.technology/
