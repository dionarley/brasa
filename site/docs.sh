#!/usr/bin/env bash
# Documentação do Brasa: build do Docusaurus (Node no podman) e site no nginx.
#
#   tools/../site/docs.sh build     # renders da última liberação + npm ci + build
#   site/docs.sh serve             # build e sobe o site em 127.0.0.1:8081
#   site/docs.sh up|down|restart   # só o serviço web (usa o build existente)
#   site/docs.sh status|logs [N]|url|open
#   site/docs.sh dev               # servidor de desenvolvimento em 127.0.0.1:8082
#
# A fonte da documentação é ../docs (Markdown do projeto) e o LEGAL.md da raiz;
# nada é editado dentro de site/. O build sai em site/build (fora do git).
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HERE/.." && pwd)"
cd "$HERE"

PORT="${DOCS_PORT:-8081}"
DEV_PORT="${DOCS_DEV_PORT:-8082}"
NODE_IMAGE="${DOCS_NODE_IMAGE:-docker.io/library/node:22-alpine}"
URL="http://127.0.0.1:$PORT/"

usage() { sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }

command -v podman >/dev/null || { echo "falta podman" >&2; exit 1; }
podman-compose version >/dev/null 2>&1 || { echo "falta podman-compose" >&2; exit 1; }

# Node/npm dentro do contêiner, como o usuário do host (arquivos 1000:1000,
# dependências em site/node_modules, cache em site/.npm). A raiz do projeto é
# montada em /repo porque o conteúdo do site é ../docs e o LEGAL.md da raiz.
node_run() {
  mkdir -p .npm
  podman run --rm -i --userns="keep-id:uid=1000,gid=1000" --user node \
    -v "$REPO_ROOT:/repo" -w /repo/site \
    -v "$REPO_ROOT/site/.npm:/home/node/.npm" \
    -e HOME=/home/node -e npm_config_cache=/home/node/.npm \
    "$NODE_IMAGE" "$@"
}

# As imagens dos manuais apontam para renders/ (gerados em dist/v<versão>/).
# Também os arquivos da raiz que o texto cita: o LICENSE (o LEGAL.md aponta para
# ele) é copiado como está, sem edição, para /LICENSE.
sync_renders() {
  local latest=""
  latest="$(ls -d ../dist/v*/ 2>/dev/null | sort -V | tail -1 || true)"
  if [ -n "$latest" ] && [ -d "$latest/renders" ]; then
    rm -rf static/renders
    cp -R "$latest/renders" static/renders
    echo "renders de $(basename "$latest") em static/renders"
  else
    echo "aviso: sem renders em ../dist/v*/renders; as figuras dos manuais vão faltar" >&2
  fi
  if [ -f ../LICENSE ]; then
    cp ../LICENSE static/LICENSE
    echo "LICENSE da raiz em static/LICENSE"
  else
    echo "aviso: sem ../LICENSE; o link do aviso legal vai faltar" >&2
  fi
}

http_code() { curl -s -o /dev/null --max-time 2 -w '%{http_code}' "${URL}" || true; }

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

compose() { DOCS_PORT="$PORT" podman-compose -f compose.yaml "$@"; }

cmd_build() {
  sync_renders
  if [ -f package-lock.json ]; then
    node_run npm ci --no-audit --no-fund
  else
    node_run npm install --no-audit --no-fund
  fi
  node_run npm run build
  echo "build em $HERE/build"
  # O nginx monta build/ como bind: recriar o contêiner para ver o build novo.
  if podman container exists brasa-docs 2>/dev/null; then
    compose down >/dev/null
    compose up -d >/dev/null
    wait_http
  fi
}

cmd_up() {
  if [ ! -f build/index.html ]; then
    echo "sem build; rode: $0 build" >&2
    exit 1
  fi
  compose up -d >/dev/null
  wait_http
}

cmd_down() {
  if podman container exists brasa-docs 2>/dev/null; then
    compose down >/dev/null
  fi
  echo "site parado"
}

cmd_status() {
  local state="ausente" code build_at="(sem build)"
  if podman container exists brasa-docs 2>/dev/null; then
    state="$(podman inspect -f '{{.State.Status}}' brasa-docs 2>/dev/null || echo '?')"
  fi
  code="$(http_code)"
  [ -f build/index.html ] && build_at="$(date -r build/index.html '+%Y-%m-%d %H:%M')"
  printf 'site      %s  (%s, contêiner %s)\n' "$URL" \
    "$([ "$code" = "200" ] && echo no-ar || echo "HTTP ${code:-?}")" "$state"
  printf 'build     %s\n' "$build_at"
  if [ -d build ]; then
    printf 'páginas   %s arquivos HTML\n' "$(find build -name '*.html' | wc -l)"
  fi
  [ "$code" = "200" ] || return 1
}

cmd_logs() { podman logs --tail "${1:-40}" brasa-docs 2>&1; }

cmd_dev() {
  mkdir -p .npm
  echo "dev em http://127.0.0.1:$DEV_PORT/ (Ctrl+C encerra)"
  podman run --rm -it --userns="keep-id:uid=1000,gid=1000" --user node \
    -p "127.0.0.1:$DEV_PORT:3000" \
    -v "$REPO_ROOT:/repo" -w /repo/site \
    -v "$REPO_ROOT/site/.npm:/home/node/.npm" \
    -e HOME=/home/node -e npm_config_cache=/home/node/.npm \
    "$NODE_IMAGE" \
    sh -c 'npm install --no-audit --no-fund >/dev/null && npx docusaurus start --host 0.0.0.0 --port 3000 --poll 1000'
}

case "${1:-}" in
  build)   cmd_build ;;
  serve)   cmd_build; cmd_up ;;
  up)      cmd_up ;;
  down)    cmd_down ;;
  restart) cmd_down; cmd_up ;;
  status)  cmd_status ;;
  logs)    shift; cmd_logs "${1:-40}" ;;
  dev)     cmd_dev ;;
  url)     echo "$URL" ;;
  open)    xdg-open "$URL" >/dev/null 2>&1 || echo "$URL" ;;
  *)       usage ;;
esac
