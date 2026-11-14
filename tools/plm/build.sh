#!/usr/bin/env bash
# Gera o pacote de liberação do PS-001: PDFs (pandoc -> typst), BOM e renders,
# com manifesto sha256. Ver docs/plm/PLANO.md §6.
#
#   tools/plm/build.sh            # tudo (PDF, BOM e renders já copiados)
#   tools/plm/build.sh --pdf      # só os PDFs
#   tools/plm/build.sh --clean    # limpa dist/ antes
#
# Saída: dist/v<versao>/  (fora do git)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

VERSION="$(sed -n 's/.*\*\*Versão:\*\* \([0-9][0-9.]*\).*/\1/p' README.md | head -1)"
VERSION="${VERSION:-0.0.0}"
OUT="dist/v${VERSION}"
BUILD="$OUT/.build"

ONLY_PDF=0
for arg in "$@"; do
  case "$arg" in
    --pdf) ONLY_PDF=1 ;;
    --clean) rm -rf dist; echo "dist/ limpo" ;;
    *) echo "argumento desconhecido: $arg" >&2; exit 2 ;;
  esac
done

command -v pandoc >/dev/null || { echo "pandoc não encontrado" >&2; exit 1; }
command -v typst  >/dev/null || { echo "typst não encontrado"  >&2; exit 1; }

mkdir -p "$BUILD"

# código do documento | fonte | slug | título
DOCS=(
  "PS-001-PL-001|docs/plm/PLANO.md|plano-plm"
  "PS-001-PL-002|docs/plm/REGISTRO.md|registro-documentos"
  "PS-001-US-001|docs/uso/USO.md|uso"
  "PS-001-CO-001|docs/construcao/CONSTRUCAO.md|construcao"
)

echo "PS-001 · pacote $VERSION"
echo "  destino: $OUT"

# ------------------------------------------------------------------ renders
if [ "$ONLY_PDF" -eq 0 ]; then
  mkdir -p "$OUT/renders"
  src_dir="out/plot/v${VERSION//./}"
  if [ ! -d "$src_dir" ]; then
    # aceita o conjunto mais recente
    src_dir="$(ls -d out/plot/v* 2>/dev/null | sort -V | tail -1 || true)"
  fi
  if [ -n "${src_dir:-}" ] && [ -d "$src_dir" ]; then
    n=0
    for f in "$src_dir"/*.png; do
      [ -e "$f" ] || continue
      base="$(basename "$f")"
      cp "$f" "$OUT/renders/PS-001_${base%.png}_rA.png"
      n=$((n + 1))
    done
    echo "  renders: $n de $src_dir"
  else
    echo "  renders: nenhum em out/plot (siga sem imagens)" >&2
  fi
fi

# --------------------------------------------------------------------- BOM
if [ "$ONLY_PDF" -eq 0 ]; then
  cp docs/construcao/BOM.csv "$OUT/PS-001-LM-001_rA_bom.csv"
  echo "  BOM: PS-001-LM-001_rA_bom.csv"
fi

# ----------------------------------------------------------------- desenho
# prancha A2 verificada (ocs_audit + save_verified), nunca a de trabalho
if [ "$ONLY_PDF" -eq 0 ]; then
  dr="$(ls -t out/draw/v*/PS-001-DR-001_rA_prancha-a2.pdf 2>/dev/null | head -1 || true)"
  if [ -n "${dr:-}" ]; then
    cp "$dr" "$OUT/$(basename "$dr")"
    dxf="${dr%.pdf}.dxf"
    [ -f "$dxf" ] && cp "$dxf" "$OUT/$(basename "$dxf")"
    echo "  desenho: $(basename "$dr") ($(dirname "$dr"))"
  else
    echo "  desenho: nenhum PS-001-DR-001 em out/draw (siga sem a prancha)" >&2
  fi
fi

# -------------------------------------------------------------------- PDFs
for entry in "${DOCS[@]}"; do
  IFS='|' read -r code src slug <<<"$entry"
  [ -f "$src" ] || { echo "  falta a fonte: $src" >&2; continue; }
  rev="$(sed -n 's/^revision: *"\(.*\)"/\1/p' "$src" | head -1)"
  rev="${rev:-A}"

  # figura ausente não quebra a build: vira nota visível no PDF
  md="$BUILD/$code.md"
  python3 - "$src" "$md" "$OUT" <<'PY'
import os, re, sys

src, dst, base = sys.argv[1], sys.argv[2], sys.argv[3]
text = open(src, encoding="utf-8").read()

def fix(m):
    path = m.group(1).strip()
    if os.path.exists(path) or os.path.exists(os.path.join(base, path)):
        return m.group(0)
    print("  aviso: figura ausente " + path)
    return "> _(figura `" + path + "` indisponível nesta build)_"

open(dst, "w", encoding="utf-8").write(
    re.sub(r"!\[[^\]]*\]\(([^)]+)\)(?:\{[^}]*\})?", fix, text)
)
PY

  typ="$OUT/.$code.typ"
  pdf="$OUT/${code}_r${rev}_${slug}.pdf"
  pandoc "$md" -t typst --template=tools/plm/template.typ -o "$typ"
  typst compile --root . "$typ" "$pdf"
  rm -f "$typ"
  echo "  PDF: $(basename "$pdf")"
done

# --------------------------------------------------------------- manifesto
cd "$OUT"
find . -maxdepth 2 -type f ! -path "./.build/*" ! -name MANIFEST.md ! -name SHA256SUMS \
  -printf '%P\n' | sort | xargs -d '\n' sha256sum > SHA256SUMS

{
  echo "# Pacote de liberação — PS-001 v${VERSION}"
  echo
  echo "- Gerado em: $(date -Iminutes)"
  echo "- Commit: \`$(git rev-parse --short HEAD 2>/dev/null || echo 'sem git')\`"
  echo "- Branch: \`$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '-')\`"
  echo "- Modelo: \`cad/solidcraft/PS-001.sc\`"
  echo
  echo "| Arquivo | Bytes |"
  echo "|---|---:|"
  while read -r hash f; do
    printf '| `%s` | %s |\n' "${f#\*}" "$(stat -c%s "${f#\*}")"
  done < SHA256SUMS
  echo
  echo "## Verificação"
  echo
  echo '```sh'
  echo "cd dist/v${VERSION} && sha256sum -c SHA256SUMS"
  echo '```'
  echo
  echo "O pacote só vale para o commit acima: PDF regerado a partir de outro"
  echo "estado não corresponde a esta liberação. Arquivos derivados não são"
  echo "versionados (ver docs/plm/PLANO.md §6)."
} > MANIFEST.md
cd "$ROOT"

rm -rf "$BUILD"
echo "  manifesto: MANIFEST.md"
echo "ok"
