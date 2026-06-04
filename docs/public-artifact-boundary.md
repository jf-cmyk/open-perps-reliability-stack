# Public Artifact Boundary

The Railway proof-pack site is a reviewer-facing static artifact. It should contain only materials that help an external reviewer understand, run, or evaluate the read-only and dry-run MVP.

## Served On Railway

- Proof-pack index.
- Static dashboard.
- Grant proposal and public docs.
- Architecture, adapter, data model, dry-run, and boundary docs.
- Public schemas.
- Sample datasets.
- Public API examples.
- Local proposal deliverable.

## Kept In GitHub Only

These files remain part of the OSS repo but are not served from the Railway proof-pack image:

- `docs/checkpoints/`

Checkpoint docs are project memory for development continuity. They may include local paths, resume prompts, agent state, and operational notes that are useful to maintainers but unnecessary for grant reviewers.

GitHub Pages uses the same public-artifact boundary through `scripts/build_public_artifact.sh`, so it should not serve `docs/checkpoints/`, deployment config files, `.env.example`, or Word lock files.

## Never Serve Or Commit

- `.env` or `.env.*`
- RPC URLs or API keys
- bearer tokens
- private keys
- seed phrases
- wallet files
- signer, custody, capital, or execution settings
- private routing or strategy notes

## Reviewer Link Rule

Any link from the proof-pack homepage must point to an artifact that is safe for public review and available inside the Railway image. Internal project-memory links belong in the GitHub repo, not the proof-pack homepage.
