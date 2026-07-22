# Epicentral SOS / OPX Verification

Observed: 2026-07-22

Sources:

- https://www.epicentrallabs.com/dao
- https://github.com/EpicentralLabs/docs-v2/commit/59891deab0654846d1d851965f4a7d498549203c

## Result

| Question | Result |
| --- | --- |
| Documented? | Yes. Public docs describe OPX workflows, historical-volatility Black-Scholes pricing, collateral, margin liquidity, and fee design. |
| Live on mainnet? | Unverified and internally contradictory. Terms describe autonomous programs deployed on Solana, while the fee page says schedules remain illustrative pending mainnet launch. |
| Open source? | Not verified. The public GitHub organization contains docs and supporting tools but no identifiable OPX/SOS program or SDK repository. |
| Audited? | Not verified. No OPX audit report, auditor, commit scope, date, or remediation record was found. |
| Program IDs? | Not found in the reviewed official docs. |
| Oracle dependencies? | No named OPX oracle provider was found; the docs mention generic oracle risk. |

"Not found" refers only to the official public sources reviewed in this bounded run. It does not prove that private or unpublished artifacts do not exist.

## Decision

Defer `OPP-009`. Reconsider only when Epicentral publishes:

- canonical mainnet program IDs and transaction evidence;
- official program and SDK repositories with licenses and pinned commits;
- named oracle and external-liquidity dependencies;
- an audit report tied to deployed code, including scope and remediation status.

## Blocksize / OPRS Implication

The documented pricing, collateral, expiry, exercise, and liquidity concepts could eventually support an options reliability adapter. They should remain post-MVP research and outside the current Open Perps grant narrative until the deployment and security evidence is independently reproducible.

## Grant Safety

Do not characterize OPX or SOS as live, production-ready, open source, audited, or secure from the current evidence.
