---
title: "Brasa (PS-001) — TeamCraft: instalação, operação e registro"
subtitle: "PDM local, ciclo de revisões, MCP e backup"
docid: "PS-001-PL-003"
revision: "C"
status: "Aprovado"
date: "2026-11-15"
author: "Dionarley"
project: "Brasa — estanhador 550 W / 127 V (PS-001, estudo)"
---

# 1. Objetivo

Este documento descreve a instância do **TeamCraft** usada como PDM do PS-001:
o que nela é registrado, como foi instalada, como se trabalha no dia a dia, como o
OpenCode consulta os dados e como o conjunto é salvo e restaurado.

O [PLANO.md](PLANO.md) define o processo (códigos, estados, papéis e liberação);
este documento é o **manual da ferramenta** que passou a guardar esse processo. O
[REGISTRO.md](REGISTRO.md) continua sendo o índice legível dos documentos, agora
acompanhado do registro mestre do TeamCraft.

Escopo: instância **local**, em `127.0.0.1`, para um projeto de estudo. Não há
exposição na rede, TLS, SSO nem backup remoto. O TeamCraft está em
desenvolvimento (versão 0.2.7) e não substitui um PDM certificado.

# 2. O que o TeamCraft guarda

| Conceito | No PS-001 |
|---|---|
| **Item** | peça, conjunto ou documento com número fixo (`PS-001`, `PS-001-LM-01`, `PS-001-PL-003`) |
| **Revisão** | letra (`A`, `B`, …) com estado `in_work`, `in_review`, `released` ou `obsolete` |
| **Arquivo** | versão imutável no vault, endereçada por sha256, com pasta e comentário |
| **BOM** | estrutura do conjunto: 16 linhas, com quantidade, número de posição e nota |
| **Referência** | ligação documentada entre o conjunto e os documentos controlados |
| **ECO** | ordem de mudança que libera revisões em conjunto, com revisão de outra pessoa |
| **ECR** | pedido de mudança (opcional; este projeto usa ECO direto para correções já analisadas) |

Regra que vale a partir desta revisão: **revisão liberada no TeamCraft é a que vale**.
O git continua guardando a fonte (`.sc`, Markdown, scripts) e o histórico do texto; o
TeamCraft guarda os arquivos publicados, o estado de cada revisão e quem aprovou.

## 2.1 Estados e correspondência com o PLANO

| PLANO (rev. D) | TeamCraft | Significado |
|---|---|---|
| Rascunho | `in_work` | em edição, sob check-out do autor |
| Em revisão | `in_review` | ECO submetida, aguardando parecer |
| Aprovado | `released` (revisão) | revisão liberada; arquivos congelados |
| Publicado | `released` + tag git | pacote `dist/v<versao>/` com manifesto |
| Obsoleto | `obsolete` | substituído por revisão posterior |

# 3. Instalação

## 3.1 Componentes

| Componente | Onde | Versão |
|---|---|---|
| Binário do TeamCraft | `~/teamcraft/teamcraft-0.2.7-linux-x86_64/teamcraft` | 0.2.7 |
| PostgreSQL | contêiner podman `teamcraft-db` (volume `teamcraft-pgdata`) | 16.16 |
| Banco | `127.0.0.1:55432`, base `teamcraft`, usuário `teamcraft` | — |
| Vault de arquivos | `~/teamcraft/data/vault` | — |
| Configuração | `~/teamcraft/teamcraft.env` (modo 600) | — |
| Servidor | `http://127.0.0.1:8080` | 0.2.7 |

O binário foi baixado do release oficial e conferido contra o `SHA256SUMS.txt`:

```sh
sha256sum teamcraft-0.2.7-linux-x86_64.tar.gz
# e98e4481cb658486798fdd68210cd502cf0b43d2ae7aa54b1d7c6d11f4ac3502
```

Não é necessário compilar Rust: o pacote do release já traz o executável e o
`packaging/teamcraft.env` de referência.

## 3.2 Banco de dados

O PostgreSQL roda em podman rootless, publicado só no loopback:

