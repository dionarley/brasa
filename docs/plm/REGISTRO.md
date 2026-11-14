---
title: "PS-001 — Registro mestre de documentos"
subtitle: "Índice controlado: código, revisão, estado e arquivo"
docid: "PS-001-PL-002"
revision: "A"
status: "Aprovado"
date: "2026-11-14"
author: "Dionarley"
project: "PS-001 — Pistola de solda por transformador (estudo)"
---

# Registro mestre

Lista de todos os documentos do projeto e do seu estado. O processo que rege esta tabela
está em [PLANO.md](PLANO.md). Um documento só entra aqui quando tem código, revisão e
arquivo definido; o que é derivado aparece na coluna **Publicação**.

## 1. Documentos controlados

| Código | Título | Rev. | Estado | Arquivo |
|---|---|---|---|---|
| PS-001-PL-001 | Plano de ciclo de vida (PLM) | A | Aprovado | `docs/plm/PLANO.md` |
| PS-001-PL-002 | Registro mestre de documentos | A | Aprovado | `docs/plm/REGISTRO.md` |
| PS-001-US-001 | Manual de uso e segurança | A | Aprovado | `docs/uso/USO.md` |
| PS-001-CO-001 | Guia de construção (estudo) | A | Aprovado | `docs/construcao/CONSTRUCAO.md` |
| PS-001-LM-001 | Lista de materiais (BOM) | A | Aprovado | `docs/construcao/BOM.csv` |
| PS-001-MD-001 | Modelo 3D paramétrico | 0.15.0 | Publicado | `cad/solidcraft/PS-001.sc` |
| PS-001-DR-001 | Prancheta 2D A2 | — | **Rascunho** | `out/draw/` |
| PS-001-RG-001 | Registro de revisões | 0.16.0 | Publicado | `CHANGELOG.md` |
| PS-001-LE-001 | Aviso legal e escopo da licença | 2026-11-14 | Publicado | `LEGAL.md`, `LICENSE` |
| PS-001-RE-001 | Referências e créditos | 2026-11-14 | Publicado | `docs/referencias.md` |

O nome do PDF publicado de cada documento segue `PS-001-<TIPO>-<NNN>_r<X>_<slug>.pdf`
(PLANO §2.3) e é gerado por `tools/plm/build.sh` em `dist/v<versao>/`.

> `PS-001-DR-001` é o único documento em rascunho: a prancha 2D está sendo refeita do
> zero em OpenCADStudio. As versões antigas em `out/draw/` e `out/vector/` estão
> **obsoletas e erradas** — não são esta revisão nem servem de referência.

## 2. Artefatos derivados

| Artefato | Gerado por | Onde | Versionado? |
|---|---|---|---|
| PDFs de documento | `tools/plm/build.sh` | `dist/v<versao>/` | não |
| Manifesto com sha256 | `tools/plm/build.sh` | `dist/v<versao>/MANIFEST.md` | não |
| Renders | `screenshot` do SolidCraft | `dist/v<versao>/renders/` | não |
| STEP / 3MF | exportação do SolidCraft | `cad/solidcraft/` | não |
| DXF da prancha | OpenCADStudio | `out/draw/` | não |

Regra: artefato derivado **nunca** é editado à mão. Se o PDF está errado, corrige-se o
Markdown e reconstrói; se o DXF está errado, corrige-se o desenho e reexporta.

## 3. Correspondência versão × documentos

| Versão | Data | Marco | Documentos afetados |
|---|---|---|---|
| 0.14.0 | 2026-11-14 | secundário em sweep único; pacote de licença | MD, LE, RE, RG |
| 0.15.0 | 2026-11-14 | **3D aprovado** | MD (congelado) |
| 0.16.0 | 2026-11-14 | documentação de produto | PL, US, CO, LM, RG |

## 4. Revisões substituídas

Nenhuma até 0.16.0. Quando houver, a linha antiga sai desta tabela e passa para o
histórico da tag correspondente — documento obsoleto não fica listado como vigente.
