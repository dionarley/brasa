#!/usr/bin/env bash
# Logos e nome do cabeçalho da instância TeamCraft do Brasa.
#
#   tools/plm/admin/teamcraft_branding.sh status
#       nome/subtítulo e situação de cada logo (enviado, sha, ou embutido)
#   tools/plm/admin/teamcraft_branding.sh upload [wide|square|both]
#       envia branding/brasa-<kind>.svg; `both` (padrão) envia os dois
#   tools/plm/admin/teamcraft_branding.sh upload wide --file outro.svg
#       envia um arquivo específico (PNG, JPEG, WebP ou SVG)
#   tools/plm/admin/teamcraft_branding.sh reset [wide|square|both]
#       volta ao logo embutido do TeamCraft
#   tools/plm/admin/teamcraft_branding.sh name --display "Brasa PLM" --subtitle PLM
#       grava o nome do cabeçalho (vazio = padrão da instância)
#
# O upload é rota web (POST /admin/branding/{kind}); exige sessão de
# administrador e os cabeçalhos Origin/Referer, senão o TeamCraft responde 403.
# O `status` lê GET /api/v1/branding com o token pessoal de administrador.
# Envios idempotentes: se o sha256 do arquivo já é o do servidor, nada é feito.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRANDING_DIR="${BRASA_BRANDING_DIR:-$HERE/../../../branding}"
HOME_DIR="${TEAMCRAFT_HOME:-$HOME/teamcraft}"
CREDS="${TEAMCRAFT_CREDENTIALS:-$HOME_DIR/credentials.txt}"
BASE="${TEAMCRAFT_SERVER:-http://127.0.0.1:8080}"

usage() { sed -n '2,19p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }

need() { command -v "$1" >/dev/null || { echo "falta $1" >&2; exit 1; }; }
need curl
need python3
[ -f "$CREDS" ] || { echo "falta $CREDS" >&2; exit 1; }

creds() { sed -n "s/^$1=//p" "$CREDS" | head -1; }
ADMIN_USER="$(creds admin_user)"
ADMIN_PASS="$(creds admin_password)"
ADMIN_TOKEN="$(creds admin_token)"
[ -n "$ADMIN_USER" ] && [ -n "$ADMIN_PASS" ] || { echo "credenciais sem admin_user/admin_password" >&2; exit 1; }

jar="$(mktemp)"
trap 'rm -f "$jar"' EXIT
login() {
  local code
  code="$(curl -sS -o /dev/null -c "$jar" -w '%{http_code}' \
    -H "Origin: $BASE" -H "Referer: $BASE/login" \
    --data-urlencode "username=$ADMIN_USER" \
    --data-urlencode "password=$ADMIN_PASS" \
    --data-urlencode "next=/" \
    "$BASE/login")"
  case "$code" in
    200|303) ;;
    403) echo "login recusado (403): faltou Origin/Referer?" >&2; exit 1 ;;
    *)   echo "login falhou (HTTP $code)" >&2; exit 1 ;;
  esac
}

api() {
  curl -sS --fail-with-body -H "Authorization: Bearer $ADMIN_TOKEN" "$BASE$1"
}

# sha256 em minúsculas do arquivo, como o TeamCraft grava.
sha256_file() { sha256sum "$1" | cut -d' ' -f1; }

# Tipo do arquivo pelos primeiros bytes; o TeamCraft decide pelo conteúdo.
file_type() {
  python3 - "$1" <<'PY'
import sys
b = open(sys.argv[1], 'rb').read(512)
if b.startswith(b'\x89PNG\r\n\x1a\n'):        print('image/png')
elif b.startswith(b'\xff\xd8\xff'):           print('image/jpeg')
elif b[:4] == b'RIFF' and b[8:12] == b'WEBP': print('image/webp')
elif b.lstrip()[:5] in (b'<?xml', b'<svg '):  print('image/svg+xml')
else:                                          print('')
PY
}

# Token do servidor para um slot ("-" = logo embutido).
server_token() {
  api /api/v1/branding | python3 -c 'import json,sys; print(json.load(sys.stdin).get(sys.argv[1]) or "-")' "$1"
}

kinds() {
  case "${1:-both}" in
    wide|square) echo "$1" ;;
    both)        echo "wide square" ;;
    *)           echo "slot inválido: $1 (use wide, square ou both)" >&2; exit 2 ;;
  esac
}

cmd_status() {
  local info
  info="$(api /api/v1/branding)" || { echo "servidor fora do ar em $BASE" >&2; exit 1; }
  printf 'nome       %s\n' "$(echo "$info" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("display_name") or "(padrão)")')"
  printf 'subtítulo  %s\n' "$(echo "$info" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("subtitle") or "(padrão)")')"
  local kind tok local_file local_sha mark
  for kind in wide square; do
    tok="$(echo "$info" | python3 -c 'import json,sys; print(json.load(sys.stdin).get(sys.argv[1]) or "")' "$kind")"
    local_file="$BRANDING_DIR/brasa-$kind.svg"
    if [ -f "$local_file" ]; then
      local_sha="$(sha256_file "$local_file")"
    else
      local_sha=""
    fi
    if [ -z "$tok" ]; then
      printf '%-9s embutido do TeamCraft\n' "$kind"
    else
      if [ -n "$local_sha" ] && [ "${local_sha:0:12}" = "$tok" ]; then
        mark="igual ao arquivo local"
      else
        mark="difere do arquivo local"
      fi
      printf '%-9s %s  (%s)\n' "$kind" "$tok" "$mark"
    fi
  done
}