```sh
podman run -d --name teamcraft-db --restart=unless-stopped \
  -e POSTGRES_USER=teamcraft -e POSTGRES_DB=teamcraft \
  -e POSTGRES_PASSWORD="$(cat ~/teamcraft/db_password)" \
  -p 127.0.0.1:55432:5432 \
  -v teamcraft-pgdata:/var/lib/postgresql/data \
  postgres:16-alpine
```

A senha fica em `~/teamcraft/db_password` (modo 600) e é embutida na
`TEAMCRAFT_DATABASE_URL` do `teamcraft.env`.

## 3.3 Configuração

`~/teamcraft/teamcraft.env` (não versionado):

```sh
TEAMCRAFT_BIND_ADDR=127.0.0.1:8080
TEAMCRAFT_PUBLIC_URL=http://localhost:8080
TEAMCRAFT_INSTANCE_NAME="Brasa PLM"
TEAMCRAFT_DATABASE_URL=postgres://teamcraft:<senha>@127.0.0.1:55432/teamcraft
TEAMCRAFT_DB_SSLMODE=disable
TEAMCRAFT_VAULT_DIR=/home/dionarley/teamcraft/data/vault
TEAMCRAFT_MAX_UPLOAD_MB=512
TEAMCRAFT_LOG_FORMAT=text
RUST_LOG=info,tower_http=warn,sqlx=warn
TEAMCRAFT_PREVIEW_MAX_MEMORY_MB=4096
```

`TEAMCRAFT_PREVIEW_MAX_MEMORY_MB=4096` eleva o limite do processo isolado que gera
as malhas de visualização. Mesmo assim o STEP do PS-001 não fecha dentro dos 180 s
do servidor (ver §7.3); o 3MF é o arquivo usado para o preview.

## 3.4 Migrações e usuários

```sh
cd ~/teamcraft
export TEAMCRAFT_ENV_FILE=$PWD/teamcraft.env
./teamcraft-0.2.7-linux-x86_64/teamcraft migrate
```

Dois usuários locais, porque a liberação exige **quatro olhos** (quem libera não
pode aprovar a própria mudança):

| Usuário | Papel | Uso |
|---|---|---|
| `dionarley` | admin | autor; cria itens, envia arquivos, abre a ECO |
| `revisor` | editor | integrante do grupo `PS-001`; aprova a ECO |

```sh
./teamcraft-0.2.7-linux-x86_64/teamcraft user create \
  --username dionarley --display-name "Dionarley" --role admin
./teamcraft-0.2.7-linux-x86_64/teamcraft user create \
  --username revisor --display-name "Revisor PS-001" --role editor
```

Senhas e tokens ficam em `~/teamcraft/credentials.txt` (modo 600). Os tokens usados
por scripts ficam em arquivos separados, também 600: `.admin_token`, `.revisor_token`
e `.mcp_token`.

## 3.5 Subir e conferir

```sh
tools/plm/admin/teamcraft_service.sh up      # banco + servidor
tools/plm/admin/teamcraft_service.sh status  # servidor, banco, contadores e backup
curl -s http://127.0.0.1:8080/readyz
# {"database":"ok","status":"ok","vault":"ok","version":"0.2.7"}
```

O `down` encerra **só** o `teamcraft serve` — o banco continua no contêiner, com
os dados no volume — e o `restart` faz `down + up`. **Nunca** use
`pkill -x teamcraft`: o sinal derruba também a ponte MCP do OpenCode, e as tools
`teamcraft_*` somem até ela reconectar. O `down` encerra com `TERM` e espera o
processo sair; o `up` sobe banco e servidor e espera o servidor responder.

## 3.6 Administração da instância

| Script | Para quê |
|---|---|
| `tools/plm/admin/teamcraft_service.sh` | `up`, `down`, `restart`, `status`, `logs` |
| `tools/plm/admin/teamcraft_branding.sh` | logos do cabeçalho (`branding/`) e nome da instância |
| `tools/plm/admin/teamcraft_tokens.sh` | listar, criar e revogar tokens pessoais |

