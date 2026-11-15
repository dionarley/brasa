# Brasa — estanhador 550 W / 127 V (estudo)

<p align="center"><img src="branding/brasa-wide.svg" alt="Brasa — estanhador 550 W / 127 V" height="96"></p>

**Licença:** [CC BY-NC-SA 4.0](LICENSE) (conteúdo próprio) · **Versão:** 0.20.0 ·
**Estado:** modelo 3D aprovado; documentação de produto publicada; prancha 2D A2
publicada; revisões liberadas no TeamCraft.

O **Brasa** é a reconstrução **de estudo** de um estanhador de 550 W / 127 V com
transformador e secundário de fita de cobre, modelado como peça paramétrica no SolidCraft
a partir de fotos públicas, artigos e teoria de transformadores. `PS-001` é o código
interno do projeto. Não é projeto de fabricação, não é peça de reposição e não tem
vínculo com o fabricante do produto original — leia [LEGAL.md](LEGAL.md) antes de
reutilizar qualquer coisa.

## Estado atual

| Entrega | Situação |
|---|---|
| Modelo 3D paramétrico (`cad/solidcraft/PS-001.sc`) | **aprovado** — 22 corpos, 0 erros, 448,4 cm³ |
| Renders de conferência (`out/plot/ps001_v15_*.png`) | gerados (não versionados) |
| Exportações STEP/3MF | **regeradas** da versão aprovada (derivadas, fora do git) |
| Prancha 2D A2 (`PS-001-DR-001` rev. A) | **publicada** — vistas em 1º diedro, detalhe 1:1, cotas de envelope, BOM |
| Documentação PLM (`docs/plm/`, `docs/uso/`, `docs/construcao/`) | **publicada** — plano, registro, uso e construção |
| PDM TeamCraft (`http://127.0.0.1:8080`) | **em uso** — 24 itens, BOM e arquivos liberados por ECO |
| Versionamento e licença | concluído |

## Estrutura

```
cad/solidcraft/
  PS-001.sc        fonte da verdade: design paramétrico (zip com document.json)
docs/
  plm/             plano do ciclo de vida (PLANO.md), registro mestre (REGISTRO.md)
                   e manual do TeamCraft (TEAMCRAFT.md)
  uso/             manual de uso e segurança (USO.md)
  construcao/      guia de construção (CONSTRUCAO.md) e lista de materiais (BOM.csv)
  referencias.md   fontes, autoria e o que cada uma contribuiu
tools/plm/
  build.sh         gera os PDFs (pandoc → typst) e o pacote em dist/
  template.typ     template de documento (capa, cabeçalho, rodapé)
  teamcraft_migrate.py  migra o PS-001 para o TeamCraft (idempotente)
  teamcraft_docs_b.py   libera PL-001 B, PL-002 B e PL-003 A
  teamcraft_identity.py libera a identidade Brasa (PS-001 B, US-001 B, PL-001/PL-002 C, PL-003 B)
  teamcraft_tools.py    libera as revisões de processo da 0.20.0 (PL-001/PL-002 D, PL-003 C)
  teamcraft_backup.sh   backup do banco e do vault
  admin/
    teamcraft_service.sh   sobe, derruba e diagnostica servidor e banco
    teamcraft_branding.sh  logos e nome do cabeçalho da instância
    teamcraft_tokens.sh    tokens pessoais de acesso (listar, criar, revogar)
tools/draw/
  sheet.py         monta a prancha A2 a partir das projeções DXF do modelo
tools/gridcraft/
  install.sh       instala o GridCraft no podman (site web + CLI) com assinatura conferida
  gridcraft.sh     up/down/status/logs, CLI headless e MCP em stdio
  compose.yaml     serviço web (nginx, 127.0.0.1:8088)
tools/cad-viewer/
  install.sh       constrói o visualizador DXF (Vite + MLightCAD no podman) e sobe
  cad_viewer.sh    view/publish de DXF, up/down/status/logs
  compose.yaml     serviço web (nginx, 127.0.0.1:8089)
workbooks/         planilhas de trabalho (fora do git; arquivo controlado vai ao TeamCraft)
site/              documentação publicada em Docusaurus (lê docs/ e LEGAL.md)
branding/
  build.sh         regera os exports do logo (VectorCraft, flatpak)
  brasa-wide.*     logo 600 × 120 px: fonte .vectorcraft, SVG e PNG
  brasa-square.*   marca 256 × 256 px: fonte .vectorcraft, SVG e PNG
out/               renders, DXF e exportações (fora do git)
dist/              pacotes de liberação gerados (fora do git)
ref/               fotos e vetores de referência (fora do git, direitos de terceiros)
LEGAL.md           escopo da licença, marcas, desenho industrial, segurança
CHANGELOG.md       histórico por versão
```

