# Kamino Scope v0.38.0

Date: 2026-07-22

## Verified Change

Kamino Finance published the non-prerelease Scope `v0.38.0` release on July 10, 2026 at commit `0d7320b6eb603c00066d66ccc92ea89b1f2feb65`. Its release notes add a `PythLazerEMA` oracle type and more logs for error cases in `MostRecentOf`. The notes state that OtterSec audited the changes; the exact report and scope were not reviewed in this checkpoint.

DefiLlama's July 22 snapshot reported approximately $1.054B of Solana TVL and $927.6M borrowed for Kamino Lend. Those figures establish scale only under DefiLlama's definitions and may overlap with other protocol accounting.

## Blocksize Opportunity

A read-only Scope reliability package can normalize:

- Pyth Lazer spot and EMA timestamps;
- spot-versus-EMA divergence;
- source freshness and configured age limits;
- `MostRecentOf` source selection and fallback;
- observable error classes and incidence;
- pinned Scope release and configuration provenance.

The primitive is adjacent to OPRS because the same oracle-freshness, divergence, and fallback evidence applies to perps and other leveraged markets. The next evidence gate is verifying whether `v0.38.0` and `PythLazerEMA` appear in current mainnet configuration and whether the new errors are observable through public logs.

At the pinned release commit, both canonical files under `configs/mainnet` contain `PythLazer` and `MostRecentOf` entries but zero exact `PythLazerEMA` oracle-type entries. This is configuration-level negative evidence only: it separates released capability from committed use but does not establish current deployed account state. The remaining gate is current onchain configuration plus public transaction-log observability.

## Claim Boundary

Do not claim a Kamino relationship, Blocksize feed usage, mainnet adoption, an oracle incident, reviewed audit assurance, customer demand, or measured risk reduction.

## Sources

- https://github.com/Kamino-Finance/scope/releases/tag/release/v0.38.0
- https://github.com/Kamino-Finance/scope/tree/0d7320b6eb603c00066d66ccc92ea89b1f2feb65/configs/mainnet
- https://api.llama.fi/protocol/kamino-lend
