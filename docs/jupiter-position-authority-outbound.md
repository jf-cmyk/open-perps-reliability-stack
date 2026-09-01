# Jupiter Position Authority Outbound Note

This is the founder-ready outbound note for asking Jupiter to confirm lifecycle and fixture authority. OPRS has already resolved account-layout decode through the live onchain Anchor IDL, so this note is only needed before promoting verified request/fulfillment pairing or replay claims. It should be sent only through an approved Jupiter contact, issue, Discord, Telegram, or email route. Sending the note does not change OPRS scope.

## Short DM

```text
Hi Jupiter team - we are building Open Perps Reliability Stack, an open-source read-only/dry-run developer tooling project for Solana perps reliability.

For Jupiter Perps, we use public docs and the live onchain Anchor IDL for read-only target discovery and scrubbed account-layout decode. We are not claiming verified request/fulfillment pairing, keeper execution, trading, signing, custody, order submission, or replay readiness.

Could Jupiter confirm the canonical source of truth for mainnet Jupiter Perps program `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu`, specifically instruction account roles, `PositionRequest` lifecycle semantics, request/fulfillment linkage, and public fixture signatures?

If the current Jupiter API exposes an authenticated read-only endpoint for role-map, lifecycle, or fixture metadata, could you also confirm the endpoint and whether its response is canonical and hashable? An API key alone will not be treated as source authority unless it returns or references a Jupiter-confirmed artifact tied to the live program.

The exact ask is here:
https://github.com/jf-cmyk/open-perps-reliability-stack/blob/main/docs/jupiter-position-authority-confirmation.md
```

## Full Email

```text
Subject: Jupiter Perps lifecycle confirmation for open-source read-only tooling

Hi Jupiter team,

I am building Open Perps Reliability Stack, an open-source, read-only and dry-run developer tooling project for Solana perps reliability.

For Jupiter Perps, we use official docs and the live onchain Anchor IDL for target discovery and scrubbed account-layout decode. We do not claim verified request/fulfillment pairing, keeper execution, liquidation replay, trading, signing, custody, order submission, or capital deployment.

Could Jupiter confirm the canonical lifecycle authority for the current mainnet Jupiter Perps program `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu`?

Specifically, we need to know whether there is a canonical source, docs page, package, release, API response, or other hashable artifact that defines instruction account roles, request/fulfillment lifecycle semantics, and expected public fixture signatures for live `Position` and `PositionRequest` flows.

We may be able to use a Jupiter API key for authenticated read-only discovery, but we will not treat authenticated access by itself as authority. If a Jupiter API endpoint returns canonical account-role, lifecycle, or public fixture metadata, please confirm the endpoint, response shape, and hash/checksum or versioning rule that ties it to the live program.

The confirmation checklist is:

1. Confirm `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu` is the current live Jupiter Perps program ID for this proof.
2. Confirm whether onchain IDL account `38GK1i4cQPAxqrbfKX4RRMNfXpKRn5PgLFHVJeXm1C8Y` is acceptable account-layout authority, or point us to the preferred replacement if not.
3. Confirm instruction account-role maps for create/open/increase/decrease/close/cancel/reject/execute/fulfill flows.
4. Confirm whether a request transaction and fulfillment transaction can be verified by a shared decoded `PositionRequest` account.
5. Confirm how the final `Position` account should be linked to the request lifecycle, if applicable.
6. Confirm `PositionRequestATA` or equivalent token-account roles in deposit/withdraw flows.
7. Confirm non-TP/SL execution/closure semantics, including how `executed` should be interpreted.
8. Confirm TP/SL persistence, trigger, and closure semantics if different from ordinary requests.
9. Share one or more public mainnet signature pairs with expected account keys and decoded before/after state for regression fixtures, if available.
10. Flag any keeper-only, internal, temporary, deprecated, or otherwise unsafe accounts that should not be interpreted publicly.
11. Confirm whether any Jupiter API-key-gated endpoint is canonical for role-map/lifecycle/fixture metadata, and if so, how OPRS should hash-pin or version that response.

We will keep all live reads read-only, keep raw payloads out of public artifacts, and mark any unconfirmed lifecycle evidence as candidate-only.

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
- Do not send or paste the Jupiter API key; ask only whether an authenticated read-only schema/IDL/source endpoint exists.
- Do not paste private RPC URLs, `.env` values, signatures from private runs, or non-public research outputs.

After sending:

- Record date, route, and public-safe summary in a source-review record.
- Keep verified pairing and replay blocked until a hashable source or explicit written confirmation is received.
- Update `docs/jupiter-source-authority-audit.md`, `docs/jupiter-perps-provenance.md`, and `examples/public/jupiter-authority-gap-v0/gap_report.json` only after confirmation.
