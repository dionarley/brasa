# Registro do PLM (Brasa, PS-001)

O que existe hoje no TeamCraft: o conjunto, as peças e o que ainda sobra do modelo
anterior. O processo está em [PLANO.md](PLANO.md); a operação da instância, em
[TEAMCRAFT.md](TEAMCRAFT.md). Documentação não aparece como item — está no git,
listada no §4.

## 1. Conjunto

| Item | Nome | Rev. | Estado | Arquivos no vault |
|---|---|---|---|---|
| `PS-001` | Brasa — estanhador 550 W / 127 V | B | `released` | `PS-001.sc`, `PS-001.step` (AP242), `PS-001.3mf`, 5 renders |

BOM: 16 linhas, uma por peça do §2. Massa e custo ainda não preenchidos (pendência
3 e 4 do plano).

## 2. Peças

Todas em revisão **A**, `released`. A coluna **corpo** é o nome no
`cad/solidcraft/PS-001.sc` — é o que liga o item à geometria.

| Item | Nome | Qtd. | Corpo no modelo |
|---|---|---:|---|
| `PS-001-LM-01` | Núcleo EI-75 (pacote de chapas) | 1 | `Nucleo` |
| `PS-001-LM-02` | Carretel do primário | 1 | `Bobina` |
| `PS-001-LM-03` | Fio de cobre esmaltado AWG 28 | 1 | `Fio_primario` |
| `PS-001-LM-04` | Fita de cobre do secundário | 1 | `Secundario` |
| `PS-001-LM-05` | Ponta em U | 1 | `Ponta_U` |
| `PS-001-LM-06` | Cantoneira do transformador | 4 | `Canto_dir_sup`, `Canto_dir_inf`, `Canto_esq_sup`, `Canto_esq_inf` |
| `PS-001-LM-07` | Parafuso M5 das cantoneiras | 4 | `Parafuso_canto_*` |
| `PS-001-LM-08` | Parafuso M5 da ponteira | 2 | `Parafuso_ponta_sup`, `Parafuso_ponta_inf` |
| `PS-001-LM-09` | Porca M5 da ponteira | 2 | `Porca_ponta_sup`, `Porca_ponta_inf` |
| `PS-001-LM-10` | Cabo / empunhadura | 1 | `Cabo` |
| `PS-001-LM-11` | Chave | 1 | `Chave` |
| `PS-001-LM-12` | Tecla | 1 | `Tecla` |
| `PS-001-LM-13` | Prensa-cabo | 1 | `Prensa_cabo` |
| `PS-001-LM-14` | Cabo de força | 1 | `Cabo_forca` |
| `PS-001-LM-15` | Isolante entre primário e secundário | 1 | — (não modelado) |
| `PS-001-LM-16` | Estanho e fluxo | 1 | — (consumível) |

Detalhe de material, dimensão e volume de cada uma está na descrição do item e na
nota da linha da BOM. `docs/construcao/BOM.csv` é a exportação dessa estrutura.

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
| STEP / 3MF | exportação do SolidCraft | `cad/solidcraft/` e vault do conjunto |
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
