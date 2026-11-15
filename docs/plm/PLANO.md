---
title: "Brasa (PS-001) — Plano de ciclo de vida do produto (PLM)"
subtitle: "Processo, estados, papéis e liberação de documentos"
docid: "PS-001-PL-001"
revision: "D"
status: "Aprovado"
date: "2026-11-15"
author: "Dionarley"
project: "Brasa — estanhador 550 W / 127 V (PS-001, estudo)"
---

# 1. Objetivo

Este documento define **como os documentos do PS-001 nascem, mudam, são aprovados e são
publicados**. Ele existe porque o projeto já tem mais de um artefato com o mesmo peso —
modelo 3D, desenho 2D, manual de uso, guia de construção, aviso legal — e sem uma regra
comum é impossível dizer qual versão de qual arquivo corresponde a qual estado do
produto.

O escopo é o **estudo** descrito em [LEGAL.md](../../LEGAL.md): um produto reconstruído
por observação, documentado e versionado. Não há fabricação, fornecimento, garantia nem
certificação. O PLM aqui é proporcional a isso: leve, com a fonte em git e o registro
liberado em uma instância local do **TeamCraft** — o manual da ferramenta está em
[TEAMCRAFT.md](TEAMCRAFT.md).

Princípios:

1. **Uma fonte da verdade por artefato.** O CAD é o `cad/solidcraft/PS-001.sc`; o texto
   vive em Markdown; PDF, PNG e DXF são **derivados** e nunca editados à mão. O git
   guarda a fonte; o TeamCraft guarda a revisão liberada e seus arquivos.
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
não gera revisão: gera commit. No TeamCraft o código do documento é o **número do item** e
a revisão é o código da revisão (`A`, `B`, …), com o mesmo significado desta seção.

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

No TeamCraft os estados são `in_work`, `in_review`, `released` e `obsolete`, e a
correspondência é: rascunho → `in_work`; em revisão → `in_review`; aprovado e
publicado → `released` (a publicação acrescenta a tag git e o pacote); obsoleto →
`obsolete`. A liberação é sempre feita por uma **ECO** aprovada por outra pessoa.

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

A evidência de cada tipo é anexada à revisão no TeamCraft (arquivo, render, PDF com o
resultado da auditoria) e citada no comentário da ECO. Aprovar sem essa evidência é
erro de processo, não opinião.

# 4. Papéis

Projeto de uma pessoa, papéis separados por **etapa**, não por pessoa. Quem escreve não
aprova no mesmo dia sem reler contra a evidência. No TeamCraft isso é imposto por dois
usuários: o autor (`dionarley`, admin) e o aprovador (`revisor`, editor do grupo).

| Papel | Responsabilidade | Entrega | Usuário |
|---|---|---|---|
| Autor | escreve documento, modelo ou desenho | rascunho + evidências | `dionarley` |
| Verificador técnico | confere números contra `measure`, BOM, normas | parecer no commit | `dionarley` |
| Verificador de segurança | confere 127 V, isolação, térmica, avisos | parecer no commit | `dionarley` |
| Aprovador | aceita a revisão e autoriza publicação | ECO aprovada | `revisor` |

O TeamCraft recusa a aprovação de quem tocou nos dados da mudança; por isso o aprovador
é um usuário separado, mesmo sendo a mesma pessoa física no laboratório.

# 5. Fluxo de mudança

Toda mudança que altere forma, número ou texto aprovado segue o mesmo caminho, mesmo
sendo pequena:

1. **Pedido** — descrever o que está errado e a evidência. Ex.: "o secundário colide
   com o núcleo; `inspect.clearance` aponta sobreposição". Se ainda não houver análise,
   o pedido é uma ECR; se a correção já está definida, vai direto para a ECO.
2. **Análise de impacto** — quais documentos e corpos mudam; qual versão sobe. No
   TeamCraft, `impact_summary`/`where_used` mostram o que a mudança alcança.
3. **Execução** — alterar a fonte (CAD ou Markdown); salvar o `.sc` a cada etapa. No
   TeamCraft, a revisão em trabalho fica sob check-out do autor.
4. **Verificação** — rodar as evidências do tipo (tabela 3.1) e anexá-las à revisão.
   Sem isso não há aprovação.
5. **Registro** — entrada no `CHANGELOG.md` com o que mudou e por quê.
6. **Liberação** — ECO no TeamCraft com todas as revisões afetadas, aprovação do
   `revisor`, commit + tag + manifesto (seção 6).

Mudança de forma **sempre** sobe a versão menor enquanto a série for `0.x`; correção que
não altera forma sobe a versão de patch. Texto sem efeito técnico pode ir no mesmo
commit, sem tag nova; no TeamCraft ainda assim exige revisão e ECO, porque o arquivo
liberado muda.

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
| `v0.18.0` | **PDM TeamCraft** — migração do PS-001, `PL-001`/`PL-002` rev. B e `PL-003` rev. A |
| `v0.19.0` | **identidade própria** — o projeto passa a se chamar **Brasa**, sem marca de terceiro |
| `v0.20.0` | **ferramentas de apoio** — documentação publicada como site, GridCraft, visualizador DXF e scripts de administração do PDM |

## 6.2 Pacote de liberação

Gerado por `tools/plm/build.sh` em `dist/v<versao>/` (fora do git):

