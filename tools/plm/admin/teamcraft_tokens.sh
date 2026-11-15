#!/usr/bin/env bash
# Tokens pessoais de acesso (PAT) do TeamCraft — listar, criar, revogar.
#
#   tools/plm/admin/teamcraft_tokens.sh list
#       tokens do administrador: nome, escopo, prefixo, criado, expira, último uso
#   tools/plm/admin/teamcraft_tokens.sh new --name "CI" [--scope SCOPE] [--days N]
#       cria um token e imprime o valor UMA vez (o servidor nunca o repete)
#   tools/plm/admin/teamcraft_tokens.sh revoke --id UUID | --name "CI"
#       revoga um token; --name precisa ser único
#
# Escopos: full (lê, escreve e aprova; padrão), write (sem aprovar),
# read_only (só leitura) e mcp_only (só as rotas do servidor MCP).
# --days ausente = sem validade. Vale para o dono do token; administrador
# revoga o token de qualquer usuário via --id.
#
# Autenticação: o token pessoal admin_token de ~/teamcraft/credentials.txt
# (ou TEAMCRAFT_TOKEN). Ele precisa ter escopo full ou write; um token
# mcp_only não alcança /api/v1/tokens e o servidor responde 403.
set -euo pipefail

HOME_DIR="${TEAMCRAFT_HOME:-$HOME/teamcraft}"
CREDS="${TEAMCRAFT_CREDENTIALS:-$HOME_DIR/credentials.txt}"
BASE="${TEAMCRAFT_SERVER:-http://127.0.0.1:8080}"

usage() { sed -n '2,17p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }

command -v curl >/dev/null || { echo "falta curl" >&2; exit 1; }
command -v python3 >/dev/null || { echo "falta python3" >&2; exit 1; }

TOKEN="${TEAMCRAFT_TOKEN:-}"
if [ -z "$TOKEN" ] && [ -f "$CREDS" ]; then
  TOKEN="$(sed -n 's/^admin_token=//p' "$CREDS" | head -1)"
fi
[ -n "$TOKEN" ] || { echo "sem token: defina TEAMCRAFT_TOKEN ou admin_token em $CREDS" >&2; exit 1; }

# api METHOD PATH [JSON] -> corpo; erro HTTP vira mensagem legível.
api() {
  local method="$1" path="$2" body="${3:-}" tmp code
  tmp="$(mktemp)"
  local args=(-sS -o "$tmp" -w '%{http_code}' -X "$method"
              -H "Authorization: Bearer $TOKEN" -H "Accept: application/json")
  [ -n "$body" ] && args+=(-H 'Content-Type: application/json' --data "$body")
  code="$(curl "${args[@]}" "$BASE$path")" || { rm -f "$tmp"; echo "servidor fora do ar em $BASE" >&2; exit 1; }
  if [ "$code" -lt 200 ] || [ "$code" -ge 300 ]; then
    echo "HTTP $code em $method $path: $(cat "$tmp")" >&2
    rm -f "$tmp"
    exit 1
  fi
  cat "$tmp"
  rm -f "$tmp"
}

cmd_list() {
  api GET /api/v1/tokens | python3 -c '
import json, sys
rows = json.load(sys.stdin)
if not rows:
    print("nenhum token")
    sys.exit()
def short(ts):
    return (ts or "-")[:10]
print("%-28s %-9s %-14s %-10s %-10s %s" % ("NOME", "ESCOPO", "PREFIXO", "CRIADO", "EXPIRA", "ID"))
for r in sorted(rows, key=lambda r: r.get("created_at") or ""):
    print("%-28s %-9s %-14s %-10s %-10s %s" % (
        (r.get("name") or "")[:28], r.get("scope") or "?", r.get("token_prefix") or "",
        short(r.get("created_at")), short(r.get("expires_at")), r.get("id")))
'
}

cmd_new() {
  local name="" scope="full" days="" json
  while [ $# -gt 0 ]; do
    case "$1" in
      --name)  name="${2:?--name exige um valor}"; shift 2 ;;
      --scope) scope="${2:?--scope exige um valor}"; shift 2 ;;
      --days)  days="${2:?--days exige um número}"; shift 2 ;;
      *)       echo "argumento inesperado: $1" >&2; exit 2 ;;
    esac
  done
  [ -n "$name" ] || { echo "informe --name" >&2; exit 2; }
  case "$scope" in full|write|read_only|mcp_only) ;; *) echo "escopo inválido: $scope" >&2; exit 2 ;; esac

  json="$(python3 -c '
import json, sys
body = {"name": sys.argv[1], "scope": sys.argv[2]}
if sys.argv[3]:
    body["expires_in_days"] = int(sys.argv[3])
print(json.dumps(body))
' "$name" "$scope" "$days")"

  api POST /api/v1/tokens "$json" | python3 -c '
import json, sys
r = json.load(sys.stdin)
for k, v in (("nome", r.get("name")), ("escopo", r.get("scope")),
             ("prefixo", r.get("token_prefix")), ("expira", r.get("expires_at") or "nunca"),
             ("id", r.get("id"))):
    print("%s=%s" % (k, v), file=sys.stderr)
print(r["token"])
'
  echo "guarde o valor: o TeamCraft não mostra o token de novo" >&2
}

cmd_revoke() {
  local id="" name=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --id)   id="${2:?--id exige um UUID}"; shift 2 ;;
      --name) name="${2:?--name exige um valor}"; shift 2 ;;
      *)      echo "argumento inesperado: $1" >&2; exit 2 ;;
    esac
  done
  if [ -z "$id" ] && [ -z "$name" ]; then
    echo "informe --id ou --name" >&2; exit 2
  fi
  if [ -z "$id" ]; then
    id="$(api GET /api/v1/tokens | python3 -c '
import json, sys
rows = [r for r in json.load(sys.stdin) if r.get("name") == sys.argv[1]]
if len(rows) != 1:
    print("ERR:%d" % len(rows))
else:
    print(rows[0]["id"])
' "$name")"
    case "$id" in
      ERR:0) echo "nenhum token chamado \"$name\"" >&2; exit 1 ;;
      ERR:*) echo "mais de um token chamado \"$name\"; use --id" >&2; exit 1 ;;
    esac
  fi
  api DELETE "/api/v1/tokens/$id" >/dev/null
  echo "token $id revogado"
}

case "${1:-list}" in
  list)   cmd_list ;;
  new)    shift; cmd_new "$@" ;;
  revoke) shift; cmd_revoke "$@" ;;
  -h|--help|help) usage ;;
  *)      usage ;;
esac
