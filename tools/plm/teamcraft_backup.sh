#!/usr/bin/env bash
# Backup do TeamCraft do PS-001: banco (pg_dump no contêiner) + vault de arquivos.
#
#   tools/plm/teamcraft_backup.sh              # ~/teamcraft/backups/
#   tools/plm/teamcraft_backup.sh /mnt/backup  # destino explícito
#
# O pacote tem data UTC no nome e é autocontido: dump, vault, SHA256SUMS e um
# README com as instruções de restauração. Mantém os 7 mais recentes.
#
# O host não tem pg_dump/psql; por isso o dump roda dentro do contêiner
# teamcraft-db (podman). O cache de previews não entra no tar: é derivado e se
# refaz sozinho.
set -euo pipefail

HOME_DIR="${TEAMCRAFT_HOME:-$HOME/teamcraft}"
CONTAINER="${TEAMCRAFT_DB_CONTAINER:-teamcraft-db}"
DB="${TEAMCRAFT_DB_NAME:-teamcraft}"
DB_USER="${TEAMCRAFT_DB_USER:-teamcraft}"
VAULT="$HOME_DIR/data/vault"
DEST="${1:-$HOME_DIR/backups}"
KEEP="${TEAMCRAFT_BACKUP_KEEP:-7}"

umask 077

[ -d "$VAULT" ] || { echo "vault não encontrado em $VAULT" >&2; exit 1; }
command -v podman >/dev/null || { echo "podman não encontrado" >&2; exit 1; }

running="$(podman inspect -f '{{.State.Running}}' "$CONTAINER" 2>/dev/null || echo false)"
[ "$running" = "true" ] || { echo "contêiner $CONTAINER não está rodando" >&2; exit 1; }

mkdir -p "$DEST"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BASE="$DEST/teamcraft-$STAMP"
DUMP="$BASE.dump"

if command -v zstd >/dev/null; then
  VCOMP=zstd
  VAULT_FILE="$BASE-vault.tar.zst"
  TAR_COMP=(--zstd)
else
  VCOMP=gzip
  VAULT_FILE="$BASE-vault.tar.gz"
  TAR_COMP=(-z)
fi

echo "TeamCraft · backup $STAMP"
echo "  destino: $DEST"

echo "  banco: $DB (contêiner $CONTAINER)"
podman exec "$CONTAINER" pg_dump -U "$DB_USER" -d "$DB" -Fc --no-owner > "$DUMP"

echo "  vault: $VAULT (sem previews)"
tar -C "$HOME_DIR/data" "${TAR_COMP[@]}" \
  --exclude='vault/previews' \
  -cf "$VAULT_FILE" vault

# --------------------------------------------------------------- manifesto
( cd "$DEST" && sha256sum "$(basename "$DUMP")" "$(basename "$VAULT_FILE")" \
    > "$BASE.SHA256SUMS" )

BIN="$(ls -d "$HOME_DIR"/teamcraft-*/teamcraft 2>/dev/null | head -1 || true)"
TC_VERSION="$("$BIN" --version 2>/dev/null | head -1 || echo '?')"
PUBLIC_URL="$(sed -n 's/^TEAMCRAFT_PUBLIC_URL=//p' "$HOME_DIR/teamcraft.env" 2>/dev/null || true)"

cat > "$BASE.README.txt" <<EOF
Backup do TeamCraft — PS-001
Gerado em: $(date -Iseconds)
Servidor: ${PUBLIC_URL:-http://127.0.0.1:8080}
Versão:   ${TC_VERSION:-?}
Banco:    $DB (usuário $DB_USER, formato custom)
Vault:    $VAULT (compactação $VCOMP, sem o cache de previews)

Conteúdo:
  $(basename "$DUMP")            pg_dump -Fc
  $(basename "$VAULT_FILE")      tar do vault
  $(basename "$BASE.SHA256SUMS")

Conferir:
  cd $DEST && sha256sum -c $(basename "$BASE.SHA256SUMS")

Restaurar (servidor parado):
  pkill -x teamcraft
  podman exec $CONTAINER psql -U $DB_USER -d postgres \\
    -c 'DROP DATABASE $DB WITH (FORCE);' \\
    -c 'CREATE DATABASE $DB OWNER $DB_USER;'
  podman exec -i $CONTAINER pg_restore -U $DB_USER -d $DB --no-owner < $(basename "$DUMP")
  rm -rf $VAULT
  tar -C $HOME_DIR/data -xf $(basename "$VAULT_FILE")
  cd $HOME_DIR && TEAMCRAFT_ENV_FILE=\$PWD/teamcraft.env \\
    nohup $BIN serve >> teamcraft.log 2>&1 &
  curl -s ${PUBLIC_URL:-http://127.0.0.1:8080}/readyz

O dump não contém as senhas dos usuários em texto: os hashes argon2 estão na tabela
users e continuam válidos. Tokens também são preservados.
EOF

# ------------------------------------------------------------------ retenção
mapfile -t old < <(ls -1t "$DEST"/teamcraft-*.dump 2>/dev/null | tail -n +$((KEEP + 1)) || true)
for dump in "${old[@]}"; do
  [ -n "$dump" ] || continue
  stem="${dump%.dump}"
  rm -f "$dump" "$stem"-vault.tar.* "$stem.SHA256SUMS" "$stem.README.txt"
done
[ "${#old[@]}" -gt 0 ] && echo "  retenção: ${#old[@]} pacote(s) antigo(s) removido(s) (mantidos $KEEP)"

echo "  $(basename "$DUMP"): $(du -h "$DUMP" | cut -f1)"
echo "  $(basename "$VAULT_FILE"): $(du -h "$VAULT_FILE" | cut -f1)"
echo "ok"
