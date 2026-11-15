# GridCraft — planilhas do Brasa

O [GridCraft](https://github.com/storytold/gridcraft) é a planilha do fluxo: serve
para listas de materiais, cálculos de conferência e relatórios em `.xlsx`. Roda
como serviço web no podman (site estático) e como CLI headless em um contêiner,
no mesmo motor de comandos do app.

## O que tem aqui

| Arquivo | O que é |
|---|---|
| `install.sh` | baixa e verifica o pacote oficial, extrai o site e a CLI, constrói a imagem e sobe o serviço |
| `gridcraft.sh` | uso diário: `up`, `down`, `status`, `logs`, `cli …`, `mcp` |
| `compose.yaml` | serviço `web` (nginx) na porta 8088 do host |
| `nginx.conf` | MIME de `.wasm`, gzip e cache do pacote web |
| `Containerfile.cli` | imagem da CLI (`debian:bookworm-slim` + binário) |
| `.cache/`, `web/`, `bin/` | resultado do install (fora do git) |

## Instalar e subir

```sh
tools/gridcraft/install.sh              # 0.19.1, porta 8088
tools/gridcraft/gridcraft.sh status
tools/gridcraft/gridcraft.sh logs 20
```

O `install.sh`:

1. baixa `gridcraft-web-<versão>.zip`, `gridcraft-<versão>-linux-x86_64.tar.gz` e
   `SHA256SUMS.txt` da release oficial;
2. confere a assinatura do `SHA256SUMS.txt` com a chave de release e o
   fingerprint fixado no script (`2B76741B…C3ED`) e depois os sha256 dos dois
   arquivos;
3. extrai o site em `web/` (26 MB) e o `gridcraft-cli` em `bin/`;
4. constrói `localhost/gridcraft-cli:<versão>` e sobe `gridcraft-web` com
   `podman-compose`;
5. espera o `index.html` responder e imprime a URL.

Repetir o comando é seguro: download no `.cache`, extração refeita, serviço
atualizado. Para outra versão: `GRIDCRAFT_VERSION=0.20.0 tools/gridcraft/install.sh`.

## Web

<http://127.0.0.1:8088> — abre direto no navegador; abrir e salvar arquivos é
local, sem servidor de arquivos. Como é um site estático (WASM), o contêiner não
guarda estado: os arquivos abertos ficam no seu computador.

```sh
tools/gridcraft/gridcraft.sh up|down|restart|status|logs [N]|url|open
```

`up` é idempotente e `down` só para o serviço web (a imagem e o site ficam).
Depois de reiniciar a máquina, rode `gridcraft.sh up` de novo: como no TeamCraft,
não há unit systemd; o `restart: unless-stopped` do compose só vale enquanto o
podman da sessão está de pé.

## CLI (headless)

O atalho monta a raiz do projeto em `/repo` (diretório de trabalho) e roda como o
seu usuário, então os caminhos são os mesmos do host e os arquivos saem com o seu
dono:

```sh
tools/gridcraft/gridcraft.sh cli info workbooks/orcamento.xlsx
tools/gridcraft/gridcraft.sh cli cat workbooks/orcamento.xlsx --range A1:F20
tools/gridcraft/gridcraft.sh cli eval '=SUM(C2:C9)' --in workbooks/orcamento.xlsx
tools/gridcraft/gridcraft.sh cli convert workbooks/orcamento.xlsx /tmp/orcamento.csv
tools/gridcraft/gridcraft.sh cli run --script passos.jsonl --out workbooks/novo.xlsx
```

Subcomandos: `info`, `convert`, `eval`, `cat`, `check`, `run`, `commands`,
`functions`, `mcp`, `send`. A ajuda completa sai de
`gridcraft.sh cli --help` (ou da [documentação da CLI](https://github.com/storytold/gridcraft/blob/main/docs/cli.md)).

## MCP no OpenCode

O servidor MCP roda em stdio dentro do contêiner, com o projeto montado:

```jsonc
// ~/.config/opencode/opencode.jsonc
"gridcraft": {
  "type": "local",
  "command": [
    "/home/dionarley/codes-area/diy_hot_gun/tools/gridcraft/gridcraft.sh",
    "mcp"
  ]
}
```

Com isso o agente abre, lê, escreve e formata planilhas pelas tools `gridcraft`
(`open_workbook`, `read_range`, `set_cell`, `execute_command`, …). Para começar
com um arquivo aberto: `gridcraft.sh mcp --in workbooks/orcamento.xlsx`.

## No fluxo do projeto

- **Rascunho local:** planilhas em [`../../workbooks/`](../../workbooks/README.md),
  fora do git.
- **Cálculo e conferência:** `cli eval` testa uma fórmula sem alterar a planilha;
  `cli check` compara valores em cache com o recálculo.
- **Entrega controlada:** o `.xlsx` que vale vira arquivo de um item no TeamCraft
  (check-in com revisão), como os PDFs — o histórico fica no PLM, não no git.
  Ver [`../../docs/plm/TEAMCRAFT.md`](../../docs/plm/TEAMCRAFT.md), §5.1.
- **Relatório:** `cli convert … saida.csv|html|pdf` para anexar ou publicar.

## Limites e cuidados

- O pacote é o oficial do GitHub (MIT/Apache-2.0); o script recusa assinatura
  inválida. Atualização é trocar a versão e rodar o `install.sh` de novo.
- A porta 8088 é só em `127.0.0.1`; nada é exposto na rede.
- O `web/` é o site inteiro (26 MB) e o `bin/gridcraft-cli` tem 18 MB; ambos
  ficam fora do git. O `.cache/` guarda os downloads (60 MB) para reinstalar sem
  baixar de novo; pode apagar quando não precisar.
- O serviço não tem volume de dados: não há nada a fazer backup. Planilhas são
  arquivos do projeto.
