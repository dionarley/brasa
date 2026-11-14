# Changelog — PS-001

Formato inspirado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/);
versionamento [SemVer](https://semver.org/lang/pt-BR/), aplicado ao **modelo e à
documentação** (não a uma API). Enquanto a série for `0.x`, mudanças de forma podem
ocorrer em versões menores. Cada tag do git corresponde a um estado do arquivo
`cad/solidcraft/PS-001.sc`.

## [0.16.0] — 2026-11-14

### Adicionado
- **PLM**: `docs/plm/PLANO.md` (`PS-001-PL-001`) define códigos de documento, estados
  (rascunho → em revisão → aprovado → publicado → obsoleto), papéis, fluxo de mudança,
  baseline por tag e critérios de aprovação por tipo de documento.
- `docs/plm/REGISTRO.md` (`PS-001-PL-002`): registro mestre com rev., estado e arquivo de
  cada documento do projeto.
- `docs/uso/USO.md` (`PS-001-US-001`): manual de uso e segurança — uso pretendido e não
  pretendido, especificações, princípio de funcionamento, ciclo de trabalho, manutenção,
  solução de problemas, descarte.
- `docs/construcao/CONSTRUCAO.md` (`PS-001-CO-001`): sequência de montagem em 5
  subconjuntos, com critério de aceitação e ponto de inspeção em cada etapa, além dos
  valores esperados de ensaio (primário ~25 Ω, secundário 0,5–1,5 mΩ, isolação ≥ 2 MΩ).
- `docs/construcao/BOM.csv` (`PS-001-LM-001`): 16 itens com quantidade, material,
  dimensões nominais, volume no modelo e observação.
- `tools/plm/build.sh` + `tools/plm/template.typ`: geram os PDFs (pandoc → typst) e o
  pacote `dist/v<versao>/` com BOM, renders, `MANIFEST.md` e `SHA256SUMS`.
- Renders de conferência `out/plot/v016/` (iso, perfil, frontal, topo, detalhe do
  transformador) gerados do modelo aprovado.

### Alterado
- `README.md`: versão 0.16.0, seção **Documentação** com a tabela de códigos e o comando
  de build, estrutura de pastas atualizada e próximos passos revisados.
- `.gitignore`: `dist/` (pacotes de liberação) fora do git.

### Corrigido
- Renders: `Nucleo` e `Cabo` estavam ocultos no documento desde a revisão anterior, o que
  fazia o modelo aparecer com o cabo solto; visibilidade restaurada antes de gerar o
  pacote.

## [0.15.0] — 2026-11-14

**Marco: modelo 3D aprovado.** A partir daqui o 3D é congelado e o trabalho passa para a
prancha 2D e para a documentação de produto.

### Alterado
- Secundário reencaminhado nos dois trechos de entrada e saída: as pontas agora correm
  por **fora** do grampo da ponteira, em X = 31,7 (face externa do grampo em 29,67,
  folga de 1 mm), em vez de atravessar o núcleo. Entrada em Y +3 / Z +16 e saída em
  Y −2 / Z −16, ambas terminando em X 54. A hélice de 2,5 voltas não foi tocada.
- Primário (`Bobina`) refeito como **carretel** de transformador real: alma
  33 × 43 × 40 mm (Z ±20) e flanges 37 × 47 × 3 mm (Z 19…22 e −22…−19), furo
  25 × 35 mm passante, filete R8 nas 12 arestas verticais e topos sem arredondamento.
  Volume 34.577 → **23.437 mm³**.

### Corrigido
- `Secundario - furo inf` deixou de emitir o aviso de booleano ("Boolean retry: tool
  displacement 8,6e-5 mm"): a face de topo do furo coincidia com a face inferior da
  tira; a altura do corte passou de 5 para **5,5 mm**.
- Colisão do secundário com o núcleo eliminada — verificado com `inspect.clearance`
  contra `Nucleo` e `Bobina`: nenhuma sobreposição.

### Verificação
- 22 corpos, 0 erros, **448,4 cm³**, envelope X −52,2…+96,1 · Y ±26,1 · Z −273,7…+39.
- Renders de conferência em `out/plot/ps001_v15_*.png` (não versionados).

### Notas
- A prancha 2D anterior (`out/draw/`, `out/vector/`) permanece descartada e não é
  referência de forma.
- Exportações STEP/3MF de 13/11 ficaram **anteriores** a este estado; reexportar a partir
  do `PS-001.sc` aprovado.

## [0.14.0] — 2026-11-14

### Adicionado
- Secundário modelado como **uma única tira** contínua (sweep de 2,5 voltas, passo
  12,8 mm, perfil 2 × 9 mm) que entra na face +Y em Z +16, desce em hélice e sai na
  face −Y em Z −16, com braços em "S" no plano e postas alongadas até X 54.
- Furos Ø6,2 do parafuso da ponteira cortados na tira e na pastilha de `Ponta_U`.
- Pacote de versionamento: `.gitignore`, `.gitattributes`, `LICENSE`
  (CC BY-NC-SA 4.0), `LEGAL.md`, `docs/referencias.md`, este changelog.

### Alterado
- Primário (`Bobina`) com quinas verticais R8 e filetes R4 nas 16 arestas de topo e
  base (volume 36.655 → 34.577 mm³).
- Parafusos e porcas das postas movidos de X 40 para **X 46**, com a pastilha de
  `Ponta_U` de 18 mm (X 34…52) e 3 mm de espessura.
- Conjunto inferior espelhado (cabeça em Y −9…−3, porca em Y 2…6).
- `README.md` reescrito: 22 corpos, EI-75, secundário helicoidal, estado real da
  prancha 2D (a refazer).

### Removido
- Corpos separados do secundário (fita, hastes e braços) — substituídos pelo sweep
  único, que também elimina as juntas que falhavam na união por faces coincidentes.

## [0.12.0] — 2026-11-13

### Alterado
- Núcleo trocado de EI-57 para **EI-75** (75 × 75 × 35 mm, janela 12,5 × 50, perna
  12,5): +14,4 % de volume no transformador (175.709 → 201.074 mm³), mantendo medidas
  de catálogo comercial.
- Chapas, cantoneiras, furos do núcleo e parafusos M5 reposicionados para o novo
  núcleo (±2,67 / ±1,5 / ±0,5 mm nas cantoneiras).
- Cabo reconstruído em **loft de 10 seções** ("cabeça de prego"), com topo largo sem
  sulco, usando topologia de superfície em vez de extrusão + filetes.
- Chave, tecla e prensa-cabo recentralizados no eixo da ponteira; fio do primário
  enterrado no cabo.

### Corrigido
- Quatro cantoneiras sem obstrução do enrolamento nem da chave.
- União entre corpos: deixou de depender de faces coincidentes.

## [0.1.0] — 2026-11-11

### Adicionado
- Primeira montagem completa em SolidCraft: núcleo EI-57, bobina, secundário em fita,
  ponta em U, cabo de madeira, chave, prensa-cabo, cabo de força e parafusos.
- Renders isométricos e ortográficos em `out/plot/`.
- Primeira tentativa de prancha 2D em DXF (descartada — ver "Notas").

### Notas
- As versões intermediárias (0.2 a 0.11) foram iterações de forma não tagueadas; o
  histórico fino está nos backups locais e nos renders arquivados em `out/plot/archive/`.
- A prancha 2D de `out/draw/` e a vetorização de `out/vector/` **não representam o
  modelo** e não devem ser usadas como referência: serão refeitas depois da aprovação
  do 3D.

[0.16.0]: #0160--2026-11-14
[0.15.0]: #0150--2026-11-14
[0.14.0]: #0140--2026-11-14
[0.12.0]: #0120--2026-11-13
[0.1.0]: #010--2026-11-11
