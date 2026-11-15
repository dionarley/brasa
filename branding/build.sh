#!/usr/bin/env bash
# Regenera os exports do logo Brasa a partir dos documentos VectorCraft.
#
#   branding/build.sh            # SVG (texto em curvas) + PNG
#   branding/build.sh --check    # só confere se os exports batem com as fontes
#
# Fontes: brasa-wide.vectorcraft (600 x 120 px) e brasa-square.vectorcraft
# (256 x 256 px). O SVG leva o texto em curvas (--outline-text) para não depender
# da fonte DejaVu Sans no navegador; o PNG sai a 72 ppi, 1 px por ponto.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

APP=ai.storyteller.vectorcraft
vc() { flatpak run --command=vectorcraft-cli "$APP" "$@"; }

command -v flatpak >/dev/null || { echo "flatpak não encontrado" >&2; exit 1; }
flatpak info "$APP" >/dev/null 2>&1 || { echo "$APP não instalado" >&2; exit 1; }

tmp="$PWD/.build"
rm -rf "$tmp"; mkdir -p "$tmp"
trap 'rm -rf "$tmp"' EXIT

for name in brasa-wide brasa-square; do
  vc convert "$name.vectorcraft" "$tmp/$name.svg" --outline-text >/dev/null
  vc convert "$name.vectorcraft" "$tmp/$name.png" --ppi 72 >/dev/null
  if [ "${1:-}" = "--check" ]; then
    for ext in svg png; do
      cmp -s "$tmp/$name.$ext" "$name.$ext" \
        && echo "ok   $name.$ext" \
        || { echo "difere $name.$ext (rode build.sh)" >&2; exit 1; }
    done
  else
    mv "$tmp/$name.svg" "$name.svg"
    mv "$tmp/$name.png" "$name.png"
    echo "gerado $name.svg e $name.png"
  fi
done
