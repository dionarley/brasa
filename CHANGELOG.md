# Changelog — PS-001

Formato inspirado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/);
versionamento [SemVer](https://semver.org/lang/pt-BR/), aplicado ao **modelo e à
documentação** (não a uma API). Enquanto a série for `0.x`, mudanças de forma podem
ocorrer em versões menores. Cada tag do git corresponde a um estado do arquivo
`cad/solidcraft/PS-001.sc`.

## [0.21.0] — 2026-11-16

**Marco: a fronteira do PLM.** O PLM passa a guardar **peça e montagem**; código e
documentação ficam no git, versionados por commit. Documento deixa de ser item do
TeamCraft: sem código de documento, sem revisão de letra, sem ECO para texto. Um
documento não tem “revisão aprovada” — tem diff.

### Alterado
- `docs/plm/PLANO.md`: reescrito em torno da fronteira (PLM × git). Estados e ECO
  valem para item de peça/conjunto; documentação muda por commit e tag `vX.Y.Z` do
  repo. O histórico do documento passa a ser `git log`.
- `docs/plm/REGISTRO.md`: agora é o índice do PLM — conjunto, 16 peças, corpo do
  modelo de cada uma e o que sobrou do modelo antigo.
- `docs/plm/TEAMCRAFT.md`: item = peça ou conjunto; o exemplo de check-in usa uma
  peça; as referências do conjunto aos documentos ficam marcadas como legado.
- `docs/uso/USO.md`, `docs/construcao/CONSTRUCAO.md`: sem front matter e sem tabela
  de revisões; os documentos passam a se citar por caminho, não por código.
- `site/`: removida a faixa de documento controlado; o site publica o texto do
  commit, sem código/revisão/estado.
- `tools/plm/build.sh`: PDFs nomeados pelo slug (`uso.pdf`, `plano-plm.pdf`), sem
  código de documento nem revisão; `BOM.csv` sai com o nome do arquivo-fonte.

### Pendente no TeamCraft
- Sete itens de documento (`PS-001-PL-00x`, `-US-001`, `-CO-001`, `-DR-001`,
  `-LM-001`) continuam `released`; sair de linha exige ECO.
- ECR-000001 (peças em três dígitos) aceita, execução pendente.

## [0.20.0] — 2026-11-15

**Marco: ferramentas de apoio.** A documentação ganha uma publicação derivada (site),
as planilhas entram pelo GridCraft, o desenho passa a ser conferido num visualizador DXF
no navegador e o TeamCraft ganha scripts de administração. Nenhum documento controlado
muda de conteúdo de produto — muda o processo em volta dele.

### Adicionado
- `site/`: Docusaurus 3.10 publicando `docs/**/*.md` e `LEGAL.md` como site estático
  (podman, `127.0.0.1:8081`), com banner de documento controlado lido do front matter e
  plugin remark para as figuras do pandoc (`{width=NN%}` e `renders/`).
- `tools/gridcraft/`: GridCraft instalado e verificado (serviço web em `127.0.0.1:8088`,
  CLI headless e servidor MCP stdio), com `workbooks/` para as planilhas de trabalho.
- `tools/cad-viewer/`: visualizador DXF com `@mlightcad/cad-simple-viewer` 1.7.8 no
  navegador (`127.0.0.1:8089`), aberto por arrastar, botão, `?file=` ou lista de
  desenhos publicados. Só DXF: DWG (LibreDWG, GPL) fica fora.
- `tools/plm/admin/`: `teamcraft_service.sh` (subir, parar, reiniciar, status, logs),
  `teamcraft_branding.sh` (logos e nome do cabeçalho) e `teamcraft_tokens.sh` (tokens).
- `dist/v0.20.0/`: pacote com as revisões desta liberação e manifesto `sha256`.

### Alterado
- `PS-001-PL-001` sobe para **rev. D**: §8 registra site, GridCraft, visualizador e
  scripts de administração; §6.2 trata o site como publicação derivada da mesma fonte;
  §9 ganha a pendência do carimbo da prancha rev. B.
- `PS-001-PL-002` sobe para **rev. D**: tabela com as revisões D/D/C, ECO 5, derivados
  (site, planilhas, `drawings/`), versão 0.20.0 e revisões substituídas.
- `PS-001-PL-003` sobe para **rev. C**: §3.5 e §8.2 passam a usar
  `tools/plm/admin/teamcraft_service.sh`; nova §3.6 descreve os scripts.
- `README.md`: versão 0.20.0, seção de documentação publicada e de desenhos, árvore de
  `site/`, `tools/gridcraft/`, `tools/cad-viewer/` e `workbooks/`.
- `.gitignore`: `site/{node_modules,build,.docusaurus,.npm,static/renders,static/LICENSE}`
  e o build do visualizador.

### Corrigido
- O manual do PDM ensinava `pkill -x teamcraft` para parar o servidor: o sinal derrubava
  também a ponte MCP do OpenCode e as tools `teamcraft_*` sumiam até reconectar. Agora o
  `down` do script encerra só o `teamcraft serve` e confere o `readyz`.

### Verificação
- ECO `CHG-000005` aprovada pelo `revisor`; `PL-001` D, `PL-002` D e `PL-003` C em
  `released`.
- `dist/v0.20.0/` com `MANIFEST.md` e sha256 conferidos.
- Site reconstruído (`site/docs.sh build`) com os banners das revisões D e C; visualizador
  abrindo o DXF da prancha A2 com textos, cotas e carimbo.

## [0.19.0] — 2026-11-14

**Marco: identidade própria.** O projeto e o produto passam a se chamar **Brasa**;
`PS-001` continua como código interno. Nenhuma marca de terceiro é usada como nome,
identidade ou referência de origem.

### Adicionado
- `tools/plm/teamcraft_identity.py`: libera a identidade no TeamCraft — conjunto rev. B,
  `US-001` rev. B, `PL-001`/`PL-002` rev. C, `PL-003` rev. B, `CO-001` rev. C e as ECOs
  `CHG-000003`/`CHG-000004`.
- `dist/v0.19.0/`: pacote com os PDFs das novas revisões e manifesto.

### Alterado
- `README.md` e `LICENSE`: título **Brasa — estanhador 550 W / 127 V (PS-001)**; a
  licença deixa de citar marca de terceiro.
- `LEGAL.md`: seção 3 passa a tratar de **nome próprio e marcas de terceiros**, sem
  nomear a marca do produto original; o Brasa é apresentado como nome do estudo.
- `PS-001-US-001` sobe para **rev. B**: identificação pelo nome Brasa, sem marca.
- `PS-001-PL-001` sobe para **rev. C** e `PS-001-PL-002` para **rev. C**: título,
  identidade e tabela de versões/revisões.
- `PS-001-PL-003` sobe para **rev. B**: instância `Brasa PLM`, grupo e ECO 3.
- `PS-001-CO-001` sobe para **rev. C**: guia de construção com a identificação Brasa.
- `docs/referencias.md`: o anúncio é citado pelo produto e pelos IDs, sem a marca.
- TeamCraft: instância renomeada para `Brasa PLM`; grupo `PS-001` com nome/descrição
  Brasa (o 0.2.7 não expõe renomear grupo pela API, então o rótulo foi corrigido como
  metadado no banco); conjunto `PS-001` rev. B com o novo nome.

### Verificação
- `CHG-000003` (5 revisões + `CO-001` B) e `CHG-000004` (`CO-001` C) aprovadas pelo
  `revisor`; 7 revisões em `released`.
- `search_items` mostra o conjunto como "Brasa — estanhador 550 W / 127 V".
- `dist/v0.19.0/` com `SHA256SUMS` verificado; PDFs `US-001` B, `PL-001` C,
  `PL-002` C e `PL-003` B gerados sem aviso.
- Backup do TeamCraft gerado e restauração de teste conferida.

## [0.18.0] — 2026-11-14

**Marco: PDM em uso.** O PS-001 passa a ter as revisões liberadas em uma instância
local do [TeamCraft](https://github.com/rudalabs/TeamCraft) 0.2.7, com PostgreSQL 16
em podman, liberação por ECO e aprovação por um segundo usuário.

### Adicionado
- `docs/plm/TEAMCRAFT.md` (`PS-001-PL-003` rev. A): instalação, configuração,
  usuários e tokens, operação de check-out/ECO, MCP do OpenCode, mapeamento do
  PS-001, backup/restauração e limites de segurança.
- `tools/plm/teamcraft_migrate.py`: migração idempotente do PS-001 (grupo, 23 itens,
  arquivos, BOM de 16 linhas, 6 referências e ECO `CHG-000001`), com aprovação
  quatro olhos pelo usuário `revisor`.
- `tools/plm/teamcraft_docs_b.py`: segunda liberação — `PL-001`/`PL-002` rev. B e
  `PL-003` rev. A na ECO `CHG-000002`.
- `tools/plm/teamcraft_backup.sh`: dump `pg_dump -Fc` dentro do contêiner, tar do
  vault (sem o cache de previews), `SHA256SUMS`, instruções de restauração e
  retenção de 7 pacotes.
- Instância TeamCraft em `http://127.0.0.1:8080` (loopback): 24 itens no grupo
  `PS-001`, BOM e arquivos do modelo (`.sc`, STEP, 3MF, cinco renders), documentos
  com PDF/DXF/CSV, preview 3D pelo 3MF.
- MCP do TeamCraft no OpenCode (`~/teamcraft/mcp.sh`, token de escopo `mcp_only`):
  consulta de itens, BOM, onde usado, impacto e ECOs; não libera nem aprova.

### Alterado
- `PS-001-PL-001` sobe para **rev. B**: adota o TeamCraft, mapeia os estados
  (`in_work`/`in_review`/`released`/`obsolete`), separa autor e aprovador, inclui a
  ECO no fluxo de mudança, atualiza checklist, ferramentas e pendências.
- `PS-001-PL-002` sobe para **rev. B**: registra o `PL-003`, o grupo/ECO do TeamCraft
  e as revisões substituídas.
- `tools/plm/build.sh`: gera o PDF do `PL-003`.
- `README.md`: versão 0.18.0, seção **PDM (TeamCraft)** e pacote `dist/v0.18.0/`.

### Verificação
- `readyz`: banco, vault e versão 0.2.7 ok; `GET /api/v1` com os endpoints esperados.
- 24 itens do grupo `PS-001` em `released`; BOM do conjunto com 16 linhas; 6
  referências de documento; `CHG-000001` e `CHG-000002` aprovadas pelo `revisor`.
- Backup gerado e conferido (`sha256sum -c`), com dump lido por `pg_restore -l`.
- `dist/v0.18.0/`: 13 arquivos, `SHA256SUMS` verificado; PDFs `PL-001` rev. B,
  `PL-002` rev. B e `PL-003` rev. A gerados sem aviso.

## [0.17.1] — 2026-11-14

### Alterado
- STEP e 3MF **regerados a partir do modelo aprovado** (`v0.15.0`): as exportações em
  `cad/solidcraft/` eram de 13/11, anteriores ao secundário reencaminhado e ao carretel.
  STEP AP242 com 2.059.738 bytes; 3MF com 5.092.530 bytes. Ambos são derivados e ficam
  fora do git (`.gitignore`), mas agora correspondem ao `PS-001.sc` da tag `v0.15.0`.
- Prancha `DR-001` regerada: a altura do envelope estava impressa como 313,1 na tabela de
  dados e 312,8 na cota; o `measure` dá **312,7 mm**. Corrigido nos dois lugares, a marca
  "A" da vista frontal foi substituída por nota (não ancorava na geometria) e a BOM
  passou a caber na moldura. Sem mudança de forma: continua rev. A, com sha256
  `8d61f09661bf6256…` para o DXF e `7850552f3876d749…` para o PDF.

## [0.17.0] — 2026-11-14

**Marco: prancha 2D A2 publicada (`PS-001-DR-001` rev. A).** O desenho é montado a partir
das projeções exportadas do modelo aprovado — nenhuma forma é desenhada à mão.

### Adicionado
- `tools/draw/sheet.py`: monta a folha A2 a partir de `out/draw/v017/{frente,lado,topo,iso,
  detalhe}.dxf` (exportados por `file.export_view_dxf`), desenhando moldura, vistas em
  1º diedro a 1:2, **detalhe A** do conjunto magnético a 1:1, cotas de envelope, lista de
  materiais lida do `BOM.csv`, dados principais, notas e carimbo.
- `PS-001-DR-001` rev. A: `out/draw/v017/PS-001-DR-001_rA_prancha-a2.dxf` (12.465
  entidades, camadas `CONTORNO`/`COTA`/`TEXTO`/`TABELA`) e o PDF A2 594 × 420 mm.
- `tools/plm/build.sh`: o pacote de liberação passa a incluir a prancha verificada
  (`PS-001-DR-001_rA_prancha-a2.pdf` + `.dxf`).
- Detalhe A exportado com o restante dos corpos oculto (`browser.visibility`), o que dá a
  vista limpa do núcleo, carretel, secundário e cantoneiras sem recorte manual de geometria.

### Alterado
- `PS-001-CO-001` sobe para **rev. B**: a pendência "prancha 2D com cotas de montagem"
  passa a apontar o `DR-001` publicado.
- `README.md`: versão 0.17.0, prancha marcada como publicada e seção de desenho 2D.

### Corrigido
- Parser DXF do gerador: `LINE` lê o segundo vértice em 11/21 (antes só 10/20, o que
  descartava todas as linhas) e só o vazio final do arquivo é removido — vazios internos
  são valores válidos.
- `SKETCH` é descartado na leitura: os traços de sketch do modelo estendiam o bbox e
  deslocavam a vista.
- Prisma de leitura da BOM: a coluna `MATERIAL` saiu do quadro (texto truncado); material,
  dimensões e volumes ficam no `PS-001-LM-001`.

### Verificação
- `ocs_audit` (dxf, 2018): 0 erro, 0 aviso, `lossless: true`, 0 entidade desconhecida.
- `save_verified` → AC1032, 12.465 entidades preservadas, sha256 `ad84cf7a5597c6ea…`.
- BOM da prancha e `BOM.csv` têm os mesmos 16 itens.

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

[0.17.1]: #0171--2026-11-14
[0.17.0]: #0170--2026-11-14
[0.16.0]: #0160--2026-11-14
[0.15.0]: #0150--2026-11-14
[0.14.0]: #0140--2026-11-14
[0.12.0]: #0120--2026-11-13
[0.1.0]: #010--2026-11-11
