# Jupiter Source Authority Resolution

This is the founder/operator checklist for the remaining Jupiter Perps source-authority work. OPRS has resolved the canonical onchain Anchor IDL path for `Position` and `PositionRequest` account-layout decode. Johann or Blocksize only needs external Jupiter confirmation if we want to promote verified request/fulfillment lifecycle pairing or replay claims.

This checklist does not authorize production execution. All OPRS Jupiter work remains read-only and dry-run only unless a separate production-scope review is explicitly approved later.

## What Needs To Be Resolved

OPRS already has a reviewed onchain Anchor IDL extraction tied to the current live Jupiter Perps program for account-layout decode. The remaining source-authority need is Jupiter-controlled or source-reviewed evidence that ties request creation, fulfillment, closure, and final position state into a verifiable lifecycle.

Current live-program target:

```text
PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu
```

Resolved decode authority:

```text
Anchor IDL account: 38GK1i4cQPAxqrbfKX4RRMNfXpKRn5PgLFHVJeXm1C8Y
Normalized IDL SHA-256: 611de36592f4508438df16ebee2ff73b9789eda105ec712575d515b432d1ebaa
Public package: examples/public/jupiter-onchain-decode-v0/
```

The remaining key question:

```text
What is the canonical source of truth for Jupiter Perps instruction account roles, request/fulfillment lifecycle semantics, and public fixture signatures?
```

Until that evidence lands, OPRS must keep these claims blocked:

- verified request/fulfillment pairing
- Jupiter liquidation replay
- keeper execution verification
- replay readiness

## Acceptable Evidence

Any one of these paths can resolve the remaining lifecycle blocker if it clearly ties back to the live program ID:

1. Public Jupiter-confirmed instruction account-role maps for request creation, execution, rejection, cancellation, trigger, close, and fulfill flows.
2. Public mainnet fixture signatures supplied or confirmed by Jupiter, together with expected decoded account keys and before/after lifecycle state.
3. A Jupiter API endpoint that returns canonical account-role, lifecycle, or fixture metadata with stable versioning or a checksum.
4. Written confirmation from an official Jupiter route that a specific source/docs/API artifact is canonical for lifecycle semantics.

The evidence should answer the confirmation checklist in [Jupiter position authority confirmation](jupiter-position-authority-confirmation.md).

## What Johann Needs To Do

Nothing from Johann is required for account-layout decode anymore. I can continue read-only development using the local Helius-backed scripts and the hash-pinned onchain IDL.

For verified lifecycle pairing, Johann can help with the following:

1. Choose the outbound route.

   Good routes are an official Jupiter support/contact channel, a Jupiter Discord or Telegram with a core contributor, an official GitHub issue or discussion if Jupiter accepts those, or an email to a Jupiter protocol/devrel contact.

2. Send the prepared note.

   Use [Jupiter position authority outbound note](jupiter-position-authority-outbound.md). Send it as Johann / Blocksize. It is already scoped as open-source, read-only, and dry-run developer tooling.

3. Ask for a hashable answer.

   The most useful reply is not just "yes"; it is a link, commit, release, package, onchain IDL address, checksum, or stable API response that we can cite and pin in the proof pack.

4. Ask whether the Jupiter API key helps with lifecycle or fixture authority.

   The exact question is:

   ```text
   Does any Jupiter API-key-gated read-only endpoint return canonical instruction account-role maps, lifecycle metadata, or public fixture metadata for the live Perps program, and if so how should the response be versioned or hash-pinned?
   ```

5. Save only public-safe evidence.

   If Jupiter replies with a public link, paste the URL into the working task. If Jupiter replies privately, save a redacted text export or screenshot with date, channel, responder identity, and the relevant non-secret answer. Do not include API keys, private RPC URLs, wallet keys, private customer data, or anything Jupiter marks confidential.

6. Give Codex the evidence.

   Provide the public URL or redacted non-secret response. OPRS can then update the source-review records, provenance docs, local validators, and public proof-pack status.

## If You Want To Add The Jupiter API Key Locally

The API key is optional for lifecycle discovery. Add it only for local read-only discovery, and never paste it into chat.

From the repo root:

```bash
cd "/Users/johannfocke/Documents/Codex-Express Relay/open-perps-reliability-stack"
printf "Paste Jupiter API key: "
stty -echo
IFS= read -r JUPITER_API_KEY
stty echo
printf "\nJUPITER_API_KEY=%s\n" "$JUPITER_API_KEY" >> .env
unset JUPITER_API_KEY
echo "Saved JUPITER_API_KEY to .env"
```

This writes the key to local `.env` without printing it. Keep `.env` uncommitted.

## What Not To Do

- Do not paste the Jupiter API key into chat, GitHub, docs, or public issues.
- Do not ask for keeper credentials, signer access, trading permissions, custody access, private RPC URLs, or production order-routing access.
- Do not provide wallet private keys or local keypairs.
- Do not publish raw RPC payloads, raw account bytes, private channel logs, or confidential Jupiter replies.
- Do not treat an API key by itself as source authority.

## What Unlocks Next

After acceptable lifecycle evidence lands, OPRS can start a local-only verified-pairing experiment:

1. Hash-pin the role-map or fixture evidence.
2. Link request and fulfillment transactions through decoded public account roles.
3. Decode source-reviewed lifecycle fields for `Position` and `PositionRequest`.
4. Add local validators and synthetic negative fixtures.
5. Keep outputs under `target/` until scrub review passes.
6. Publish only a scrubbed proof-pack update after source-review approval.

Even after source authority lands, transaction submission, signing, keeper behavior, custody, capital deployment, and production execution remain out of scope.