```
dist/v0.20.0/
  MANIFEST.md                       versão, data, commit, sha256 de cada arquivo
  PS-001-US-001_rB_uso.pdf
  PS-001-CO-001_rC_construcao.pdf
  PS-001-PL-001_rD_plano-plm.pdf
  PS-001-PL-002_rD_registro-documentos.pdf
  PS-001-PL-003_rC_teamcraft.pdf
  PS-001-LM-001_rA_bom.csv
  PS-001-DR-001_rA_prancha-a2.pdf    prancha A2 (594 x 420 mm, 1:1)
  PS-001-DR-001_rA_prancha-a2.dxf    mesma prancha, AC1032 verificado
  renders/PS-001_iso_rA.png …
```

O mesmo pacote é anexado às revisões no TeamCraft antes da ECO de liberação. O
`MANIFEST.md` é a prova de que o PDF corresponde ao commit: sem ele, o pacote não é
publicado.

O **site** é uma publicação derivada desta mesma fonte, não um segundo documento:
`site/docs.sh build` lê `docs/**/*.md` e `LEGAL.md` e gera o HTML em `site/build/`
(fora do git). Nada é escrito em `docs/` a partir do site; o banner de revisão que
aparece na página vem do front matter do Markdown.

## 6.3 Checklist de publicação

- [ ] `git status` limpo (só artefatos ignorados).
- [ ] `CHANGELOG.md` com a entrada da versão.
- [ ] `measure` do modelo sem erro e sem aviso de booleano.
- [ ] PDFs gerados sem warning de build.
- [ ] `MANIFEST.md` com sha256 de todos os arquivos.
- [ ] Site reconstruído (`site/docs.sh build`) com as revisões vigentes.
- [ ] Revisões e arquivos anexados no TeamCraft, com `readiness` sem bloqueios.
- [ ] ECO aprovada pelo `revisor` (usuário diferente do autor).
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
| Revisão liberada e responsável pela aprovação | `PL-002`, ECO | TeamCraft: `get_change`, `item_history` |

# 8. Ferramentas

| Etapa | Ferramenta | Observação |
|---|---|---|
| CAD 3D | SolidCraft (MCP) | `measure` e `inspect.clearance` são a evidência |
| Desenho 2D | OpenCADStudio (MCP) | `ocs_audit` + `save_verified` antes de entregar |
| Montagem da prancha | `tools/draw/sheet.py` | vistas exportadas do CAD; BOM lida do `LM-001` |
| Texto | Markdown | fonte única, diff legível |
| PDF | `pandoc` → `typst` | `tools/plm/build.sh` |
| Site | Docusaurus (`site/`) | publica `docs/` e `LEGAL.md`; derivado, sem conteúdo próprio |
| Planilhas | GridCraft (web + CLI) | rascunhos em `workbooks/`; o arquivo controlado vai ao PDM |
| Visualizador DXF | MLightCAD (`tools/cad-viewer/`) | só leitura, no navegador; DWG (GPL) fica fora |
| Render | `screenshot` do SolidCraft | CPU, sem GPU |
| PDM | TeamCraft 0.2.7 (local) | revisões, ECO, arquivos e BOM liberados |
| Administração do PDM | `tools/plm/admin/*.sh` | serviço, branding e tokens; não derruba a ponte MCP |
| Consulta | MCP do TeamCraft no OpenCode | somente leitura/ECR; não libera |
| Backup | `tools/plm/teamcraft_backup.sh` | `pg_dump` no contêiner + vault |
| Versão | git + tags anotadas | `PS-001.sc` é zip: o par commit+tag é o histórico |

# 9. Pendências do processo

| # | Pendência | Impacto | Dono |
|---|---|---|---|
| 1 | Densidade por material (massa real) | BOM e manual sem massa | autor |
| 2 | Cotas finas de montagem na prancha | o `DR-001` cobre envelope e detalhe, não a furação | autor |
| 3 | Ensaio de isolação documentado | critério de segurança sem evidência | autor |
| 4 | Backup remoto e teste de restauração periódico | hoje o pacote fica no mesmo disco do servidor | autor |
| 5 | Preview do STEP no TeamCraft | o conversor excede 180 s / 4 GB; o 3MF cobre a visualização | autor |
| 6 | Referência do `PL-003` no conjunto | entra na próxima revisão do item `PS-001` | autor |
| 7 | Carimbo da prancha com a identidade Brasa | o `DR-001` rev. A ainda traz o título genérico; entra na rev. B, com as cotas | autor |

As pendências 3 e 5 da revisão A (reexportar STEP/3MF e versionar o template) foram
resolvidas em `v0.17.1` e `v0.16.0`, respectivamente.

# 10. Histórico deste documento

| Rev. | Data | Mudança |
|---|---|---|
| A | 2026-11-14 | primeira emissão, junto com `US-001` e `CO-001` |
| B | 2026-11-14 | adota o TeamCraft como PDM: estados, papéis, ECO e checklist; cita o `PL-003` |
| C | 2026-11-14 | adota o nome próprio **Brasa**; produto deixa de ser identificado por marca de terceiro |
| D | 2026-11-15 | registra as ferramentas de apoio (site, GridCraft, visualizador DXF, scripts de administração) e a publicação derivada; pendência da prancha rev. B |
