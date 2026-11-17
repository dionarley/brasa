# Registro do PLM (Brasa, PS-001)

O que existe hoje no TeamCraft: o conjunto, as peças e o que ainda sobra do modelo
anterior. O processo está em [PLANO.md](PLANO.md); a operação da instância, em
[TEAMCRAFT.md](TEAMCRAFT.md). Documentação não aparece como item — está no git,
listada no §4.

## 1. Conjunto

| Item | Nome | Rev. | Estado | Arquivos no vault |
|---|---|---|---|---|
| `PS-001` | Brasa — estanhador 550 W / 127 V | C | `released` | `cad/PS-001.sc` (montagem nativa), `cad/PS-001.step`, `cad/PS-001.3mf`, 5 renders |

BOM: 16 linhas, uma por peça do §2 — as 14 com geometria passam a apontar para a
revisão **B** das peças. Massa do conjunto: **1,72098 kg** (soma das peças), gravada
na revisão C. Custo ainda não preenchido (pendência 4 do plano).

A rev. C entrou junto com as peças na ECO **CHG-000010** ("modelo nativo: 14 peças
+ montagem"), submetida e aprovada pelo usuário `revisor`. O release de um produto
é atômico: peça e montagem foram liberadas no mesmo movimento.

## 2. Peças

Todas em revisão **B**, `released`, com `mass_kg` e material na revisão. Cada peça é
um arquivo nativo em `cad/solidcraft/parts/`; `PS-001.sc` é a montagem — 14 links,
22 posições — e a coluna **arquivo** é o que liga o item à geometria. Cada revisão
guarda o `.sc` e o STEP derivado (`cad/<item>.sc` e `cad/<item>.step` no vault).

| Item | Nome | Qtd. | Arquivo nativo | Massa unit. (g) |
|---|---|---:|---|---:|
| `PS-001-LM-01` | Núcleo EI-75 (pacote de chapas) | 1 | `parts/PS-001-LM-01.sc` | 1.139,08 |
| `PS-001-LM-02` | Carretel do primário | 1 | `parts/PS-001-LM-02.sc` | 32,81 |
| `PS-001-LM-03` | Fio de cobre esmaltado AWG 28 | 1 | `parts/PS-001-LM-03.sc` | 5,90 |
| `PS-001-LM-04` | Fita de cobre do secundário | 1 | `parts/PS-001-LM-04.sc` | 91,93 |
| `PS-001-LM-05` | Ponta em U | 1 | `parts/PS-001-LM-05.sc` | 21,43 |
| `PS-001-LM-06` | Cantoneira do transformador | 4 | `parts/PS-001-LM-06.sc` | 43,62 |
| `PS-001-LM-07` | Parafuso M5 das cantoneiras | 4 | `parts/PS-001-LM-07.sc` | 14,51 |
| `PS-001-LM-08` | Parafuso M5 da ponteira | 2 | `parts/PS-001-LM-08.sc` | 6,49 |
| `PS-001-LM-09` | Porca M5 da ponteira | 2 | `parts/PS-001-LM-09.sc` | 2,47 |
| `PS-001-LM-10` | Cabo / empunhadura | 1 | `parts/PS-001-LM-10.sc` | 161,25 |
| `PS-001-LM-11` | Chave | 1 | `parts/PS-001-LM-11.sc` | 7,29 |
| `PS-001-LM-12` | Tecla | 1 | `parts/PS-001-LM-12.sc` | 2,61 |
| `PS-001-LM-13` | Prensa-cabo | 1 | `parts/PS-001-LM-13.sc` | 1,63 |
| `PS-001-LM-14` | Cabo de força | 1 | `parts/PS-001-LM-14.sc` | 6,62 |
| `PS-001-LM-15` | Isolante entre primário e secundário | 1 | — (não modelado) | — |
| `PS-001-LM-16` | Estanho e fluxo | 1 | — (consumível) | — |

Cada peça tem material atribuído (densidade em `g/cm³`): silício 7,65; aço 7,85;
aço zincado 7,87; baquelite 1,40; cobre esmaltado 8,94; cobre 8,96; madeira 0,75;
ABS 1,04; borracha 1,10; PVC 1,35. Detalhe de dimensão e volume está na descrição
do item e na nota da linha da BOM; `docs/construcao/BOM.csv` é a exportação dessa
estrutura.

Os números de 2 dígitos são históricos e **ficam**: o TeamCraft não renomeia item e
a ECR-000001 foi decidida em 16/11/2026 por manter a numeração (a lista de
materiais em 3 dígitos, `PS-001-LM-001`, está obsoleta e não colide mais).

## 3. Sobra do modelo anterior

Sete itens de **documento** foram criados quando a documentação era controlada
por revisão e ECO. Eles não têm mais papel: o texto está no git e o PDF é derivado.
Foram **obsoletados em 16/11/2026** — a política do grupo `PS-001` não exige ECO
para obsolescência, então a mudança foi direta e está no `item_history`.

| Item | Nome | Rev. | Estado |
|---|---|---|---|
| `PS-001-CO-001` | Guia de construção (estudo) | C | `obsolete` |
| `PS-001-US-001` | Manual de uso e segurança | B | `obsolete` |
| `PS-001-DR-001` | Prancha 2D A2 — conjunto geral | A | `obsolete` |
| `PS-001-LM-001` | Lista de materiais (BOM) | A | `obsolete` |
| `PS-001-PL-001` | Plano de ciclo de vida (PLM) | D | `obsolete` |
| `PS-001-PL-002` | Registro mestre de documentos | D | `obsolete` |
| `PS-001-PL-003` | TeamCraft: instalação, operação e registro | C | `obsolete` |

O conjunto `PS-001` rev. B ainda os referencia como *documento controlado* — são
referências a itens obsoletos. A próxima revisão do conjunto as tira; até lá, a
leitura que vale é a deste registro.

## 4. Documentação (git)

| Arquivo | O que é |
|---|---|
| `README.md` | apresentação, estado e o que está pronto |
| `docs/uso/USO.md` | manual de uso e segurança |
| `docs/construcao/CONSTRUCAO.md` | sequência de montagem e critérios de aceitação |
| `docs/construcao/BOM.csv` | exportação da BOM do conjunto |
| `docs/plm/PLANO.md` | este modelo: PLM × git |
| `docs/plm/REGISTRO.md` | este arquivo |
| `docs/plm/TEAMCRAFT.md` | instalação e operação do PDM |
| `docs/referencias.md` | fontes de terceiros e o que cada uma contribuiu |
| `LEGAL.md`, `LICENSE` | escopo do estudo, direitos e licença |
| `CHANGELOG.md` | o que mudou e por quê, por versão |

O histórico de qualquer um é `git log -- <arquivo>`; a tag `vX.Y.Z` congela o
conjunto. Nenhum deles tem revisão de letra.

## 5. Derivados (fora do git)

| Artefato | Gerado por | Onde |
|---|---|---|
| PDFs e manifesto | `tools/plm/build.sh` | `dist/v<versao>/` |
| Site | `site/docs.sh build` | `site/build/` |
| Renders | `screenshot` do SolidCraft | `dist/v<versao>/renders/` |
| STEP do conjunto e das peças | exportação do SolidCraft | `cad/solidcraft/PS-001.step` e `cad/solidcraft/parts/*.step` |
| 3MF e renders | exportação do SolidCraft | `cad/solidcraft/` e `dist/v<versao>/renders/` |
| DXF da prancha | OpenCADStudio | `out/draw/` |
| Backup do PDM | `tools/plm/teamcraft_backup.sh` | `~/teamcraft/backups/` |

Derivado nunca é editado à mão: corrige-se a fonte (`.sc`, Markdown, desenho) e
regera.

## 6. Onde conferir

Pelo MCP do TeamCraft, no OpenCode:

```text
get_bom({ item: "PS-001", revision: "B" })
get_revision({ item: "PS-001-LM-05", revision: "A" })
item_history({ item: "PS-001" })
```

Interface: <http://localhost:8080> — grupo `PS-001`. A API é `http://127.0.0.1:8080/api/v1`
(token em `~/teamcraft/.admin_token`); as rotas usadas estão em
[TEAMCRAFT.md](TEAMCRAFT.md) §5.