Os três leem servidor e token de `~/teamcraft/credentials.txt`; exemplos e
detalhes em `tools/plm/admin/README.md`. O upload de logo é rota web e exige
sessão de administrador com `Origin`/`Referer` — o script já cuida disso.

# 4. Acesso

| Recurso | Endereço |
|---|---|
| Interface web | <http://127.0.0.1:8080> |
| API REST | `http://127.0.0.1:8080/api/v1` (Bearer `tc_pat_…`) |
| MCP HTTP | `http://127.0.0.1:8080/api/v1/mcp` (token de escopo `mcp_only`) |
| Saúde | `/healthz` (processo) e `/readyz` (banco + vault) |

A interface web aceita login local. O `dionarley` vê tudo; o `revisor` vê o grupo
`PS-001` e as revisões que precisa aprovar.

Escopos de token usados:

| Token | Escopo | Para quê |
|---|---|---|
| migração | `full` | criar itens, enviar arquivos, abrir e liberar a ECO |
| revisão | `full` | aprovar a ECO como `revisor` |
| OpenCode | `mcp_only` | apenas tools do MCP (leitura, ECR e rascunhos) |

# 5. Operação diária

## 5.1 Check-out e check-in

Toda alteração de arquivo ou BOM começa com a revisão em `in_work` sob check-out do
autor. A interface faz isso pelos botões; via API:

```sh
API=http://127.0.0.1:8080/api/v1
TOK=$(cat ~/teamcraft/.admin_token)

# pegar a revisão mais nova e colocá-la em trabalho
curl -s -X POST -H "Authorization: Bearer $TOK" \
  $API/items/PS-001-DR-001/revisions/latest/revise

# enviar um arquivo (multipart, com pasta e comentário)
curl -s -X POST -H "Authorization: Bearer $TOK" \
  -F file=@dist/v0.19.0/PS-001-US-001_rB_uso.pdf \
  -F 'folders={"PS-001-US-001_rB_uso.pdf":"docs"}' \
  -F comment='manual de uso rev. B' \
  $API/items/PS-001-US-001/revisions/B/files

# devolver sem liberar (opcional)
curl -s -X POST -H "Authorization: Bearer $TOK" \
  $API/items/PS-001-DR-001/revisions/B/checkin
```

Arquivos são imutáveis: reenviar o mesmo nome cria **outra versão** do mesmo
arquivo, com sha256 próprio. O script de migração evita reenvio quando o sha256 já
está presente.

## 5.2 Liberar uma revisão (ECO)

1. Revisões em `in_work` com arquivos, BOM e referências completos.
2. `POST /changes` com título e descrição; `POST /changes/{n}/items` com
   `{"item": "...", "revision": "B"}`.
3. `POST /changes/{n}/reviewers` com o `revisor`.
4. `GET /changes/{n}/readiness`: **bloqueios** impedem a submissão (filho de BOM não
   liberado, documento pendente, etc.); avisos podem ser aceitos.
5. `POST /changes/{n}/submit` → `in_review`; as revisões ficam `in_review`.
6. O `revisor` aprova com `POST /changes/{n}/review`
   `{"decision": "approve", "comment": "..."}` → revisões `released`.
7. Tag git e pacote `dist/v<versao>/` (PLANO §6).

O autor não aprova a própria ECO. O TeamCraft recusa a aprovação de quem tocou nos
dados da mudança.

## 5.3 Pedido de mudança (ECR)

Para um problema ainda não analisado, abra uma ECR (`POST /change-requests`) e
descreva o sintoma com evidência. A ECR é triada por um editor do grupo; aceita,
ela vira ECO. Neste projeto as duas mudanças feitas até agora já estavam analisadas
e foram direto para ECO — o registro está em §7.

# 6. MCP no OpenCode

O OpenCode fala MCP por stdio. A ponte é `~/teamcraft/mcp.sh`:

```sh
#!/bin/sh
export TEAMCRAFT_SERVER="${TEAMCRAFT_SERVER:-http://127.0.0.1:8080}"
export TEAMCRAFT_TOKEN="$(cat "$HOME/teamcraft/.mcp_token")"
exec "$HOME/teamcraft/teamcraft-0.2.7-linux-x86_64/teamcraft" mcp
```

