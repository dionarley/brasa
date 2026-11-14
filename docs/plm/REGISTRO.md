---
title: "Brasa (PS-001) — Registro mestre de documentos"
subtitle: "Índice controlado: código, revisão, estado e arquivo"
docid: "PS-001-PL-002"
revision: "C"
status: "Aprovado"
date: "2026-11-14"
author: "Dionarley"
project: "Brasa — estanhador 550 W / 127 V (PS-001, estudo)"
---

# Registro mestre

Lista de todos os documentos do projeto e do seu estado. O processo que rege esta tabela
está em [PLANO.md](PLANO.md); a instância do PDM que guarda as revisões liberadas está em
[TEAMCRAFT.md](TEAMCRAFT.md). Um documento só entra aqui quando tem código, revisão e
arquivo definido; o que é derivado aparece na coluna **Publicação**.

## 1. Documentos controlados

| Código | Título | Rev. | Estado | Arquivo |
|---|---|---|---|---|
| PS-001-PL-001 | Plano de ciclo de vida (PLM) | C | Aprovado | `docs/plm/PLANO.md` |
| PS-001-PL-002 | Registro mestre de documentos | C | Aprovado | `docs/plm/REGISTRO.md` |
| PS-001-PL-003 | TeamCraft: instalação, operação e registro | B | Aprovado | `docs/plm/TEAMCRAFT.md` |
| PS-001-US-001 | Manual de uso e segurança | B | Aprovado | `docs/uso/USO.md` |
| PS-001-CO-001 | Guia de construção (estudo) | C | Aprovado | `docs/construcao/CONSTRUCAO.md` |
| PS-001-LM-001 | Lista de materiais (BOM) | A | Aprovado | `docs/construcao/BOM.csv` |
| PS-001-MD-001 | Modelo 3D paramétrico | 0.15.0 | Publicado | `cad/solidcraft/PS-001.sc` |
| PS-001-DR-001 | Prancha 2D A2 (conjunto geral) | A | Publicado | `out/draw/v017/PS-001-DR-001_rA_prancha-a2.dxf` |
| PS-001-RG-001 | Registro de revisões | 0.19.0 | Publicado | `CHANGELOG.md` |
| PS-001-LE-001 | Aviso legal e escopo da licença | 2026-11-14 | Publicado | `LEGAL.md`, `LICENSE` |
| PS-001-RE-001 | Referências e créditos | 2026-11-14 | Publicado | `docs/referencias.md` |

O nome do PDF publicado de cada documento segue `PS-001-<TIPO>-<NNN>_r<X>_<slug>.pdf`
(PLANO §2.3) e é gerado por `tools/plm/build.sh` em `dist/v<versao>/`.

> O carimbo da prancha rev. A traz o título genérico "PS-001 PISTOLA DE SOLDA", sem
> marca de terceiro. O título com a identidade **Brasa** entra na rev. B, junto com as
> cotas de montagem (pendência registrada no `PS-001-CO-001` §8).
>
> `PS-001-DR-001` rev. A é a prancha refeita do zero a partir das projeções do modelo
> aprovado (`file.export_view_dxf` → `tools/draw/sheet.py` → OpenCADStudio). As versões
> anteriores em `out/draw/` e `out/vector/` estão **obsoletas e erradas**: não são esta
> revisão nem servem de referência de forma. O PDF e o DXF publicados ficam em
> `out/draw/v017/` (derivados, fora do git); o gerador é versionado em `tools/draw/`.

## 2. Registro no TeamCraft

O TeamCraft é o registro mestre executável: guarda a revisão liberada, os arquivos com
sha256, a BOM e o histórico de aprovação. A tabela acima continua sendo a leitura
humana; a consulta oficial é a API/MCP do PDM.

