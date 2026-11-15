#!/usr/bin/env bash
# Instala o GridCraft no podman: baixa o pacote oficial, confere a assinatura e
# os checksums, extrai o site estático e a CLI, constrói a imagem da CLI e sobe
# o serviço web.
#
#   tools/gridcraft/install.sh              # versão fixada abaixo, porta 8088
#   tools/gridcraft/install.sh --no-cli     # só o site
#   GRIDCRAFT_VERSION=0.20.0 tools/gridcraft/install.sh
#
# A assinatura é conferida com a chave de release do projeto e o fingerprint
# fixado em FINGERPRINT; sem `gpg`, cai para o SHA256SUMS.txt (HTTPS).
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

VERSION="${GRIDCRAFT_VERSION:-0.19.1}"
PORT="${GRIDCRAFT_PORT:-8088}"
REPO="storytold/gridcraft"
# Chave de release do GridCraft (release-signing-key.asc), impressão digital
# completa da chave principal.
FINGERPRINT="2B76741B414AAD6CD33E631213A005C0B9D7C3ED"

WITH_CLI=1
while [ $# -gt 0 ]; do
  case "$1" in
    --no-cli)  WITH_CLI=0; shift ;;
    --port)    PORT="${2:?--port exige um número}"; shift 2 ;;
    --version) VERSION="${2:?--version exige uma versão}"; shift 2 ;;
    -h|--help) sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *)         echo "argumento inesperado: $1" >&2; exit 2 ;;
  esac
done

case "$(uname -m)" in
  x86_64)        ARCH=x86_64 ;;
  aarch64|arm64) ARCH=aarch64 ;;
  *) echo "arquitetura $(uname -m) sem pacote Linux oficial" >&2; exit 1 ;;
esac

BASE="https://github.com/$REPO/releases/download/v$VERSION"
ZIP="gridcraft-web-$VERSION.zip"
TARBALL="gridcraft-$VERSION-linux-$ARCH.tar.gz"
CACHE=".cache"

for tool in curl sha256sum tar unzip podman; do
  command -v "$tool" >/dev/null || { echo "falta $tool" >&2; exit 1; }
done
podman-compose version >/dev/null 2>&1 || { echo "falta podman-compose" >&2; exit 1; }

tmp=""
gnupg=""
cleanup() {
  [ -n "$tmp" ] && rm -rf "$tmp"
  [ -n "$gnupg" ] && rm -rf "$gnupg"
  return 0
}
trap cleanup EXIT

mkdir -p "$CACHE" bin ../../workbooks
echo "GridCraft $VERSION ($ARCH) · porta $PORT"

fetch() {
  local url="$1" dest="$2"
  if [ -s "$dest" ]; then
    echo "  já baixado: $(basename "$dest")"
    return 0
  fi
  echo "  baixando $(basename "$dest")…"
  curl -fsSL --retry 3 -o "$dest.part" "$url"
  mv "$dest.part" "$dest"
}

fetch "$BASE/SHA256SUMS.txt" "$CACHE/SHA256SUMS.txt"
fetch "$BASE/$ZIP" "$CACHE/$ZIP"
if [ "$WITH_CLI" = 1 ]; then
  fetch "$BASE/$TARBALL" "$CACHE/$TARBALL"
fi

echo "  conferindo a assinatura do SHA256SUMS.txt…"
if command -v gpg >/dev/null; then
  fetch "$BASE/SHA256SUMS.txt.asc" "$CACHE/SHA256SUMS.txt.asc"
  fetch "$BASE/release-signing-key.asc" "$CACHE/release-signing-key.asc"
  gnupg="$(mktemp -d)"
  GNUPGHOME="$gnupg" gpg -q --import "$CACHE/release-signing-key.asc" 2>/dev/null
  # VALIDSIG: o primeiro campo é a (sub)chave que assinou; o último, quando
  # existe, é a chave principal.
  sig="$(GNUPGHOME="$gnupg" gpg --status-fd 1 --verify \
          "$CACHE/SHA256SUMS.txt.asc" "$CACHE/SHA256SUMS.txt" 2>/dev/null \
        | awk '/^\[GNUPG:\] VALIDSIG/{print $NF; exit}')"
  if [ "$sig" != "$FINGERPRINT" ]; then
    echo "assinatura inválida (fingerprint ${sig:-nenhum}, esperado $FINGERPRINT)" >&2
    exit 1
  fi
  echo "    assinatura boa: $FINGERPRINT"
else
  echo "    gpg ausente: só o SHA256 via HTTPS" >&2
fi

echo "  conferindo os sha256…"
(cd "$CACHE"
 awk -v zip="$ZIP" -v tar="$TARBALL" -v cli="$WITH_CLI" \
   '($2==zip) || (cli==1 && $2==tar)' SHA256SUMS.txt > SUMS.part
 sha256sum -c --quiet SUMS.part
 rm -f SUMS.part)

echo "  extraindo o site…"
tmp="$(mktemp -d)"
unzip -q "$CACHE/$ZIP" -d "$tmp"
site="$(find "$tmp" -maxdepth 1 -type d -name "gridcraft-web-$VERSION" -print -quit)"
if [ -z "$site" ]; then
  echo "zip sem a pasta gridcraft-web-$VERSION" >&2
  exit 1
fi
rm -rf web.new
mv "$site" web.new
# O nginx monta web/ como bind: trocar a pasta por baixo do contêiner deixa o
# mount antigo (vazio). Derruba antes e sobe de novo depois.
if podman container exists gridcraft-web 2>/dev/null; then
  echo "  parando o serviço para trocar o site…"
  GRIDCRAFT_PORT="$PORT" podman-compose -f compose.yaml down >/dev/null
fi
rm -rf web
mv web.new web
echo "    $(find web -type f | wc -l) arquivos, $(du -sh web | cut -f1)"

if [ "$WITH_CLI" = 1 ]; then
  echo "  extraindo a CLI…"
  tar -xzf "$CACHE/$TARBALL" -C "$tmp" --wildcards "*/bin/gridcraft-cli"
  cli_bin="$(find "$tmp" -type f -name gridcraft-cli -print -quit)"
  if [ -z "$cli_bin" ]; then
    echo "tarball sem bin/gridcraft-cli" >&2
    exit 1
  fi
  install -m 0755 "$cli_bin" bin/gridcraft-cli
  echo "    $(bin/gridcraft-cli --version 2>/dev/null || echo '?') em bin/"

  echo "  construindo a imagem da CLI (localhost/gridcraft-cli:$VERSION)…"
  podman build -q -t "localhost/gridcraft-cli:$VERSION" -t localhost/gridcraft-cli:latest \
    -f Containerfile.cli . >/dev/null
fi

printf '%s\n' "$VERSION" > .version
printf '%s\n' "$PORT" > .port

echo "  subindo o serviço web…"
GRIDCRAFT_PORT="$PORT" podman-compose -f compose.yaml up -d >/dev/null

code=""
for _ in $(seq 1 30); do
  code="$(curl -s -o /dev/null --max-time 2 -w '%{http_code}' "http://127.0.0.1:$PORT/index.html" || true)"
  [ "$code" = "200" ] && break
  sleep 1
done
if [ "$code" != "200" ]; then
  echo "o serviço não respondeu em 30 s (veja: podman logs gridcraft-web)" >&2
  exit 1
fi

echo
echo "GridCraft no ar: http://127.0.0.1:$PORT"
if [ "$WITH_CLI" = 1 ]; then
  echo "CLI:             $(pwd)/gridcraft.sh cli --help"
fi