O token tem escopo **`mcp_only`** e fica **fora** do repositório e do config do
OpenCode. O servidor está registrado em `~/.config/opencode/opencode.jsonc`:

```jsonc
"teamcraft": {
  "type": "local",
  "command": ["/home/dionarley/teamcraft/mcp.sh"]
}
```

Conferir a conexão: `opencode mcp list` deve mostrar `teamcraft connected`. As
tools expostas são de leitura e de preparação — `search_items`, `get_item`,
`get_revision`, `get_bom`, `where_used`, `impact_summary`, `read_file_text`,
`my_worklist`, `list_changes`, `get_change`, `suggest_reviewers`, entre outras.
Elas **não** liberam, aprovam nem apagam: essas ações continuam na interface ou na
API com token `full`.

Exemplo de consulta:

```text
search_items {"query": "PS-001"}
→ 24 itens (1 conjunto, 16 peças, 7 documentos), revisões liberadas, projeto PS-001
```

# 7. Mapeamento do PS-001

## 7.1 Grupo e itens

Grupo de projeto `PS-001` — **Brasa**, estanhador 550 W / 127 V, visibilidade
`internal`, membros `dionarley` (gerente) e `revisor`.

| Tipo | Itens | Quantidade |
|---|---|---:|
| Conjunto | `PS-001` | 1 |
| Peças | `PS-001-LM-01` … `PS-001-LM-16` | 16 |
| Documentos | `PS-001-DR-001`, `-US-001`, `-CO-001`, `-PL-001`, `-PL-002`, `-LM-001`, `-PL-003` | 7 |

O conjunto `PS-001` tem no vault: `PS-001.sc`, STEP AP242, 3MF e cinco renders
(`frontal`, `iso`, `perfil`, `topo`, `trafo`). Os documentos têm os PDFs
publicados; o `DR-001` tem também o DXF verificado e o `LM-001` o CSV da BOM.

## 7.2 Estrutura e referências

- BOM do conjunto: 16 linhas, iguais ao `docs/construcao/BOM.csv` (quantidade,
  material, dimensões e volume estão na descrição do item; o corpo do modelo e a
  posição vão na nota da linha).
- Referências do conjunto (revisão A): `DR-001` (drawing) e `US-001`, `CO-001`,
  `PL-001`, `PL-002`, `LM-001` (specification). O `PL-003` entra no registro pelo
  `PL-002` rev. B; a revisão A do conjunto foi liberada antes da existência dele e
  não é reaberta só para criar a referência — o vínculo aparece na próxima revisão
  do conjunto.

## 7.3 Visualização 3D

| Arquivo | Preview | Observação |
|---|---|---|
| `PS-001.3mf` | **sim** (malha 7,5 MB) | usado como visualização do conjunto |
| `PS-001.step` | não | o conversor excede os 180 s e 4 GB do processo de preview |
| `PS-001.sc` | não | formato do SolidCraft; abrir no app |
| PDFs e renders | sim | pré-visualização da página/imagem |

O STEP continua anexado e baixável; só não tem malha gerada. A visualização oficial
é o 3MF, que é derivado da mesma geometria do modelo aprovado.

## 7.4 Liberações

| ECO | Data | Conteúdo | Resultado |
|---|---|---|---|
| `CHG-000001` | 2026-11-14 | 23 revisões A: conjunto, 16 peças, 6 documentos | aprovada pelo `revisor`; tudo `released` |
| `CHG-000002` | 2026-11-14 | `PL-001` B, `PL-002` B, `PL-003` A | aprovada pelo `revisor`; tudo `released` |
| `CHG-000003` | 2026-11-14 | `PS-001` B, `US-001` B, `PL-001` C, `PL-002` C, `PL-003` B e `CO-001` B (regularização) | identidade **Brasa**; aprovada pelo `revisor` |
| `CHG-000004` | 2026-11-14 | `CO-001` C | guia de construção com a identidade Brasa; aprovada pelo `revisor` |