| Conceito | Valor |
|---|---|
| Servidor | `http://127.0.0.1:8080` (somente loopback) |
| Grupo de projeto | `PS-001` — **Brasa**, estanhador 550 W / 127 V |
| Itens | 1 conjunto (`PS-001`), 16 peças (`PS-001-LM-01`…`-16`), 7 documentos |
| BOM do conjunto | 16 linhas, iguais ao `LM-001` |
| Referências do conjunto | `DR-001`, `US-001`, `CO-001`, `PL-001`, `PL-002`, `LM-001` (rev. A) |
| ECO de liberação inicial | `CHG-000001` — 23 revisões A, aprovada pelo `revisor` |
| ECO da documentação | `CHG-000002` — `PL-001` B, `PL-002` B, `PL-003` A, aprovada pelo `revisor` |
| ECO da identidade | `CHG-000003` — `PS-001` B, `US-001` B, `PL-001` C, `PL-002` C, `PL-003` B, `CO-001` C |

A migração é reproduzível por `tools/plm/teamcraft_migrate.py`; a segunda liberação por
`tools/plm/teamcraft_docs_b.py`. O `PL-003` ainda não é referência do conjunto porque a
revisão A do item `PS-001` foi liberada antes da sua criação; o vínculo entra na próxima
revisão do conjunto.

## 3. Artefatos derivados

| Artefato | Gerado por | Onde | Versionado? |
|---|---|---|---|
| PDFs de documento | `tools/plm/build.sh` | `dist/v<versao>/` | não |
| Manifesto com sha256 | `tools/plm/build.sh` | `dist/v<versao>/MANIFEST.md` | não |
| Renders | `screenshot` do SolidCraft | `dist/v<versao>/renders/` | não |
| STEP / 3MF | exportação do SolidCraft | `cad/solidcraft/` | não |
| DXF da prancha | OpenCADStudio | `out/draw/` | não |
| Backup do PDM | `tools/plm/teamcraft_backup.sh` | `~/teamcraft/backups/` | não |

Regra: artefato derivado **nunca** é editado à mão. Se o PDF está errado, corrige-se o
Markdown e reconstrói; se o DXF está errado, corrige-se o desenho e reexporta.

## 4. Correspondência versão × documentos

| Versão | Data | Marco | Documentos afetados |
|---|---|---|---|
| 0.14.0 | 2026-11-14 | secundário em sweep único; pacote de licença | MD, LE, RE, RG |
| 0.15.0 | 2026-11-14 | **3D aprovado** | MD (congelado) |
| 0.16.0 | 2026-11-14 | documentação de produto | PL, US, CO, LM, RG |
| 0.17.0 | 2026-11-14 | **prancha 2D A2 publicada** | DR, CO (rev. B), RG |
| 0.17.1 | 2026-11-14 | exportações STEP/3MF regeradas do modelo aprovado | MD (derivados), RG |
| 0.18.0 | 2026-11-14 | **PDM TeamCraft e documentação do fluxo** | PL-001 (B), PL-002 (B), PL-003 (A), RG |
| 0.19.0 | 2026-11-14 | **identidade própria Brasa** | MD (nome), US (B), PL-001 (C), PL-002 (C), PL-003 (B), CO (C), LE, RE, RG |

## 5. Revisões substituídas

| Documento | Revisão antiga | Revisão vigente | Quando | Onde a antiga continua válida |
|---|---|---|---|---|
| `PS-001-CO-001` | A | B | 0.17.0 | tag `v0.16.0` |
| `PS-001-CO-001` | B | C | 0.19.0 | tag `v0.18.0` |
| `PS-001-PL-001` | A | B | 0.18.0 | tag `v0.17.1` |
| `PS-001-PL-001` | B | C | 0.19.0 | tag `v0.18.0` |
| `PS-001-PL-002` | A | B | 0.18.0 | tag `v0.17.1` |
| `PS-001-PL-002` | B | C | 0.19.0 | tag `v0.18.0` |
| `PS-001-PL-003` | A | B | 0.19.0 | tag `v0.18.0` |
| `PS-001-US-001` | A | B | 0.19.0 | tag `v0.18.0` |

Documento obsoleto não fica listado como vigente; o histórico fica na tag correspondente
e nas revisões `obsolete` do TeamCraft.
