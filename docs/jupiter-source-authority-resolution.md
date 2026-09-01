# Jupiter Source Authority Resolution

This is the founder/operator checklist for resolving the Jupiter Perps source-authority blocker. It explains exactly what Johann or Blocksize needs to obtain before OPRS can move Jupiter beyond target discovery and unverified lifecycle candidates.

This checklist does not authorize production execution. All OPRS Jupiter work remains read-only and dry-run only unless a separate production-scope review is explicitly approved later.

## What Needs To Be Resolved

OPRS needs Jupiter-controlled evidence that ties the current live Jupiter Perps program to the account layouts and lifecycle semantics we would decode.

Current live-program target:

```text
PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu
```

The key question:

```text
What is the canonical source of truth for the live Jupiter Perps Position and PositionRequest account layouts, instruction account roles, and request/fulfillment lifecycle semantics?
```

Without that evidence, OPRS must keep these claims blocked:

- Jupiter binary `Position` decode
- Jupiter binary `PositionRequest` decode
- verified request/fulfillment pairing
- Jupiter liquidation replay
- keeper execution verification
- replay readiness

## Acceptable Evidence

Any one of these paths can resolve the blocker if it clearly ties back to the live program ID:

1. A public Jupiter-confirmed IDL, source repository, package, release, or docs page with a stable hash, commit, version, or checksum.
2. A Jupiter-confirmed onchain/program-IDL extraction path, including the onchain IDL address and a hashable extracted artifact.
3. Written confirmation from an official Jupiter route that a specific docs-linked IDL/source candidate is canonical for the current live program.
4. A Jupiter API endpoint that returns canonical schema, IDL, source-revision, program-metadata, or fixture metadata with stable versioning or a checksum.
5. Public mainnet fixture signatures supplied or confirmed by Jupiter, together with expected decoded account keys and before/after lifecycle state.

The evidence should answer the confirmation checklist in [Jupiter position authority confirmation](jupiter-position-authority-confirmation.md).

## What Johann Needs To Do

1. Choose the outbound route.

   Good routes are an official Jupiter support/contact channel, a Jupiter Discord or Telegram with a core contributor, an official GitHub issue or discussion if Jupiter accepts those, or an email to a Jupiter protocol/devrel contact.

2. Send the prepared note.

   Use [Jupiter position authority outbound note](jupiter-position-authority-outbound.md). Send it as Johann / Blocksize. It is already scoped as open-source, read-only, and dry-run developer tooling.

3. Ask for a hashable answer.

   The most useful reply is not just "yes"; it is a link, commit, release, package, onchain IDL address, checksum, or stable API response that we can cite and pin in the proof pack.

4. Ask whether the Jupiter API key helps with source authority.

   The exact question is:

   ```text
   Does any Jupiter API-key-gated read-only endpoint return canonical schema, IDL, source-revision, program-metadata, or public fixture metadata for the live Perps program, and if so how should the response be versioned or hash-pinned?
   ```

5. Save only public-safe evidence.

   If Jupiter replies with a public link, paste the URL into the working task. If Jupiter replies privately, save a redacted text export or screenshot with date, channel, responder identity, and the relevant non-secret answer. Do not include API keys, private RPC URLs, wallet keys, private customer data, or anything Jupiter marks confidential.

6. Give Codex the evidence.

   Provide the public URL or redacted non-secret response. OPRS can then update the source-review records, provenance docs, local validators, and public proof-pack status.

## If You Want To Add The Jupiter API Key Locally

The API key is optional for resolving source authority. Add it only for local read-only discovery, and never paste it into chat.

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

After acceptable evidence lands, OPRS can start a local-only Jupiter decode experiment:

1. Hash-pin the source/IDL/schema evidence.
2. Decode only discriminator and account length first.
3. Decode source-reviewed identity and lifecycle fields for `Position` and `PositionRequest`.
4. Add local validators and synthetic negative fixtures.
5. Keep outputs under `target/` until scrub review passes.
6. Publish only a scrubbed proof-pack update after source-review approval.

Even after source authority lands, transaction submission, signing, keeper behavior, custody, capital deployment, and production execution remain out of scope.
