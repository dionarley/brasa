#!/usr/bin/env bash
# Instala o visualizador DXF (MLightCAD) e sobe o serviço no podman.
#
#   tools/cad-viewer/install.sh              # npm install + build + up, porta 8089
#   tools/cad-viewer/install.sh --no-up      # só instala e constrói
#   CAD_VIEWER_PORT=8099 tools/cad-viewer/install.sh
#
# O app é montado a partir dos pacotes publicados no npm (MIT); não clona o
# repositório do MLightCAD. O apoio a DWG (LibreDWG, GPL) fica de fora.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

PORT="${CAD_VIEWER_PORT:-8089}"
NODE_IMAGE="${CAD_NODE_IMAGE:-docker.io/library/node:22-alpine}"
WORKER="node_modules/@mlightcad/mtext-renderer/dist/mtext-renderer-worker.js"

WITH_UP=1
while [ $# -gt 0 ]; do
  case "$1" in
    --no-up) WITH_UP=0; shift ;;
    --port)  PORT="${2:?--port exige um número}"; shift 2 ;;
    -h|--help) sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "argumento inesperado: $1" >&2; exit 2 ;;
  esac
done

for tool in podman curl; do
  command -v "$tool" >/dev/null || { echo "falta $tool" >&2; exit 1; }
done
podman-compose version >/dev/null 2>&1 || { echo "falta podman-compose" >&2; exit 1; }

# Node/npm dentro do contêiner como o usuário do host: os arquivos de
# node_modules/ e dist/ saem com o dono do host.
node_run() {
  mkdir -p .npm drawings
  podman run --rm -i --userns="keep-id:uid=1000,gid=1000" --user node \
    -v "$PWD:/app" -w /app \
    -v "$PWD/.npm:/home/node/.npm" \
    -e HOME=/home/node -e npm_config_cache=/home/node/.npm \
    "$NODE_IMAGE" "$@"
}

echo "Visualizador DXF do Brasa · porta $PORT"
echo "  instalando dependências…"
if [ -f package-lock.json ]; then
  node_run npm ci --no-audit --no-fund
else
  node_run npm install --no-audit --no-fund
fi

echo "  construindo o app…"
node_run npm run build

if [ -f "$WORKER" ]; then
  mkdir -p dist/workers
  cp "$WORKER" dist/workers/
  echo "  worker de MTEXT copiado para dist/workers/"
else
  echo "  aviso: $WORKER não encontrado; o MTEXT usa a thread principal" >&2
fi

[ -f dist/index.html ] || { echo "build sem dist/index.html" >&2; exit 1; }

printf '%s\n' "$PORT" > .port

if [ "$WITH_UP" = 1 ]; then
  echo "  subindo o serviço web…"
  # Recria sempre: o dist/ é substituído a cada build e os volumes mudam.
  if podman container exists brasa-cad-viewer 2>/dev/null; then
    CAD_VIEWER_PORT="$PORT" podman-compose -f compose.yaml down >/dev/null
  fi
  CAD_VIEWER_PORT="$PORT" podman-compose -f compose.yaml up -d >/dev/null
  code=""
  for _ in $(seq 1 30); do
    code="$(curl -s -o /dev/null --max-time 2 -w '%{http_code}' "http://127.0.0.1:$PORT/index.html" || true)"
    [ "$code" = "200" ] && break
    sleep 1
  done
  [ "$code" = "200" ] || { echo "o serviço não respondeu em 30 s (podman logs brasa-cad-viewer)" >&2; exit 1; }
  echo
  echo "Visualizador no ar: http://127.0.0.1:$PORT"
  echo "Abrir um desenho:   $(pwd)/cad_viewer.sh view ../../dist/v0.19.0/PS-001-DR-001_rA_prancha-a2.dxf"
fi
