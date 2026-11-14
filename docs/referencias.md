# Referências — PS-001

Registro das fontes usadas na reconstrução. **Nenhum destes materiais é
redistribuído** neste repositório (ver [`../LEGAL.md`](../LEGAL.md), seções 3 e 4):
os arquivos originais ficam em `ref/` e `docs/` apenas na cópia de trabalho local, fora
do git. Aqui estão autoria, origem e o que cada fonte contribuiu.

## 1. Produto estudado

| Fonte | Uso | Direitos |
|---|---|---|
| Anúncios do estanhador 550 W / 127 V, cabo de madeira — Mercado Livre, itens `MLB83995165997` e `MLA99450924224` (fotos salvas em `ref/photos/`) | forma geral, proporções, posição da chave, do cabo e da ponta; cor e acabamento | fotos dos vendedores; uso apenas como referência de estudo |

A marca do produto original não é reproduzida no projeto: o estudo adota o nome próprio
**Brasa** e identifica a fonte apenas pelo anúncio e pelas fotos.

As fotos não são versionadas e não integram nenhuma imagem publicada do projeto. Os
renders do modelo são gerados no SolidCraft a partir da geometria reconstruída.

## 2. Artigos técnicos (Instructables)

| Título | Autor | Publicação | Uso |
|---|---|---|---|
| How to Built Cheap and Trusty Soldering Gun Out of Old Transformer | utsubedi | 2016-01-18 | princípio do secundário de fita de cobre e montagem sobre transformador reaproveitado |
| Soldering Gun — Pistola De Solda De Aquecimento Rápido | Cion Cassiano | 2016-07-14 | arranjo geral de pistola com transformador, cabo e gatilho |
| DIY Hot Air Soldering Iron Using 12–18 V DC at 2–3 A | OzzyRoo | 2007-09-10 | referência de segurança em aquecimento resistivo (não usado no modelo final) |
| Coil Winder (Automatic) — Bobinadeira Automatizada | — | — | noção de execução do primário (enrolamento), sem transposição direta |

Cópias locais: `docs/*.pdf` e texto extraído em `docs/extracted/` (não versionados).
Uso de citação e estudo, com autoria e origem indicadas (Lei 9.610/98, art. 46, VIII).

## 3. Teoria de transformadores

| Fonte | Uso |
|---|---|
| Capítulo "Transformer" (`docs/FCBIQ6KIJM04YMA.pdf`, 96 p., metadados `Chp-32.PMD`, autor não identificado) | equação da FEM, relação de espiras, perdas no núcleo e no cobre, ensaio de curto-circuito, regulação |

Usado para conferir ordem de grandeza de espiras e corrente do secundário. O texto é de
terceiro (material didático digitalizado) e não é redistribuído.

## 4. Normas e boas práticas (não incluídas)

Citadas como critério de projeto e de segurança; são documentos pagos/normativos e não
fazem parte do repositório:

- **ABNT NBR 5410** — instalações elétricas de baixa tensão.
- **IEC 60335-2-45** — segurança de ferros de soldar e ferramentas térmicas similares.
- **NR-10** — segurança em instalações e serviços em eletricidade.
- **Regulamento de certificação do Inmetro** aplicável a ferramentas elétricas de uso
  doméstico (verificar a portaria vigente antes de qualquer fabricação).
- **ISO 286 / ISO 2768** — ajustes e tolerâncias gerais (para a futura prancha 2D).
- **NBR 14136** — plugues e tomadas 127/220 V (cabo de força).

## 5. Conversa de apoio (não técnica)

`docs/extracted/pistola e solda caseira.txt` — exportação de uma conversa com assistente
de IA sobre o tema. Foi usada apenas como **lista de riscos** (choque, incêndio,
aquecimento do secundário); não forneceu medidas nem valores adotados. Não é versionada.

## 6. O que veio de onde (rastreabilidade resumida)

| Elemento do modelo | Base |
|---|---|
| Núcleo EI-75, janela 12,5 × 50, perna 12,5 | série comercial EI (dimensões normalizadas) |
| Primário ~700 espiras, AWG 28 (127 V) | equação da FEM + densidade de corrente usual para transformador de 550 W |
| Secundário em fita 2 × 9 mm, 2,5 voltas | prática dos artigos + corrente estimada no secundário |
| Cabo em "cabeça de prego" | silhueta das fotos + ajuste de empunhadura |
| Chave, prensa-cabo, cantoneiras, parafusos | fotos do produto + padronização M5 |
| Cotas e volumes | medidos no modelo CAD (SolidCraft), não na peça real |

## Como atualizar

Ao adicionar uma referência: registre título, autor, data, link estável quando houver e
o que foi efetivamente usado. Se o material tiver direitos de terceiro, guarde o arquivo
fora do git e cite apenas a referência aqui.
