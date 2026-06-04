#!/usr/bin/env bash
set -euo pipefail

outdir="${1:-public-proof-pack}"

if [ -e "$outdir" ]; then
  echo "Output path already exists: $outdir" >&2
  echo "Choose a fresh output path so stale files cannot leak into the public artifact." >&2
  exit 1
fi

mkdir -p "$outdir"

cp index.html README.md LICENSE "$outdir/"
cp -R apps datasets examples schemas "$outdir/"

mkdir -p "$outdir/docs"
for path in docs/*; do
  case "$path" in
    docs/checkpoints)
      ;;
    *)
      cp -R "$path" "$outdir/docs/"
      ;;
  esac
done

mkdir -p "$outdir/deliverables"
for path in deliverables/*; do
  base="$(basename "$path")"
  case "$base" in
    '~$'*)
      ;;
    *)
      cp -R "$path" "$outdir/deliverables/"
      ;;
  esac
done

echo "Built public proof-pack artifact at $outdir"
