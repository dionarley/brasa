#!/usr/bin/env bash
# Uso diário do GridCraft instalado pelo install.sh.
#
#   tools/gridcraft/gridcraft.sh up|down|restart|status|logs [N]
#   tools/gridcraft/gridcraft.sh cli info workbooks/exemplo.xlsx
#   tools/gridcraft/gridcraft.sh cli eval '=SUM(B2:B9)' --in workbooks/exemplo.xlsx
#   tools/gridcraft/gridcraft.sh cli convert workbooks/exemplo.xlsx /tmp/exemplo.csv
#   tools/gridcraft/gridcraft.sh mcp --in workbooks/exemplo.xlsx   # MCP em stdio
#
# A CLI roda no contêiner com a raiz do projeto montada em /repo (é o diretório
# de trabalho), então os caminhos são os mesmos do host. O site é servido em
# http://127.0.0.1:<porta> (padrão 8088).
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

VERSION="$(cat .version 2>/dev/null || true)"
PORT="${GRIDCRAFT_PORT:-$(cat .port 2>/dev/null || echo 8088)}"
IMAGE="localhost/gridcraft-cli:${VERSION:-latest}"
REPO_ROOT="$(cd "$HERE/../.." && pwd)"
URL="http://127.0.0.1:$PORT/"

usage() { sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }

need_install() {
  [ -f web/index.html ] || { echo "nada instalado; rode $HERE/install.sh" >&2; exit 1; }
}

http_code() { curl -s -o /dev/null --max-time 2 -w '%{http_code}' "${URL}index.html" || true; }

wait_http() {
  local code=""
  for _ in $(seq 1 30); do
    code="$(http_code)"
    [ "$code" = "200" ] && { echo "no ar: $URL"; return 0; }
    sleep 1
  done
  echo "sem resposta em $URL (HTTP ${code:-?}); veja: $0 logs" >&2
  return 1
}

cmd_up() {
  need_install
  GRIDCRAFT_PORT="$PORT" podman-compose -f compose.yaml up -d >/dev/null
  wait_http
}

cmd_down() {
  if podman container exists gridcraft-web 2>/dev/null; then
    GRIDCRAFT_PORT="$PORT" podman-compose -f compose.yaml down >/dev/null
  fi
  echo "serviço web parado"
}

cmd_status() {
  local state="ausente" code version
  if podman container exists gridcraft-web 2>/dev/null; then
    state="$(podman inspect -f '{{.State.Status}}' gridcraft-web 2>/dev/null || echo '?')"
  fi
  code="$(http_code)"
  printf 'web        %s  (%s, contêiner %s)\n' "$URL" \
    "$([ "$code" = "200" ] && echo no-ar || echo "HTTP ${code:-?}")" "$state"
  if [ -n "$VERSION" ]; then
    printf 'versão     %s (site e CLI)\n' "$VERSION"
  else
    printf 'versão     (não instalado)\n'
  fi
  if [ -f web/index.html ]; then
    printf 'arquivos   %s em web/\n' "$(find web -type f | wc -l)"
  fi
  if podman image exists "$IMAGE" 2>/dev/null; then
    version="$(podman run --rm "$IMAGE" --version 2>/dev/null || echo '?')"
    printf 'cli        %s (%s)\n' "$version" "$IMAGE"
  fi
  [ "$code" = "200" ] || return 1
}

cmd_logs() {
  local n="${1:-40}"
  podman logs --tail "$n" gridcraft-web 2>&1
}

cmd_cli() {
  if ! podman image exists "$IMAGE" 2>/dev/null; then
    echo "imagem $IMAGE não existe; rode $HERE/install.sh" >&2
    exit 1
  fi
  # uid/gid 1000 são o usuário gridcraft da imagem: com keep-id os arquivos
  # gravados em /repo ficam com o dono e o grupo do usuário do host.
  exec podman run --rm -i --userns="keep-id:uid=1000,gid=1000" \
    -v "$REPO_ROOT:/repo" -w /repo \
    "$IMAGE" "$@"
}

case "${1:-}" in
  up)      cmd_up ;;
  down)    cmd_down ;;
  restart) cmd_down; cmd_up ;;
  status)  cmd_status ;;
  logs)    shift; cmd_logs "$@" ;;
  cli)     shift; cmd_cli "$@" ;;
  mcp)     shift; cmd_cli mcp "$@" ;;
  url)     echo "$URL" ;;
  open)    xdg-open "$URL" >/dev/null 2>&1 || echo "$URL" ;;
  *)       usage ;;
esac
