# Visualizador DXF — desenhos do Brasa no navegador

O [MLightCAD](https://github.com/mlightcad/cad-viewer) é um visualizador de
DXF/DWG que roda inteiramente no navegador (parsing, geometria e render em
WebGL, sem backend). Aqui ele aparece como um app mínimo deste projeto: abre os
DXF do Brasa, deixa dar zoom, medir e ligar/desligar camadas.

Só **DXF** é habilitado de propósito. O pacote de render é MIT; o suporte a DWG
do MLightCAD depende do LibreDWG, que é GPL — não entra neste projeto.

## O que tem aqui

| Arquivo | O que é |
|---|---|
| `package.json` | app Vite + `@mlightcad/cad-simple-viewer` 1.7.8 (pacotes publicados no npm, sem clonar o repositório) |
| `src/main.ts` | instância do visualizador, abertura por arquivo, por `?file=` e pelos desenhos publicados |
| `index.html`, `src/style.css` | a página e a identidade Brasa |
| `install.sh` | npm install + build no podman (Node 22) e sobe o nginx |
| `cad_viewer.sh` | `view`, `publish`, `up/down/status/logs`, `build` |
| `compose.yaml`, `nginx.conf` | serviço em `127.0.0.1:8089`; `drawings/` montado em `/srv/drawings` |
| `drawings/` | DXF publicados + `index.json` (fora do git) |

## Instalar e subir

```sh
tools/cad-viewer/install.sh              # build + up, porta 8089
tools/cad-viewer/cad_viewer.sh status
```

O build roda em `node:22-alpine` com o projeto montado e o usuário do host
(`keep-id`), então `node_modules/` e `dist/` saem com o seu dono. O `install.sh`
recria o contêiner a cada execução porque `dist/` é substituído.

## Abrir um desenho

```sh
# copia o DXF para drawings/, sobe o serviço se preciso e abre no navegador
tools/cad-viewer/cad_viewer.sh view ../dist/v0.19.0/PS-001-DR-001_rA_prancha-a2.dxf

# publica todos os DXF de uma pasta (ex.: as projeções do modelo)
tools/cad-viewer/cad_viewer.sh publish ../out/draw/v017
```

No navegador (<http://127.0.0.1:8089>) também dá para:

- **arrastar** um `.dxf` para a janela;
- **Abrir DXF…** no botão do topo;
- escolher um **desenho publicado** na lista, alimentada por `drawings/index.json`.

O arquivo é lido localmente: nada é enviado para servidor (o nginx só entrega
estático). `drawings/` e `dist/` não entram no git.

## Detalhes

- **Fontes e blocos de título:** vêm do CDN público `mlightcad/cad-data` (mesmo
  caminho do demo oficial), porque o pacote não as embute. Sem rede, o desenho
  abre com os glifos de fallback. Para uso offline, sirva os arquivos e construa
  com `VITE_CAD_BASE_URL=https://.../cad-data/`.
- **MTEXT** é desenhado na thread principal (`useMainThreadDraw`); o worker
  `dist/workers/mtext-renderer-worker.js` é copiado no build e fica disponível,
  mas não é o caminho padrão.
- **Leitura apenas:** o documento abre em `AcEdOpenMode.Read`; a barra de
  comandos do visualizador serve para zoom, medida, camadas e seleção, não para
  editar o desenho.
- **Porta** 8089 só em `127.0.0.1`; `CAD_VIEWER_PORT` muda. Não há unit systemd:
  depois de reiniciar a máquina, `cad_viewer.sh up`.
- **Licenças:** o app usa pacotes MIT do MLightCAD; o DXF é do próprio projeto
  (ver `../../LEGAL.md`). O código do visualizador não é redistribuído aqui —
  `node_modules/` e `dist/` ficam fora do git.

## No fluxo do projeto

- **Conferir o desenho:** abrir o DXF da prancha (`dist/v<versão>/`) antes de
  gerar o PDF, ou as projeções de `out/draw/` durante o trabalho no modelo.
- **Revisar marcas e camadas:** ligar/desligar camadas e medir no navegador é
  mais rápido que reabrir o CAD para uma dúvida.
- **Não é fonte de verdade:** o desenho vale pelo que está no modelo/DXF
  versionado; o visualizador é só leitura. A prancha 2D continua sendo gerada
  por `tools/draw/sheet.py` e liberada por `tools/plm/build.sh`.
