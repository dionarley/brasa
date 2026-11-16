# Documentação do Brasa (Docusaurus)

O site publica os documentos do projeto — os mesmos Markdown que
`tools/plm/build.sh` transforma em PDF. Não existe conteúdo próprio do site: a
fonte única continua em [`../docs/`](../docs) e no [`../LEGAL.md`](../LEGAL.md).

## O que tem aqui

| Arquivo | O que é |
|---|---|
| `docusaurus.config.js` | raiz do conteúdo em `..`, só `docs/**/*.md` e `LEGAL.md`, navbar/footer/cores |
| `sidebars.js` | ordem: uso e segurança, construção, PLM, referências, projeto e direitos |
| `plugins/remark-doc-images.js` | `renders/*.png` → `/renders/*.png` e `{width=NN%}` → `style="width: NN%"` |
| `src/pages/index.js` | página inicial com o logo e os cartões dos documentos |
| `docs.sh` | build/serve/dev do site no podman (Node 22) |
| `compose.yaml`, `nginx.conf` | site em `127.0.0.1:8081` |

## Publicar

```sh
site/docs.sh build      # renders da última liberação + npm ci + build
site/docs.sh serve      # build e sobe o site em 127.0.0.1:8081
site/docs.sh status
site/docs.sh dev        # servidor de desenvolvimento em 127.0.0.1:8082
```

O build roda em `node:22-alpine` com a raiz do projeto montada em `/repo` e o
usuário do host (`keep-id`): `node_modules/`, `build/` e `.npm/` saem com o seu
dono e ficam fora do git.

## Como o conteúdo entra

- `path: '..'` com `include: ['docs/**/*.md', 'LEGAL.md']`: o site publica os
  documentos a partir da raiz do projeto, então os links relativos dos manuais
  (`../../LEGAL.md`) continuam válidos. PDFs, TXT e CSV ficam de fora.
- `USO.md` dentro de `docs/uso/` e `CONSTRUCAO.md` dentro de `docs/construcao/`
  são índices de categoria para o Docusaurus: as rotas são `/docs/uso/` e
  `/docs/construcao/` (e não `/docs/uso/USO`).
- `markdown.format: 'md'` é obrigatório: os manuais usam a sintaxe do pandoc
  (`{width=58%}`), que quebraria o MDX. O plugin remark converte depois.
- As figuras apontam para `renders/*.png`, que só existem em
  `dist/v<versão>/renders/` (fora do git). `docs.sh build` copia os da última
  liberação para `static/renders/`; sem eles o build avisa e as imagens faltam.
- O `LICENSE` da raiz é copiado para `static/LICENSE` no build (o `LEGAL.md`
  aponta para ele) e servido como texto puro pelo nginx.

**Nada de conteúdo é editado aqui.** Corrigir texto ou figura é mudar `docs/`, num
commit: o site reflete o que estiver nos documentos e o PDF sai da mesma fonte.

## Limites

- Sem edição: o site é somente leitura e é derivado do commit (não há banner de
  documento controlado nem revisão de texto).
- O verificador de links do Docusaurus ainda avisa do link `LEGAL.md` → `LICENSE`:
  o arquivo é servido em `/LICENSE`, mas fora do grafo de rotas. O build segue
  verde (`onBrokenLinks: 'warn'`) e o link funciona.
- Ainda não há publicação externa: o alvo é local (`127.0.0.1:8081`). Para um
  host real, trocar `url`/`baseUrl` em `docusaurus.config.js` e servir `build/`
  por HTTPS.
- Sem unit systemd: depois de reiniciar a máquina, `site/docs.sh up`.
