#!/usr/bin/env bash
# Uso diário do visualizador DXF do Brasa (MLightCAD no navegador).
#
#   tools/cad-viewer/cad_viewer.sh view ARQUIVO.dxf...   copia para drawings/ e abre
#   tools/cad-viewer/cad_viewer.sh publish DIR           copia os .dxf de DIR (recursivo)
#   tools/cad-viewer/cad_viewer.sh up|down|restart|status|logs [N]
#   tools/cad-viewer/cad_viewer.sh build                 npm install + build (sem subir)
#   tools/cad-viewer/cad_viewer.sh open|url
#
# O desenho é aberto por ?file=drawings/<nome>, servido pelo nginx do compose.
# Nada é enviado para fora: o DXF é lido no navegador.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

PORT="${CAD_VIEWER_PORT:-$(cat .port 2>/dev/null || echo 8089)}"
URL="http://127.0.0.1:$PORT/"
DRAWINGS="$HERE/drawings"

usage() { sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }

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

need_build() { [ -f dist/index.html ] || { echo "sem build; rode $0 build" >&2; exit 1; }; }

cmd_up() {
  need_build
  mkdir -p drawings
  # Contêiner antigo (sem o volume de drawings/): recria antes de subir.
  if podman container exists brasa-cad-viewer 2>/dev/null; then
    if ! podman inspect -f '{{range .Mounts}}{{.Destination}} {{end}}' brasa-cad-viewer 2>/dev/null |
      grep -q '/srv/drawings'; then
      cmd_down >/dev/null
    fi
  fi
  CAD_VIEWER_PORT="$PORT" podman-compose -f compose.yaml up -d >/dev/null
  wait_http
}

cmd_down() {
  if podman container exists brasa-cad-viewer 2>/dev/null; then
    CAD_VIEWER_PORT="$PORT" podman-compose -f compose.yaml down >/dev/null
  fi
  echo "visualizador parado"
}

cmd_status() {
  local state="ausente" code
  if podman container exists brasa-cad-viewer 2>/dev/null; then
    state="$(podman inspect -f '{{.State.Status}}' brasa-cad-viewer 2>/dev/null || echo '?')"
  fi
  code="$(http_code)"
  printf 'web        %s  (%s, contêiner %s)\n' "$URL" \
    "$([ "$code" = "200" ] && echo no-ar || echo "HTTP ${code:-?}")" "$state"
  printf 'build      %s\n' "$([ -f dist/index.html ] && date -r dist/index.html '+%Y-%m-%d %H:%M' || echo '(sem build)')"
  printf 'desenhos   %s em drawings/\n' "$(find "$DRAWINGS" -maxdepth 1 -name '*.dxf' 2>/dev/null | wc -l)"
  [ "$code" = "200" ] || return 1
}

# Copia um DXF para drawings/ (nome achatado) e devolve o nome publicado.
publish_one() {
  local src="$1" name
  [ -f "$src" ] || { echo "não existe: $src" >&2; return 1; }
  case "$src" in
    *.dxf|*.DXF) ;;
    *) echo "não é .dxf: $src" >&2; return 1 ;;
  esac
  name="$(basename "$src")"
  mkdir -p "$DRAWINGS"
  cp -f "$src" "$DRAWINGS/$name"
  printf '%s\n' "$name"
}

# Lista publicada que o app lê em drawings/index.json.
write_index() {
  mkdir -p "$DRAWINGS"
  {
    printf '[\n'
    find "$DRAWINGS" -maxdepth 1 -type f -name '*.dxf' -printf '  "%f",\n' 2>/dev/null |
      sort | sed '$ s/,$//'
    printf '\n]\n'
  } > "$DRAWINGS/index.json"
}

cmd_view() {
  [ $# -gt 0 ] || usage
  need_build
  [ "$(http_code)" = "200" ] || cmd_up >/dev/null
  local first="" name
  for src in "$@"; do
    name="$(publish_one "$src")" || continue
    [ -n "$first" ] || first="$name"
  done
  [ -n "$first" ] || return 1
  write_index
  local target="$URL?file=drawings/$first"
  xdg-open "$target" >/dev/null 2>&1 || echo "$target"
}

cmd_publish() {
  [ $# -gt 0 ] || usage
  local dir="$1" count=0
  [ -d "$dir" ] || { echo "não é diretório: $dir" >&2; exit 1; }
  while IFS= read -r file; do
    publish_one "$file" >/dev/null && count=$((count + 1))
  done < <(find "$dir" -type f \( -iname '*.dxf' \) | sort)
  write_index
  echo "$count desenho(s) em drawings/"
}

case "${1:-}" in
  view)    shift; cmd_view "$@" ;;
  publish) shift; cmd_publish "$@" ;;
  build)   exec "$HERE/install.sh" --no-up ;;
  up)      cmd_up ;;
  down)    cmd_down ;;
  restart) cmd_down; cmd_up ;;
  status)  cmd_status ;;
  logs)    shift; podman logs --tail "${1:-40}" brasa-cad-viewer 2>&1 ;;
  url)     echo "$URL" ;;
  open)    xdg-open "$URL" >/dev/null 2>&1 || echo "$URL" ;;
  *)       usage ;;
esac
