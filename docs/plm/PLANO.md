# Plano de ciclo de vida do produto (Brasa, PS-001)

O que este documento define: **o que é item de PLM e o que é arquivo de git**. A
fronteira é curta e vale para o produto inteiro.

## 1. A fronteira

| artefato | onde vive | como muda | como se prova |
|---|---|---|---|
| peça e conjunto: forma, material, quantidade, estrutura | **PLM** (TeamCraft) — item, revisão, ECO | revisão nova (A, B, C…), liberada por ECO | `measure`, `inspect.clearance`, sha256 do arquivo anexado |
| código: scripts, site, serviço, template | **git** | commit | build e teste no commit |
| documentação: este plano, registro, manual, guia, referências, aviso legal | **git**, dentro do repo | commit | leitura no diff; site reconstruído do commit |
| derivados: STEP, 3MF, PDF, DXF, render, pacote de build | fora do git (`dist/`, `out/`), anexados à revisão quando o PLM precisa | regerados da fonte | manifesto com sha256 |

**O PLM guarda o que se fabrica ou monta; o git guarda o que se escreve ou
programa.** Uma peça é um compromisso de forma: mudou a forma, muda a revisão e
alguém aprova. Um texto é um rascunho em revisão permanente: mudou, é commit, e o
diff mostra o que mudou.

Isso também separa as perguntas que cada um responde:

- PLM: “qual é a peça que eu compro, em que revisão, dentro de qual conjunto?”
- git: “como o produto foi pensado e como o número foi calculado, e desde quando?”

Misturar os dois faz a ECO virar burocracia sobre erro de digitação, e faz o
histórico de forma se perder no meio de commits de texto.

## 2. Identificação

Item de PLM tem número fixo; a revisão é letra:

```
PS-001        conjunto (montagem)
PS-001-LM-01  peça — sequencial de 2 dígitos
```

O TeamCraft **não renomeia item** (`PATCH /items/{n}` aceita só grupo, unidade e
classificação). Os 16 números nasceram com 2 dígitos e ficam assim: a ECR-000001
foi aceita e decidida em 16/11/2026 por manter os números históricos — a
lista de materiais que colidia (`PS-001-LM-001`, 3 dígitos) está obsoleta, e a BOM
do conjunto `PS-001` é a verdade da estrutura.

- Um item existe uma vez; revisões A, B, C… registram a forma liberada.
- Código de documento (`PS-001-US-001` etc.) **não existe mais**: documento é
  caminho de arquivo (`docs/uso/USO.md`), e o histórico é `git log`.
- O número da peça não muda quando a forma muda; muda a revisão.
- Item que sai de linha vira `obsolete`; nunca é apagado.

## 3. Estados de uma revisão

| Estado | Significado | Pode ser usado? | Como sai |
|---|---|---|---|
| `in_work` | em edição, com check-out do autor | não | vai para revisão |
| `in_review` | ECO submetida, aguardando parecer | não | aprova ou volta |
| `released` | forma liberada; o arquivo está congelado | sim | fica obsoleto |
| `obsolete` | substituída por revisão posterior | não (só histórico) | — |

A liberação é sempre por **ECO** aprovada por outra pessoa — o TeamCraft recusa a
aprovação de quem tocou nos dados da mudança. Correção de texto, de script ou de
figura **não** passa por aqui: é commit.

## 4. Mudança de forma

1. **Pedido** — ECR descreve o problema e a evidência (“o secundário colide com o
   núcleo; `inspect.clearance` aponta sobreposição”).
2. **Impacto** — `impact_summary`/`where_used`: quais conjuntos usam a peça.
3. **Execução** — alterar `cad/solidcraft/PS-001.sc`; exportar STEP/3MF da
   revisão; check-in da revisão em trabalho.
4. **Verificação** — `measure` sem erro, `inspect.clearance` sem sobreposição nos
   conjuntos críticos, arquivo com sha256. A evidência vai no comentário da ECO.
5. **Liberação** — ECO com todas as revisões afetadas; aprovação do `revisor`.
6. **Registro** — entrada no `CHANGELOG.md` (que é git) e tag do repo.

Nada de “quase igual”: ou a revisão está liberada, ou não pode ser citada como
base de decisão de forma.

## 5. Documentação e código: git

- O repo do produto é a fonte do texto e do código. O site (`site/`) e os PDFs
  (`dist/`) são **derivados**: reconstruídos do commit, nunca editados à mão.
- Histórico = `git log`. Não há tabela de revisões de documento, nem ECO, nem
  `dist/` versionado.
- Tag `vX.Y.Z` é uma **baseline do repo**: o estado exato de modelo, código e
  documentação naquele instante. A mensagem da tag lista as revisões de PLM
  liberadas junto.
- Markdown não carrega código, revisão nem estado de documento: o título é o H1 e
  a ordem do site está em `site/sidebars.js`.
- Quem precisa do texto impresso usa o pacote de `dist/v<versao>/`, gerado por
  `tools/plm/build.sh` a partir do commit e identificado pelo manifesto.

## 6. Rastreabilidade

| afirmação | onde se confere |
|---|---|
| a peça `PS-001-LM-05` é o corpo `Ponta_U` | BOM do conjunto `PS-001` no PLM (nota da linha) |
| quantidade e material de cada peça | BOM do conjunto `PS-001` no PLM |
| a forma corresponde ao texto | `measure` + `inspect.clearance` na revisão liberada |
| de onde veio a decisão | `ECR-*`/`ECO` no PLM; commit no git |
| o texto publicado corresponde ao commit | `dist/v<versao>/MANIFEST.md` (sha256 + commit) |
| direitos de terceiros | `LEGAL.md` §3–4 e `docs/referencias.md` |

A BOM do conjunto no PLM é a verdade da estrutura. `docs/construcao/BOM.csv` é a
exportação que serviu à migração inicial e continua útil para leitura rápida —
regenerar dela para o PLM é sempre conferir contra o modelo, nunca o contrário.

## 7. Papéis

Projeto de uma pessoa, papéis separados por etapa. No PLM, autor (`dionarley`) e
aprovador (`revisor`) são usuários distintos porque o TeamCraft exige isso. No
git, o próprio commit e o diff fazem a revisão; o parecer técnico (medir,
conferir BOM, conferir 127 V) continua obrigatório e vai no comentário da ECO ou
no commit.

## 8. Pendências

| # | Pendência | Impacto | Dono |
|---|---|---|---|
| 1 | Tirar as referências do conjunto aos itens de documento obsoletos | `PS-001` rev. B aponta para 6 itens em `obsolete` | autor |
| 2 | Densidade por material (massa real) | BOM e manual sem massa | autor |
| 3 | Cotas finas de montagem na prancha | a prancha cobre envelope e detalhe, não a furação | autor |
| 4 | Ensaio de isolação documentado | critério de segurança sem evidência | autor |
| 5 | Backup remoto e teste de restauração periódico | hoje o pacote fica no mesmo disco do servidor | autor |
| 6 | Preview do STEP no TeamCraft | o conversor excede 180 s / 4 GB; o 3MF cobre a visualização | autor |

## 9. Histórico

Este arquivo não tem tabela de revisões: o histórico é `git log -- docs/plm/PLANO.md`.
O modelo anterior (documento com código, revisão e ECO) está nas tags até
`v0.20.0`; a virada está registrada no `CHANGELOG.md`.