A migração inicial é reproduzível por `tools/plm/teamcraft_migrate.py`; a segunda
liberação, por `tools/plm/teamcraft_docs_b.py`; a identidade própria, por
`tools/plm/teamcraft_identity.py`. Os scripts leem os artefatos de `dist/v<versao>/` e
são idempotentes (não repetem item, arquivo por sha256, linha, referência ou aprovação).

# 8. Backup e restauração

## 8.1 Backup

`tools/plm/teamcraft_backup.sh` gera um pacote com banco e vault:

```sh
tools/plm/teamcraft_backup.sh                 # ~/teamcraft/backups/
tools/plm/teamcraft_backup.sh /mnt/backup     # destino explícito
```

O script:

1. roda `pg_dump -Fc` **dentro do contêiner** (`podman exec teamcraft-db`), porque o
   host não tem `pg_dump`;
2. arquiva `data/vault` em tar (sem o cache `previews/`, que é derivado);
3. grava `SHA256SUMS` e um `README` com data, versão e instruções de restauração;
4. mantém os 7 pacotes mais recentes no destino.

Saída típica:

```
~/teamcraft/backups/teamcraft-20261114T2300.dump
~/teamcraft/backups/teamcraft-20261114T2300-vault.tar.zst
~/teamcraft/backups/teamcraft-20261114T2300.SHA256SUMS
```

## 8.2 Restauração

```sh
tools/plm/admin/teamcraft_service.sh down

# banco: recriar a base e restaurar
podman exec teamcraft-db psql -U teamcraft -d postgres \
  -c 'DROP DATABASE teamcraft WITH (FORCE);' \
  -c 'CREATE DATABASE teamcraft OWNER teamcraft;'
podman exec -i teamcraft-db pg_restore -U teamcraft -d teamcraft --no-owner \
  < teamcraft-20261114T2300.dump

# vault
rm -rf ~/teamcraft/data/vault
tar -C ~/teamcraft/data -xf teamcraft-20261114T2300-vault.tar.zst

# subir e conferir
tools/plm/admin/teamcraft_service.sh up
curl -s http://127.0.0.1:8080/readyz
```

Conferir depois: `/api/v1/items?project=PS-001`, `vault check` e a abertura de um
PDF do `DR-001`. O cache de previews se refaz sozinho na primeira visualização.

# 9. Segurança e limites

- O servidor escuta **só** em `127.0.0.1`; não há TLS, proxy reverso nem acesso
  externo. Para uso em rede seria necessário TLS, política de senhas e backup
  remoto — nada disso está configurado.
- Tokens e senhas ficam em arquivos `600` fora do git. O token do MCP não pode
  escrever dados liberados.
- O TeamCraft 0.2.7 é software em desenvolvimento; a liberação registrada aqui não
  substitui revisão humana. O PS-001 continua sendo **estudo não certificado**, em
  127 V — ver `LEGAL.md` e o `US-001`.
- O vault cresce com cada versão de arquivo; não há expurgo automático. Rodar
  `teamcraft vault gc --apply` só depois de conferir a lista e com backup recente.

# 10. Checklist rápido

- [ ] `readyz` responde `database` e `vault` ok.
- [ ] Revisão em `in_work` sob check-out do autor.
- [ ] Arquivo novo com sha256 diferente do já anexado.
- [ ] BOM e referências completos antes de submeter a ECO.
- [ ] `readiness` sem bloqueios.
- [ ] ECO aprovada por usuário diferente do autor.
- [ ] Tag git e `dist/v<versao>/` com manifesto conferido.
- [ ] Backup do dia gerado e testado.

# 11. Histórico deste documento

| Rev. | Data | Mudança |
|---|---|---|
| A | 2026-11-14 | primeira emissão: instalação 0.2.7, operação, MCP, migração do PS-001 e backup |
| B | 2026-11-14 | identidade **Brasa**: instância, grupo e ECO 3; exemplo de consulta com 24 itens |
| C | 2026-11-15 | scripts de administração (`tools/plm/admin/`) no lugar do `pkill`; nova seção 3.6 e restauração pelo serviço |
