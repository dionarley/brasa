---
title: "PS-001 — Plano de ciclo de vida do produto (PLM)"
subtitle: "Processo, estados, papéis e liberação de documentos"
docid: "PS-001-PL-001"
revision: "A"
status: "Aprovado"
date: "2026-11-14"
author: "Dionarley"
project: "PS-001 — Pistola de solda por transformador (estudo)"
---

# 1. Objetivo

Este documento define **como os documentos do PS-001 nascem, mudam, são aprovados e são
publicados**. Ele existe porque o projeto já tem mais de um artefato com o mesmo peso —
modelo 3D, desenho 2D, manual de uso, guia de construção, aviso legal — e sem uma regra
comum é impossível dizer qual versão de qual arquivo corresponde a qual estado do
produto.

O escopo é o **estudo** descrito em [LEGAL.md](../../LEGAL.md): um produto reconstruído
por observação, documentado e versionado. Não há fabricação, fornecimento, garantia nem
certificação. O PLM aqui é proporcional a isso: leve, versionado em git, sem servidor de
PDM.

Princípios:

1. **Uma fonte da verdade por artefato.** O CAD é o `cad/solidcraft/PS-001.sc`; o texto
   vive em Markdown; PDF, PNG e DXF são **derivados** e nunca editados à mão.
2. **Nada é aprovado sem verificação registrada.** Aprovar é apontar a evidência
   (medição, render, auditoria), não dar opinião.
3. **Todo documento tem código, revisão e estado.** Um PDF solto no disco não é
   documento: é sobra.
4. **O que é derivado não entra no git.** O git guarda fonte, decisão e histórico.

# 2. Estrutura de identificação

## 2.1 Código de documento

```
PS-001 - TT - NNN - rX
   |     |    |     |
   |     |    |     +-- revisão: A, B, C… (letra, não número)
   |     |    +-------- sequencial de 3 dígitos dentro do tipo
   |     +------------- tipo (2 letras)
   +------------------- produto
```

A revisão é **letra** e sobe só com mudança aprovada de conteúdo. Correção de digitação
não gera revisão: gera commit.

## 2.2 Tipos

| Tipo | Nome | O que guarda | Fonte |
|---|---|---|---|
| `PL` | Plano | processo, regras, registro mestre | `docs/plm/*.md` |
| `US` | Uso | manual de operação e segurança do produto | `docs/uso/USO.md` |
| `CO` | Construção | sequência de montagem, critérios de aceitação | `docs/construcao/*.md` |
| `LM` | Lista de materiais | BOM quantificada | `docs/construcao/BOM.csv` |
| `DR` | Desenho | prancha 2D, vistas e cotas | `out/draw/*.dxf` → PDF |
| `MD` | Modelo | CAD paramétrico e exportações | `cad/solidcraft/PS-001.sc` |
| `RG` | Registro | histórico de revisões | `CHANGELOG.md` |
| `LE` | Legal | licença, marcas, risco | `LEGAL.md`, `LICENSE` |
| `RE` | Referência | fontes de terceiros e seu uso | `docs/referencias.md` |

## 2.3 Nome de arquivo

- Markdown e CSV: `MAIUSCULAS_COM_UNDERSCORE.md` dentro da pasta do tipo
  (`docs/uso/`, `docs/construcao/`, `docs/plm/`).
- PDF publicado: `PS-001-<TIPO>-<NNN>_r<X>_<slug>.pdf`, em `dist/v<versao>/`.
- Render publicado: `PS-001_<vista>_r<X>.png`, em `dist/v<versao>/renders/`.
- Nunca renomear um arquivo publicado: a próxima revisão é outro arquivo.

# 3. Estados e ciclo de vida

```
   RASCUNHO ──► EM REVISÃO ──► APROVADO ──► PUBLICADO ──► OBSOLETO
       ▲             │             │
       └─────────────┴─────────────┘   (rejeitado / corrigido volta a rascunho)
```

| Estado | Significado | Pode ser citado? | Como termina |
|---|---|---|---|
| **Rascunho** | conteúdo em escrita, números não conferidos | não | vai para revisão |
| **Em revisão** | conteúdo completo, aguardando verificação | não | aprova ou volta |
| **Aprovado** | verificado e aceito; ainda não empacotado | sim, com ressalva | é publicado |
| **Publicado** | incluído em uma tag `vX.Y.Z` com manifesto | sim | fica obsoleto |
| **Obsoleto** | substituído por revisão posterior | não (só histórico) | permanece na tag antiga |

Regra dura: **documento em rascunho não pode ser usado como base de decisão de forma.**
Foi o que aconteceu com a primeira prancha 2D (`out/draw/`, `out/vector/`), descartada
por não corresponder ao modelo.

## 3.1 Critérios de aprovação por tipo

| Tipo | Evidência mínima para aprovar |
|---|---|
| `MD` modelo | `measure` sem erro, 0 avisos de booleano, `inspect.clearance` dos conjuntos críticos sem sobreposição, renders de conferência |
| `DR` desenho | `ocs_audit` limpo para o formato/versão alvo, `save_verified`, BOM do desenho igual à `LM` |
| `US` uso | cada número rastreável ao modelo ou a norma citada; aviso de segurança presente |
| `CO` construção | cada etapa com critério de aceitação; BOM fecha com o modelo |
| `PL`/`RG`/`LE`/`RE` | revisão de consistência com os demais documentos |

# 4. Papéis

Projeto de uma pessoa, papéis separados por **etapa**, não por pessoa. Quem escreve não
aprova no mesmo dia sem reler contra a evidência.

