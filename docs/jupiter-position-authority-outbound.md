# Jupiter Position Authority Outbound Note

This is the founder-ready outbound note for asking Jupiter to confirm source authority. It should be sent only through an approved Jupiter contact, issue, Discord, Telegram, or email route. Sending the note does not change OPRS scope.

## Short DM

```text
Hi Jupiter team - we are building Open Perps Reliability Stack, an open-source read-only/dry-run developer tooling project for Solana perps reliability.

For Jupiter Perps, we currently use public docs only for target discovery and unverified lifecycle candidates. We are not claiming binary decode, verified request/fulfillment pairing, keeper execution, trading, signing, custody, or order submission.

Could Jupiter confirm the canonical source of truth for mainnet Jupiter Perps program `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu`, specifically the `PositionRequest` and `Position` account layouts and lifecycle semantics?

The exact ask is here:
https://github.com/jf-cmyk/open-perps-reliability-stack/blob/main/docs/jupiter-position-authority-confirmation.md
```

## Full Email

```text
Subject: Jupiter Perps source authority confirmation for open-source read-only tooling

Hi Jupiter team,

I am building Open Perps Reliability Stack, an open-source, read-only and dry-run developer tooling project for Solana perps reliability.

For Jupiter Perps, we currently use official docs only for target discovery and unverified lifecycle research. We do not claim binary account decoding, verified request/fulfillment pairing, keeper execution, liquidation replay, trading, signing, custody, order submission, or capital deployment.

Could Jupiter confirm the canonical source/IDL authority for the current mainnet Jupiter Perps program `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu`?

Specifically, we need to know whether there is a canonical source, IDL, package, release, onchain IDL address, or other hashable artifact that defines the live `Position` and `PositionRequest` account layouts and lifecycle semantics.

The confirmation checklist is:

1. Confirm `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu` is the current live Jupiter Perps program ID for this proof.
2. Provide the canonical IDL/source repo, package, release, or onchain IDL address.
3. Provide a commit/release/hash tying that IDL/source to the live program.
4. Confirm `Position` account discriminator, account size, field order/types/offsets, enum layouts, and PDA seeds.
5. Confirm `PositionRequest` account discriminator, account size, field order/types/offsets, enum layouts, PDA seeds, bump encoding, and counter/random-seed encoding.
6. Confirm instruction account-role maps for create/open/increase/decrease/close/cancel/reject/execute/fulfill flows.
7. Confirm whether a request transaction and fulfillment transaction can be verified by a shared decoded `PositionRequest` account.
8. Confirm how the final `Position` account should be linked to the request lifecycle, if applicable.
9. Confirm `PositionRequestATA` or equivalent token-account roles in deposit/withdraw flows.
10. Confirm non-TP/SL execution/closure semantics, including how `executed` should be interpreted.
11. Confirm TP/SL persistence, trigger, and closure semantics if different from ordinary requests.
12. Share one or more public mainnet signature pairs with expected account keys and decoded before/after state for regression fixtures, if available.
13. Flag any keeper-only, internal, temporary, deprecated, or otherwise unsafe accounts that should not be interpreted publicly.

We will keep all live reads read-only, keep raw payloads out of public artifacts, and mark any unconfirmed evidence as source-authority blocked.

Repository reference:
https://github.com/jf-cmyk/open-perps-reliability-stack

Confirmation checklist:
https://github.com/jf-cmyk/open-perps-reliability-stack/blob/main/docs/jupiter-position-authority-confirmation.md
```

## Follow-Up Tracker

Before sending:

- Confirm the contact route.
- Confirm whether to send as Johann/Blocksize.
- Confirm whether to mention Solana Foundation grant review.
- Do not paste private RPC URLs, `.env` values, signatures from private runs, or non-public research outputs.

After sending:

- Record date, route, and public-safe summary in a source-review record.
- Keep Jupiter decode and verified pairing blocked until a hashable source or explicit written confirmation is received.
- Update `docs/jupiter-source-authority-audit.md`, `docs/jupiter-perps-provenance.md`, and `examples/public/jupiter-authority-gap-v0/gap_report.json` only after confirmation.