cmd_upload() {
  local slot="${1:-both}" file=""
  shift || true
  while [ $# -gt 0 ]; do
    case "$1" in
      --file) file="${2:?--file exige um caminho}"; shift 2 ;;
      *)      echo "argumento inesperado: $1" >&2; exit 2 ;;
    esac
  done

  login
  local kind path ctype code tok sha before after
  for kind in $(kinds "$slot"); do
    path="${file:-$BRANDING_DIR/brasa-$kind.svg}"
    [ -f "$path" ] || { echo "não encontrei $path" >&2; exit 1; }
    ctype="$(file_type "$path")"
    [ -n "$ctype" ] || { echo "$path não é PNG, JPEG, WebP nem SVG" >&2; exit 1; }

    before="$(server_token "$kind")"
    sha="$(sha256_file "$path")"
    if [ "${sha:0:12}" = "$before" ]; then
      echo "$kind: já é este arquivo (${before}), nada a fazer"
      continue
    fi

    code="$(curl -sS -o /dev/null -b "$jar" -c "$jar" -w '%{http_code}' \
      -H "Origin: $BASE" -H "Referer: $BASE/admin/branding" \
      -F "file=@$path;type=$ctype" \
      "$BASE/admin/branding/$kind")"
    case "$code" in
      200|303) ;;
      *) echo "$kind: upload recusado (HTTP $code) — veja o log do servidor" >&2; exit 1 ;;
    esac

    after="$(server_token "$kind")"
    if [ "${sha:0:12}" != "$after" ]; then
      echo "$kind: o servidor não adotou o arquivo (token ${after:-nenhum})" >&2
      exit 1
    fi
    echo "$kind: enviado ($after, $(wc -c <"$path") bytes, $ctype)"
  done
}

cmd_reset() {
  local slot="${1:-both}"
  login
  local kind code
  for kind in $(kinds "$slot"); do
    code="$(curl -sS -o /dev/null -b "$jar" -c "$jar" -w '%{http_code}' \
      -H "Origin: $BASE" -H "Referer: $BASE/admin/branding" \
      -X POST "$BASE/admin/branding/$kind/reset")"
    case "$code" in
      200|303) ;;
      *) echo "$kind: reset recusado (HTTP $code)" >&2; exit 1 ;;
    esac
    if [ "$(server_token "$kind")" = "-" ]; then
      echo "$kind: logo embutido de volta"
    else
      echo "$kind: o servidor continua com um logo próprio" >&2
      exit 1
    fi
  done
}

cmd_name() {
  local display="" subtitle="" set_display=0 set_subtitle=0
  while [ $# -gt 0 ]; do
    case "$1" in
      --display)  display="${2-}"; set_display=1; shift 2 ;;
      --subtitle) subtitle="${2-}"; set_subtitle=1; shift 2 ;;
      *)          echo "argumento inesperado: $1" >&2; exit 2 ;;
    esac
  done
  [ "$set_display" = 1 ] || [ "$set_subtitle" = 1 ] || { echo "informe --display e/ou --subtitle" >&2; exit 2; }
  # Campo não informado mantém o valor atual.
  local current
  current="$(api /api/v1/branding)"
  if [ "$set_display" = 0 ]; then
    display="$(echo "$current" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("display_name") or "")')"
  fi
  if [ "$set_subtitle" = 0 ]; then
    subtitle="$(echo "$current" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("subtitle") or "")')"
  fi
  if [ "$display" = "$(echo "$current" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("display_name") or "")')" ] &&
     [ "$subtitle" = "$(echo "$current" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("subtitle") or "")')" ]; then
    echo "nome já é \"${display:-(padrão)}\" / \"${subtitle:-(padrão)}\", nada a fazer"
    return 0
  fi

  login
  local code
  code="$(curl -sS -o /dev/null -b "$jar" -c "$jar" -w '%{http_code}' \
    -H "Origin: $BASE" -H "Referer: $BASE/admin/branding" \
    --data-urlencode "display_name=$display" \
    --data-urlencode "subtitle=$subtitle" \
    "$BASE/admin/branding/name")"
  case "$code" in
    200|303) ;;
    *) echo "nome recusado (HTTP $code)" >&2; exit 1 ;;
  esac
  api /api/v1/branding | python3 -c 'import json,sys; d=json.load(sys.stdin); print("nome: %s | subtítulo: %s" % (d.get("display_name") or "(padrão)", d.get("subtitle") or "(padrão)"))'
}

case "${1:-}" in
  status) cmd_status ;;
  upload) shift; cmd_upload "$@" ;;
  reset)  shift; cmd_reset "$@" ;;
  name)   shift; cmd_name "$@" ;;
  *)      usage ;;
esac