| Papel | Responsabilidade | Entrega |
|---|---|---|
| Autor | escreve documento, modelo ou desenho | rascunho + evidências |
| Verificador técnico | confere números contra `measure`, BOM, normas | parecer no commit |
| Verificador de segurança | confere 127 V, isolação, térmica, avisos | parecer no commit |
| Aprovador | aceita a revisão e autoriza publicação | estado `Aprovado` |

# 5. Fluxo de mudança

Toda mudança que altere forma, número ou texto aprovado segue o mesmo caminho, mesmo
sendo pequena:

1. **Pedido** — descrever o que está errado e a evidência. Ex.: "o secundário colide
   com o núcleo; `inspect.clearance` aponta sobreposição".
2. **Análise de impacto** — quais documentos e corpos mudam; qual versão sobe.
3. **Execução** — alterar a fonte (CAD ou Markdown); salvar o `.sc` a cada etapa.
4. **Verificação** — rodar as evidências do tipo (tabela 3.1). Sem isso não há aprovação.
5. **Registro** — entrada no `CHANGELOG.md` com o que mudou e por quê.
6. **Liberação** — commit + tag + manifesto (seção 6).

Mudança de forma **sempre** sobe a versão menor enquanto a série for `0.x`; correção que
não altera forma sobe a versão de patch. Texto sem efeito técnico pode ir no mesmo
commit, sem tag nova.

# 6. Liberação e baseline

## 6.1 Versionamento

[SemVer](https://semver.org/lang/pt-BR/) aplicado ao **conjunto modelo + documentos**,
não a uma API. Uma tag `vX.Y.Z` é uma **baseline**: o estado exato de tudo que estava
aprovado naquele instante.

| Tag | Conteúdo |
|---|---|
| `v0.14.0` | secundário em sweep único, pacote de licença |
| `v0.15.0` | **3D aprovado** — secundário fora do grampo, primário em carretel |
| `v0.16.0` | documentação PLM, uso e construção |
| `v0.17.0` | **prancha 2D A2 publicada** (`DR-001` rev. A) |
| `v0.17.1` | exportações STEP/3MF regeradas do modelo aprovado |

## 6.2 Pacote de liberação

Gerado por `tools/plm/build.sh` em `dist/v<versao>/` (fora do git):

```
dist/v0.17.0/
  MANIFEST.md                       versão, data, commit, sha256 de cada arquivo
  PS-001-US-001_rA_uso.pdf
  PS-001-CO-001_rB_construcao.pdf
  PS-001-PL-001_rA_plano-plm.pdf
  PS-001-PL-002_rA_registro-documentos.pdf
  PS-001-LM-001_rA_bom.csv
  PS-001-DR-001_rA_prancha-a2.pdf    prancha A2 (594 x 420 mm, 1:1)
  PS-001-DR-001_rA_prancha-a2.dxf    mesma prancha, AC1032 verificado
  renders/PS-001_iso_rA.png …
```

O `MANIFEST.md` é a prova de que o PDF corresponde ao commit: sem ele, o pacote não é
publicado.

## 6.3 Checklist de publicação

- [ ] `git status` limpo (só artefatos ignorados).
- [ ] `CHANGELOG.md` com a entrada da versão.
- [ ] `measure` do modelo sem erro e sem aviso de booleano.
- [ ] PDFs gerados sem warning de build.
- [ ] `MANIFEST.md` com sha256 de todos os arquivos.
- [ ] Tag anotada criada e enviada (quando houver remote).

# 7. Rastreabilidade

Cada afirmação de documento aponta para uma fonte verificável.

| Requisito / afirmação | Documento | Verificação |
|---|---|---|
| Núcleo EI-75, janela 12,5 × 50 | `US`, `CO` | `measure` do corpo `Nucleo`; catálogo EI |
| Secundário = 1 tira contínua, 2,5 voltas | `US`, `CO` | feature `Secundario - tira helicoidal`, `path` único |
| Sem colisão núcleo × secundário × carretel | `CO` | `inspect.clearance` — 0 sobreposições |
| 22 corpos, 448,4 cm³ | `README`, `US` | `measure` na tag `v0.15.0` |
| Massa não informada | `US`, `CO` | densidade uniforme no CAD não representa a peça |
| Isolação e 127 V | `US`, `CO` | NBR 5410, IEC 60335-2-45, NR-10 (citadas, não reproduzidas) |
| Direitos de terceiros | `LE`, `RE` | `LEGAL.md` §3–4 |

# 8. Ferramentas

| Etapa | Ferramenta | Observação |
|---|---|---|
| CAD 3D | SolidCraft (MCP) | `measure` e `inspect.clearance` são a evidência |
| Desenho 2D | OpenCADStudio (MCP) | `ocs_audit` + `save_verified` antes de entregar |
| Montagem da prancha | `tools/draw/sheet.py` | vistas exportadas do CAD; BOM lida do `LM-001` |
| Texto | Markdown | fonte única, diff legível |
| PDF | `pandoc` → `typst` | `tools/plm/build.sh` |
| Render | `screenshot` do SolidCraft | CPU, sem GPU |
| Versão | git + tags anotadas | `PS-001.sc` é zip: o par commit+tag é o histórico |

# 9. Pendências do processo

| # | Pendência | Impacto | Dono |
|---|---|---|---|
| 1 | Densidade por material (massa real) | BOM e manual sem massa | autor |
| 2 | Cotas finas de montagem na prancha | o `DR-001` cobre envelope e detalhe, não a furação | autor |
| 3 | Reexportar STEP/3MF da versão aprovada | exportações de 13/11 defasadas | autor |
| 4 | Ensaio de isolação documentado | critério de segurança sem evidência | autor |
| 5 | Template de documento versionado | hoje o layout vive no script | autor |

# 10. Histórico deste documento

| Rev. | Data | Mudança |
|---|---|---|
| A | 2026-11-14 | primeira emissão, junto com `US-001` e `CO-001` |