## Plataforma (Forja)

As ferramentas não moram neste repositório: os apps (SolidCraft, CadCraft,
GridCraft, visualizador DXF) e o serviço de PDM vivem na plataforma
[`dionarley/forja`](https://github.com/dionarley/forja), com os forks em
submodules. Aqui fica o **produto**: modelo, desenhos, documentos e os scripts
que agem no PDM.

| ferramenta | onde | o que faz com o PS-001 |
|---|---|---|
| `forja-pdm` | `dionarley/forja`, `127.0.0.1:8090` | abre o STEP do TeamCraft e tessela com o kernel `solidcore` (22 corpos, ~32,6 mil triângulos) |
| [Gabarito](https://github.com/dionarley/gabarito) | `dionarley/gabarito` | molde para produto novo; o PS-001 é anterior a ele |
| TeamCraft | local, `127.0.0.1:8080` | itens, revisões, ECO e arquivos |

A marca que assina contrato, laudo e proposta é a **Tessera**; **Brasa** é a
marca deste produto.

## Modelo 3D

Um design no SolidCraft, sem montagem separada: cada peça é um corpo nomeado, com
histórico paramétrico. Medidas do `measure` atual:

| Peça(s) | Qtd. | Volume (cm³) | Observação |
|---|---:|---:|---|
| `Nucleo` | 1 | 148,90 | EI-75, 75 × 75 × 35 mm, janela 12,5 × 50 |
| `Bobina` | 1 | 23,44 | carretel: alma 33 × 43 e flanges 37 × 47 × 3 |
| `Secundario` | 1 | 10,26 | tira 2 × 9 mm, 2,5 voltas, sweep único |
| `Ponta_U` | 1 | 2,39 | tubo Ø4,5 + pastilhas de fixação (X 34…52) |
| `Cabo` | 1 | 215,00 | loft "cabeça de prego", 10 seções |
| `Chave`, `Tecla` | 2 | 9,52 | na face +Y do cabo |
| `Fio_primario` | 1 | 0,66 | enterrado no cabo |
| `Prensa_cabo`, `Cabo_forca` | 2 | 6,39 | saída pela base |
| `Canto_*` | 4 | 22,24 | cantoneiras do transformador |
| `Parafuso_canto_*` | 4 | 7,36 | M5 passante |
| `Parafuso_ponta_*`, `Porca_ponta_*` | 4 | 2,26 | fixação das postas, em X 46 |
| **Total** | **22** | **448,4** | |

Envelope: X −52,2…+96,1 · Y ±26,1 · Z −273,7…+39 mm (≈ 148 × 52 × 313 mm).

> A massa mostrada pelo CAD (~594 g) usa a densidade padrão de 1,29 g/cm³ para todos os
> corpos; não representa a peça real. Atribuir densidade por material é pendência.

### Transformador

Núcleo EI-75 de catálogo: perna 12,5 mm, janela 12,5 × 50 mm, pacote 35 mm
(75 × 75 × 35). Volume do transformador montado: **201,1 cm³** (+14,4 % sobre a versão
EI-57, que tinha 175,7 cm³).

### Secundário

Uma tira única de cobre de 2 × 9 mm que dá 2,5 voltas em hélice (passo 12,8 mm) em volta
do núcleo, entra na face +Y em Z +16, desce e sai na face −Y em Z −16, terminando nos
braços em "S" que alimentam as postas. Modelada como **um sweep e um corpo** — foi a
forma de garantir continuidade elétrica e evitar uniões por faces coincidentes.

As duas pontas (entrada e saída) contornam o grampo do lado da ponteira por fora, em
X = 31,7 (face externa do grampo em 29,67), com 1 mm de folga; o resto da hélice passa
pelas duas janelas do núcleo (X 9,17 e −30,83) sem tocar em núcleo, carretel ou grampos.

## Parâmetros principais

| Item | Valor |
|---|---|
| Núcleo | EI-75: 75 × 75 × 35 mm, janela 12,5 × 50, perna 12,5 |
| Primário | ~700 espiras AWG 28 (127 V) em carretel 37 × 47 × 44 (alma 33 × 43, flanges 3) |
| Secundário | 2,5 voltas de fita Cu 2 × 9 mm, passo 12,8 |
| Ponta | tubo Cu Ø4,5 (parede 0,75), em U, X 34…96,1 |
| Fixação das postas | parafuso M5 em X 46, furo Ø6,2 |
| Cantoneiras | 4 ×, 15,5 × 13 × 75, parafusos M5 passantes |
| Cabo | madeira, loft de 10 seções, ~167 mm, topo largo |
| Chave | bezel 7 × 28 × 37, tecla 5,5 × 18 |

## Documentação

Os documentos são escritos em Markdown (fonte única) e os PDFs são **gerados**. O
processo — códigos, estados, critérios de aprovação e liberação — está em
[`docs/plm/PLANO.md`](docs/plm/PLANO.md); o índice controlado em
[`docs/plm/REGISTRO.md`](docs/plm/REGISTRO.md).

| Código | Documento | Fonte |
|---|---|---|
| PS-001-PL-001 | Plano de ciclo de vida (PLM) | [`docs/plm/PLANO.md`](docs/plm/PLANO.md) |
| PS-001-PL-002 | Registro mestre de documentos | [`docs/plm/REGISTRO.md`](docs/plm/REGISTRO.md) |
| PS-001-PL-003 | TeamCraft: instalação, operação e registro | [`docs/plm/TEAMCRAFT.md`](docs/plm/TEAMCRAFT.md) |
| PS-001-US-001 | Manual de uso e segurança | [`docs/uso/USO.md`](docs/uso/USO.md) |
| PS-001-CO-001 | Guia de construção (estudo) | [`docs/construcao/CONSTRUCAO.md`](docs/construcao/CONSTRUCAO.md) |
| PS-001-LM-001 | Lista de materiais (BOM) | [`docs/construcao/BOM.csv`](docs/construcao/BOM.csv) |
| PS-001-DR-001 | Prancha 2D A2 (conjunto geral) | `out/draw/v017/` (gerada por `tools/draw/sheet.py`) |

Gerar o pacote de liberação (PDFs, BOM e renders com manifesto `sha256`):

```sh
tools/plm/build.sh                  # dist/v0.20.0/
tools/plm/build.sh --pdf            # só os PDFs
tools/plm/build.sh --clean          # limpa dist/ antes
```

Requer `pandoc` e `typst`. Os renders vêm da pasta mais recente em `out/plot/`; se
faltarem, o PDF sai com uma nota no lugar da figura em vez de quebrar.

A mesma fonte é publicada como site (Docusaurus) em <http://127.0.0.1:8081>:
`site/docs.sh build` (ou `serve`) gera e sobe; nada é editado em `site/`, o site
só lê `docs/` e `LEGAL.md`. Ver [`site/README.md`](site/README.md).

## PDM (TeamCraft)

As revisões liberadas ficam em uma instância local do
[TeamCraft](https://github.com/rudalabs/TeamCraft) em <http://127.0.0.1:8080>
(somente loopback), com o grupo de projeto `PS-001`:

- 1 conjunto (`PS-001`), 16 peças (`PS-001-LM-01`…`-16`) e 7 documentos;
- BOM de 16 linhas e arquivos do modelo (`.sc`, STEP, 3MF, renders) na revisão do
  conjunto;
- liberação por ECO aprovada por um segundo usuário (`revisor`): `CHG-000001` levou as
  23 revisões A, `CHG-000002` liberou `PL-001`/`PL-002` rev. B e `PL-003` rev. A, e
  `CHG-000003` liberou a identidade **Brasa** (`PS-001` B, `US-001` B, `PL-001`/`PL-002`
  C, `PL-003` B, `CO-001` B) e `CHG-000004` fechou o `CO-001` C.

A instalação, a operação, o MCP do OpenCode e o backup estão em
[`docs/plm/TEAMCRAFT.md`](docs/plm/TEAMCRAFT.md). Backup manual:

```sh
tools/plm/teamcraft_backup.sh          # banco + vault em ~/teamcraft/backups/
```

## Planilhas (GridCraft)

O [GridCraft](https://github.com/storytold/gridcraft) roda no podman: site em
<http://127.0.0.1:8088> e CLI headless (também MCP) no mesmo motor. Serve para
listas, orçamento e conferência de cálculo; o arquivo que vale é entregue como
revisão no TeamCraft, como os PDFs.

```sh
tools/gridcraft/install.sh             # baixa, confere a assinatura e sobe o serviço
tools/gridcraft/gridcraft.sh status
tools/gridcraft/gridcraft.sh cli info workbooks/orcamento.xlsx
tools/gridcraft/gridcraft.sh cli eval '=SUM(C2:C9)' --in workbooks/orcamento.xlsx
```

Planilhas de trabalho ficam em [`workbooks/`](workbooks/README.md), fora do git.
Instalação, CLI, MCP e limites em
[`tools/gridcraft/README.md`](tools/gridcraft/README.md).

## Desenhos (visualizador DXF)

O [MLightCAD](https://github.com/mlightcad/cad-viewer) roda como app estático no
podman: <http://127.0.0.1:8089> abre DXF no próprio navegador (parsing e render
em WebGL), com zoom, medida e camadas — sem CAD instalado e sem enviar arquivo
para servidor. Serve para conferir a prancha e as projeções durante o trabalho.

```sh
tools/cad-viewer/install.sh            # build do app (Node no podman) + serviço
tools/cad-viewer/cad_viewer.sh view dist/v0.20.0/PS-001-DR-001_rA_prancha-a2.dxf
tools/cad-viewer/cad_viewer.sh publish out/draw/v017
```

Só DXF: o suporte a DWG usa LibreDWG (GPL), que fica fora do projeto. Detalhes,
fontes do CDN e limites em [`tools/cad-viewer/README.md`](tools/cad-viewer/README.md).

## Abrir e editar

Requer o SolidCraft (app desktop) ou o servidor MCP equivalente. O `.sc` é um zip com
`document.json`:

```sh
unzip -l cad/solidcraft/PS-001.sc        # conteúdo
unzip -p cad/solidcraft/PS-001.sc document.json | head -c 400
```

Ao editar: mantenha os nomes dos corpos, use expressões nos campos que devem seguir
parâmetros, e feche cada sketch com `dof 0`. Depois de qualquer mudança, confira com
`measure` (volume e envelope) e gere os renders de conferência.

## Versionamento

- Repositório git **dentro de `brasa/`** (branch `main`); tags `v0.x.y`.
- `PS-001.sc` é gravado pelo SolidCraft como zip: o diff não é legível, então o
  histórico útil é o par **(commit + tag)**; para inspecionar uma versão, faça checkout
  da tag e abra o `.sc`.
- Fora do git (`.gitignore`): `out/` (renders, DXF, STEP/3MF), `ref/` e `docs/*.pdf`
  (direitos de terceiros), backups `.bak`/`*_backup.sc`, `render.png`, `shot*.png`,
  `workbooks/*.xlsx`, o que o `tools/gridcraft/install.sh` baixa (`web/`, `bin/`,
  `.cache/`) e o build do visualizador (`tools/cad-viewer/{node_modules,dist,drawings}`).
- Commits em português, no imperativo ("ajusta o secundário para sweep único").

```sh
git log --oneline --decorate
git show v0.14.0 --stat
git checkout v0.14.0 -- cad/solidcraft/PS-001.sc
```

## Licença e avisos legais

O conteúdo próprio (modelo CAD, textos, tabelas e imagens geradas pelo autor) está sob
**CC BY-NC-SA 4.0**: use, estude e compartilhe com atribuição, sem fins comerciais, e
licencie derivados sob a mesma licença.

Ficam **fora** da licença: marcas, nomes comerciais e logotipos de terceiros; fotos,
PDFs e textos de terceiros (não redistribuídos, listados em
[`docs/referencias.md`](docs/referencias.md)); e eventuais direitos de desenho
industrial ou patente sobre o produto original. O produto original não é identificado
por marca neste repositório. Detalhes, inclusive sobre fabricação e venda, em
[LEGAL.md](LEGAL.md).

## Segurança

O produto original opera em **127 V** e o secundário trabalha com corrente da ordem de
100 A. O modelo é de estudo: **não é certificado e não é instrução de fabricação**.
Construir, ligar ou modificar um equipamento assim envolve risco de choque elétrico,
incêndio e queimadura, e a responsabilidade é de quem constrói. Ver LEGAL.md, seção 7.

## Prancha 2D

A folha A2 não é desenhada à mão: as vistas vêm do modelo. O fluxo é

1. exportar as projeções com `file.export_view_dxf` (frente, lado, topo, iso) para
   `out/draw/v017/`; o detalhe do conjunto magnético é exportado à parte, com o resto dos
   corpos oculto;
2. rodar `python3 tools/draw/sheet.py`, que escala a 1:2, posiciona em 1º diedro,
   acrescenta moldura, cotas de envelope, detalhe 1:1, BOM (lida de `BOM.csv`), notas e
   carimbo;
3. abrir o DXF no OpenCADStudio e conferir com `ocs_audit` (dxf/2018) e `save_verified`;
   o plot A2 1:1 é gerado pelo mesmo app.

Resultado publicado: `out/draw/v017/PS-001-DR-001_rA_prancha-a2.dxf` (AC1032) e o PDF
A2 correspondente. As pranchas antigas em `out/draw/` e `out/vector/` estão **descartadas**.

## Próximos passos

1. Atribuir densidade/material por corpo para massa realista (hoje o CAD usa 1,29 g/cm³
   para tudo, o que não representa a peça).
2. Cotas finas de montagem (furação, folgas) na prancha — hoje ela cobre envelope e
   detalhe.
3. Publicar a revisão `B` do manual de uso quando houver massa e ciclo de trabalho
   declarados.
4. Backup remoto do TeamCraft e teste de restauração periódico.
5. Referenciar o `PL-003` no conjunto na próxima revisão do item `PS-001`.
