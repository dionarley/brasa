#!/usr/bin/env bash
# Controle do TeamCraft local do Brasa: banco em podman + servidor.
#
#   tools/plm/admin/teamcraft_service.sh up       sobe banco e servidor
#   tools/plm/admin/teamcraft_service.sh down     encerra só o servidor
#   tools/plm/admin/teamcraft_service.sh restart  down + up
#   tools/plm/admin/teamcraft_service.sh status   banco, servidor, contadores, backup
#   tools/plm/admin/teamcraft_service.sh logs [N] últimas N linhas (padrão 40)
#
# O `down` não mexe no contêiner do banco: os dados ficam no volume e sobem no
# próximo `up`. Ele encerra o processo `teamcraft serve`; a ponte MCP
# (`teamcraft mcp`) do OpenCode cai junto e volta a conectar quando o servidor
# responder de novo. Ver tools/plm/admin/README.md.
set -euo pipefail

HOME_DIR="${TEAMCRAFT_HOME:-$HOME/teamcraft}"
ENV_FILE="$HOME_DIR/teamcraft.env"
BASE="${TEAMCRAFT_SERVER:-http://127.0.0.1:8080}"
CONTAINER="${TEAMCRAFT_DB_CONTAINER:-teamcraft-db}"
DB_USER="${TEAMCRAFT_DB_USER:-teamcraft}"
DB_NAME="${TEAMCRAFT_DB_NAME:-teamcraft}"
LOG="$HOME_DIR/teamcraft.log"

BIN="$(ls "$HOME_DIR"/teamcraft-*/teamcraft 2>/dev/null | sort -V | tail -1)"
[ -n "${BIN:-}" ] || { echo "binário do TeamCraft não encontrado em $HOME_DIR" >&2; exit 1; }
[ -f "$ENV_FILE" ] || { echo "falta $ENV_FILE" >&2; exit 1; }

usage() { sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }
# O processo pode ter sido iniciado pelo caminho absoluto ou relativo
# (./teamcraft-0.2.7-linux-x86_64/teamcraft serve); a ponte MCP é `teamcraft mcp`
# e não entra no padrão.
server_pids() { pgrep -f -- '(^|/)teamcraft serve' || true; }
http_code() { curl -s -o /dev/null --max-time 3 -w '%{http_code}' "$BASE/login" || true; }
db_ready() { podman exec "$CONTAINER" pg_isready -U "$DB_USER" -d "$DB_NAME" >/dev/null 2>&1; }

cmd_up() {
  local code running i
  code="$(http_code)"
  if [ "$code" = "200" ]; then
    echo "servidor já responde em $BASE"
    return 0
  fi

  running="$(podman inspect -f '{{.State.Running}}' "$CONTAINER" 2>/dev/null || echo false)"
  if [ "$running" != "true" ]; then
    echo "subindo o banco ($CONTAINER)…"
    podman start "$CONTAINER" >/dev/null
  fi
  for i in $(seq 1 30); do db_ready && break; sleep 1; done
  db_ready || { echo "banco não respondeu em 30 s" >&2; exit 1; }

  if [ -n "$(server_pids)" ]; then
    echo "processo do servidor existe mas não responde; veja $LOG" >&2
    exit 1
  fi

  echo "subindo o servidor…"
  # shellcheck source=/dev/null
  ( set -a; . "$ENV_FILE"; set +a; nohup "$BIN" serve >>"$LOG" 2>&1 & )
  for i in $(seq 1 30); do [ "$(http_code)" = "200" ] && break; sleep 1; done
  [ "$(http_code)" = "200" ] || { echo "servidor não respondeu em 30 s; veja $LOG" >&2; exit 1; }
  echo "no ar: $BASE"
}

cmd_down() {
  local pids
  pids="$(server_pids)"
  if [ -z "$pids" ]; then
    echo "servidor não está rodando"
    return 0
  fi
  echo "encerrando o servidor (pid $(echo "$pids" | tr '\n' ' '))…"
  # shellcheck disable=SC2086
  kill -TERM $pids
  for _ in $(seq 1 15); do
    [ -z "$(server_pids)" ] && { echo "servidor encerrado"; return 0; }
    sleep 1
  done
  echo "o servidor não encerrou em 15 s; veja $LOG" >&2
  return 1
}

cmd_status() {
  local state="parado" code version name items revisions changes projects
  if podman container exists "$CONTAINER" 2>/dev/null; then
    [ "$(podman inspect -f '{{.State.Running}}' "$CONTAINER" 2>/dev/null || echo false)" = "true" ] \
      && state="rodando" || state="parado"
  else
    state="não existe"
  fi
  db_ready && db="pronto" || db="fora"

  code="$(http_code)"
  if [ "$code" = "200" ]; then
    version="$(curl -s --max-time 3 "$BASE/api/v1" \
      | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("name","?"), d.get("version","?"))' 2>/dev/null || echo "?")"
  else
    version="-"
  fi

  printf 'servidor   %s  (%s)\n' "$BASE" "$([ "$code" = "200" ] && echo no-ar || echo "HTTP ${code:-?}")"
  printf 'versão     %s\n' "$version"
  printf 'banco      %s  (contêiner %s %s)\n' "$db" "$CONTAINER" "$state"

  if db_ready; then
    read -r items revisions changes projects < <(
      podman exec "$CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -A -t -F ' ' -c \
        "select (select count(*) from items),
                (select count(*) from revisions),
                (select count(*) from changes),
                (select count(*) from projects);"
    )
    printf 'conteúdo   %s itens, %s revisões, %s ECO%s, %s grupo%s\n' \
      "$items" "$revisions" "$changes" "$([ "$changes" = 1 ] || echo s)" \
      "$projects" "$([ "$projects" = 1 ] || echo s)"
  fi

  printf 'vault      %s\n' "$(du -sh "$HOME_DIR/data/vault" 2>/dev/null | cut -f1 || echo '-')"
  local last_backup name="(nenhum)"
  last_backup="$(ls -t "$HOME_DIR"/backups/*.dump 2>/dev/null | head -1 || true)"
  [ -n "$last_backup" ] && name="$(basename "$last_backup")"
  printf 'backup     %s\n' "$name"
  printf 'log        %s\n' "$LOG"
  [ "$code" = "200" ] || return 1
}

cmd_logs() {
  local n="${1:-40}"
  [ -f "$LOG" ] || { echo "sem log em $LOG" >&2; exit 1; }
  tail -n "$n" "$LOG" | sed 's/\x1b\[[0-9;]*m//g'
}

case "${1:-}" in
  up)      cmd_up ;;
  down)    cmd_down ;;
  restart) cmd_down; cmd_up ;;
  status)  cmd_status ;;
  logs)    cmd_logs "${2:-40}" ;;
  *)       usage ;;
esac
