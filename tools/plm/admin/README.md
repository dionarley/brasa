# Administração do TeamCraft (Brasa PLM)

Scripts para operar a instância local do TeamCraft que guarda o projeto `PS-001`:
subir/derrubar o serviço, trocar os logos e o nome do cabeçalho, e cuidar dos
tokens de acesso. Todos são bash + `curl` + `python3`, sem dependência Python do
projeto, e leem a configuração de `~/teamcraft` (sobrescrevível por variável de
ambiente).

| Script | Para quê |
|---|---|
| [`teamcraft_service.sh`](teamcraft_service.sh) | `up`, `down`, `restart`, `status`, `logs [N]` |
| [`teamcraft_branding.sh`](teamcraft_branding.sh) | `status`, `upload`, `reset`, `name` |
| [`teamcraft_tokens.sh`](teamcraft_tokens.sh) | `list`, `new`, `revoke` |

O backup fica um nível acima, em [`../teamcraft_backup.sh`](../teamcraft_backup.sh).

## Ambiente

| Variável | Padrão | Uso |
|---|---|---|
| `TEAMCRAFT_HOME` | `~/teamcraft` | pasta com binário, `teamcraft.env`, log, `data/vault` e `backups/` |
| `TEAMCRAFT_SERVER` | `http://127.0.0.1:8080` | endereço da instância |
| `TEAMCRAFT_CREDENTIALS` | `$TEAMCRAFT_HOME/credentials.txt` | usuário, senha e tokens de administrador |
| `TEAMCRAFT_TOKEN` | `admin_token` do arquivo | token usado pelo `teamcraft_tokens.sh` |
| `TEAMCRAFT_DB_CONTAINER` | `teamcraft-db` | contêiner podman do PostgreSQL |
| `BRASA_BRANDING_DIR` | `branding/` do projeto | onde estão `brasa-wide.svg` e `brasa-square.svg` |

`credentials.txt` não é versionado. Formato: `chave=valor` por linha, com
`admin_user`, `admin_password`, `admin_token` (e as contas de revisor/MCP, que
estes scripts não usam).

## Serviço

```sh
tools/plm/admin/teamcraft_service.sh status
tools/plm/admin/teamcraft_service.sh up
tools/plm/admin/teamcraft_service.sh logs 60
tools/plm/admin/teamcraft_service.sh restart
```

- `up` sobe o contêiner do banco se preciso, espera o `pg_isready` e inicia
  `teamcraft serve` com o `teamcraft.env`, anexando ao `teamcraft.log`. Se o
  servidor já responde, não faz nada.
- `down` encerra **só** o servidor (`SIGTERM`) e deixa o banco rodando; o `up`
  seguinte é rápido. Os dados ficam no volume do podman.
- `status` confere servidor, versão pela API, banco e contadores (itens,
  revisões, ECOs, grupos), tamanho do vault e último backup. Sai com código 1 se
  o servidor não responde.
- `restart` é `down` + `up`.

O processo é localizado por `pgrep -f '(^|/)teamcraft serve'`. **Nunca** use
`pkill -x teamcraft` ou mate o contêiner: a ponte MCP do OpenCode também roda
como `teamcraft` e cai junto. O `down` daqui não a atinge.

Se o banco não subir, `logs` mostra a mensagem de conexão recusada; o TeamCraft
tenta reconectar por 20 s antes de desistir.

## Branding

```sh
tools/plm/admin/teamcraft_branding.sh status
tools/plm/admin/teamcraft_branding.sh upload          # wide + square
tools/plm/admin/teamcraft_branding.sh upload square --file marca.png
tools/plm/admin/teamcraft_branding.sh reset wide
tools/plm/admin/teamcraft_branding.sh name --display "Brasa PLM" --subtitle PLM
```

- `status` mostra nome/subtítulo e, por slot, o token sha do logo no servidor
  comparado com o arquivo local (`igual ao arquivo local` ou `difere`).
- `upload` é idempotente: se o sha256 do arquivo já é o do servidor, não envia
  nada. O tipo é detectado pelos bytes (PNG, JPEG, WebP, SVG), como o TeamCraft
  faz; limites: 512 KiB, 4096 px por lado, SVG sem script/link externo.
- A rota é web (`POST /admin/branding/{kind}`), então o script faz login com
  `admin_user`/`admin_password` e envia `Origin` e `Referer` — sem eles o
  servidor responde **403**. O cookie de sessão fica num arquivo temporário.
- `reset` volta ao logo embutido do TeamCraft. `name` grava o cabeçalho e, se um
  campo for omitido, mantém o valor atual; com os dois iguais, não escreve.
- Os logos ficam em `branding_logos` no banco e entram no backup. As fontes e os
  exports estão em [`../../branding/`](../../branding/README.md).

## Tokens

```sh
tools/plm/admin/teamcraft_tokens.sh list
tools/plm/admin/teamcraft_tokens.sh new --name "CI" --scope read_only --days 90
tools/plm/admin/teamcraft_tokens.sh revoke --name "CI"
tools/plm/admin/teamcraft_tokens.sh revoke --id 4ded81ef-433d-46e7-9d47-1aa738cd8d11
```

- `list` mostra nome, escopo, prefixo, criação, validade e id (nunca o valor).
- `new` imprime o token **uma vez** no stdout; os metadados vão para o stderr,
  então dá para capturar só o valor: `TOKEN=$(... new --name CI 2>/dev/null)`.
  Escopos: `full` (lê, escreve, aprova), `write`, `read_only`, `mcp_only`;
  `--days` ausente = sem validade.
- `revoke` aceita `--id` ou `--name` (o nome precisa ser único).
- O token que autentica estes comandos precisa de escopo `full` ou `write`; um
  token `mcp_only` recebe 403 em `/api/v1/tokens`.

## Ordem de operação

1. `teamcraft_service.sh status` — servidor e banco no ar.
2. `teamcraft_branding.sh status` — o que a instância mostra hoje.
3. Mudança de logo/nome ou token.
4. `../teamcraft_backup.sh` — o backup leva banco (logos, tokens, ECOs) e vault.
5. `git status` no projeto: o que é conteúdo versionado entra em commit próprio.

Os scripts não alteram a forma do produto: logo e administração da instância não
são revisão de peça. Mudança de documentação é commit (e `build.sh` para o PDF);
revisão de peça e conjunto é ECO no TeamCraft — a fronteira está em
[`../../docs/plm/PLANO.md`](../../docs/plm/PLANO.md) §1.
