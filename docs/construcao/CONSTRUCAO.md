# 1. Escopo e limites

Este guia descreve **como o Brasa (`PS-001`) foi decomposto e montado no modelo** e quais
critérios tornam cada etapa aceitável. Ele serve para ler o CAD, revisar o projeto e
entender a função de cada peça.

> **Não é instrução de fabricação.** O Brasa é uma reconstrução por observação, sem
> ensaio elétrico, sem certificação e sem análise de isolação do produto original. As
> etapas abaixo reproduzem a lógica de montagem do estudo; executá-las fisicamente em
> 127 V é decisão e risco de quem executa. Ver [LEGAL.md](../../LEGAL.md) §7 e o manual
> [`docs/uso/USO.md`](../uso/USO.md).

A lista de materiais é a BOM do conjunto `PS-001` no PLM; `BOM.csv`, nesta pasta, é a
exportação dela. Números de volume e envelope vêm do `measure` do modelo aprovado em
`v0.15.0`. O desenho de conjunto é a prancha A2 (`out/draw/`, derivada do modelo) — vistas
em 1º diedro a 1:2, o detalhe do conjunto magnético a 1:1 e as cotas de envelope.

# 2. Visão geral

```
        ┌──────────────┐
        │ Núcleo EI-75 │  pacote 75 × 75 × 35 + 4 cantoneiras M5
        └──────┬───────┘
               │
   ┌───────────┴───────────┐
   │ Carretel + primário   │  ~700 AWG 28, 127 V
   │ (Bobina)              │
   └───────────┬───────────┘
               │
   ┌───────────┴───────────┐
   │ Secundário (1 tira)   │  2 × 9 mm, 2,5 voltas
   └───────────┬───────────┘
               │
   ┌───────────┴───────────┐
   │ Ponta em U + postas   │  Cu Ø4,5; M5 em X 46
   └───────────┬───────────┘
               │
   ┌───────────┴───────────┐
   │ Cabo, chave, cabo de  │  madeira; tecla; prensa-cabo
   │ força                 │
   └───────────────────────┘
```

Subconjuntos: (A) magnético, (B) primário, (C) secundário, (D) ponta, (E) empunhadura e
comando. A ordem de montagem segue A → B → C → D → E porque cada etapa fecha o acesso à
anterior.

![Vista de perfil do conjunto montado: ponta em U à direita, transformador no topo e cabo na base](renders/PS-001_perfil_rA.png){width=58%}

# 3. Ferramentas e cuidados

| Necessidade | Ferramenta |
|---|---|
| Medição | paquímetro 0,05 mm, régua, esquadro |
| Elétrica | multímetro, miliohmímetro (4 fios) ou fonte/amperímetro, megômetro 500 V |
| Mecânica | chaves M5, alicate, lima, broca Ø 5,2 e Ø 6,2 |
| Enrolamento | bobinadeira manual ou torno lento, fita isolante, papel/mica |
| Conferência | acesso ao `PS-001.sc` no SolidCraft para `measure` |

Regra de bancada: cada etapa termina com medição registrada. Sem número, a etapa não
fecha — é o mesmo critério do plano (`docs/plm/PLANO.md` §4).

# 4. Etapas

## Etapa 1 — Núcleo (subconjunto A)

1. Empilhar as chapas EI-75 alternando a direção do "E" e do "I" para reduzir o entreferro.
2. Prensar o pacote até 35 mm e fixar com as quatro cantoneiras (chapa 3 mm,
   15,5 × 13 × 75), uma em cada canto, com parafuso M5 passante.
3. Conferir esquadro e a janela: **12,5 × 50 mm** livres, perna de **12,5 mm**.

**Aceitação:** envelope 75 × 75 × 35 mm (±0,5); janela sem rebarba; pacote sem folga
entre chapas; cantoneiras sem invadir a janela.
**Ponto de inspeção IP-1** — registrar altura do pacote e largura da janela.

## Etapa 2 — Carretel e primário (subconjunto B)

1. O carretel é uma peça só: alma 33 × 43 × 40 mm (Z ±20) e flanges 37 × 47 × 3 mm
   (Z 19…22 e −22…−19), com furo 25 × 35 mm passante para a perna central. Cantos
   verticais com R8, topos planos.
2. Enrolar ~700 espiras de AWG 28 em camadas, com papel entre camadas.
3. Deixar ~150 mm de ponta de cada lado para a ligação com a chave.
4. Fixar as pontas e cobrir o enrolamento com uma camada de fita.

**Aceitação:** o carretel desliza sobre a perna central **sem forçar e sem folga
excessiva**; enrolamento sem espira cruzada; resistência do primário na faixa esperada
(§5); nenhuma espira em contato com o núcleo.
**Ponto de inspeção IP-2** — resistência do primário e continuidade das pontas.

## Etapa 3 — Secundário (subconjunto C)

Esta é a etapa crítica do projeto: o secundário é **uma tira contínua**, sem emenda.

1. Preparar **uma** tira de cobre de 2 × 9 mm, com ~0,7 m, pontas já aplainadas.
2. Dar **2,5 voltas** em hélice em volta do conjunto núcleo + carretel, com passo
   **12,8 mm**: entrada na face +Y em **Z +16**, saída na face −Y em **Z −16**.
3. A tira passa pelas duas janelas do núcleo — X **9,17** e X **−30,83** — sem tocar em
   núcleo, carretel ou cantoneiras.
4. As duas pontas, no lado da ponteira, contornam o grampo **por fora**, em **X 31,7**:
   a face externa do grampo está em 29,67, então sobram **1 mm** de folga.
5. Isolar a tira do primário com mica/papel entre os enrolamentos.

**Aceitação:** continuidade de ponta a ponta; **nenhum contato** com núcleo, carretel ou
grampo; folga de 1 mm mantida na região do grampo; passo uniforme.
**Ponto de inspeção IP-3** — teste de continuidade e conferência de folga com lâmina de
1 mm (o mesmo valor validado por `inspect.clearance` no CAD).

![Detalhe: tira do secundário contornando o grampo por fora e entrando nas pastilhas](renders/PS-001_trafo_rA.png){width=66%}

> Por que faixa e não fio: com 2,5 voltas e ~100 A, a seção precisa ser grande e a
> espessura pequena. A tira de 18 mm² cabe na janela de 12,5 mm e dissipa melhor que um
> fio redondo de mesma seção. Modelar como um único `sweep` também eliminou as juntas
> que falhavam por faces coincidentes nas versões 0.1–0.13.

## Etapa 4 — Ponta e postas (subconjunto D)

1. Conformar o tubo de cobre Ø 4,5 × 0,75 mm em U, com os braços indo de X 34 a X 96,1.
2. Achatar as extremidades e abrir os furos **Ø 6,2 mm** nas pastilhas (18 × 3 × 10 mm).
3. Fixar cada braço com parafuso M5 em **X 46**; o conjunto inferior é espelhado
   (cabeça em Y −9…−3, porca em Y 2…6).
4. As pontas do secundário entram por baixo das pastilhas — a união é parafusada, não
   soldada, para permitir troca da ponta.

**Aceitação:** os dois braços no mesmo plano e paralelos; parafuso passa nos dois furos
sem forçar; aperto firme — conexão frouxa aquece e derrete a solda; ponta alinhada ao
eixo do cabo.

## Etapa 5 — Empunhadura e comando (subconjunto E)

1. Usinar o cabo em madeira (~167 mm, loft de 10 seções, topo largo).
2. Montar a chave (bezel 7 × 28 × 37 mm) e a tecla (5,5 × 18 mm) na face +Y.
3. Passar o fio do primário **dentro** do cabo, do transformador até a chave.
4. Instalar prensa-cabo e cabo de força (2 × 0,75 mm², plugue NBR 14136) na base.

**Aceitação:** a mão não alcança partes metálicas energizadas; a tecla retorna sozinha;
o cabo de força não se move quando tracionado (alívio de tração efetivo); nenhum fio
esmagado pelo prensa-cabo.

# 5. Ensaios e valores esperados

| Ensaio | Como | Esperado | Se falhar |
|---|---|---|---|
| Continuidade do primário | multímetro nos terminais da chave | ~**25 Ω** (700 espiras AWG 28, ~118 m); 20–35 Ω aceitável | espira rompida ou curto entre camadas |
| Continuidade do secundário | miliohmímetro 4 fios | **0,5–1,5 mΩ** | emenda ruim, pastilha solta |
| Isolação primário × secundário | megômetro 500 V DC | ≥ **2 MΩ** (referência de norma; não ensaiado neste estudo) | umidade, fita perfurada, espira encostando |
| Isolação primário × núcleo | megômetro 500 V DC | ≥ **2 MΩ** | carretel trincado |
| Primeira energização | **lâmpada em série** com o primário | lâmpada apaga/quase apaga; sem estalo nem cheiro | curto no primário ou secundário fechado |

Ordem obrigatória: continuidade → isolação → primeira energização com lâmpada em série.
Nunca energizar direto na tomada para "testar".

> Os valores de resistência são **cálculo**, não medição: seção AWG 28 (0,081 mm²),
> resistividade do cobre 0,0175 Ω·mm²/m e perímetro médio de espira de 168 mm.

# 6. Interfaces críticas

| Interface | Valor | Por que importa |
|---|---|---|
| Carretel × perna central | furo 25 × 35 sobre perna 25 × 35 | isolação e montagem sem folga |
| Secundário × grampo | 1 mm (X 31,7 contra face 29,67) | evita curto com a carcaça |
| Secundário × núcleo | sem contato | curto e aquecimento local |
| Ponta × posta | parafuso M5, furo Ø 6,2 | conexão de baixa resistência |
| Cabo × transformador | prensa-cabo na base | alívio de tração e isolação |
| Chave × cabo | face +Y, tecla 5,5 × 18 | alcance do polegar |

# 7. Riscos desta montagem

| Risco | Controle |
|---|---|
| Choque no primário | isolação do carretel, fio dentro do cabo, prensa-cabo, ensaio de isolação |
| Curto no secundário por contato com a carcaça | folga de 1 mm no grampo, mica entre enrolamentos |
| Aquecimento da conexão da ponta | aperto M5 e conferência de resistência |
| Queimadura ao montar | montar desenergizado; testar com lâmpada em série |
| Erro de tensão | 127 V; nunca ligar em 220 V sem trocar o primário |

# 8. Pendências

| # | Pendência | Efeito |
|---|---|---|
| 1 | Densidade por material | BOM sem massa; manual sem massa |
| 2 | Cotas finas de montagem (furação, folgas) | a prancha traz envelope e detalhe, não a cota de cada furo |
| 3 | Ensaio de isolação executado | critério de segurança sem evidência |
| 4 | Ciclo de trabalho declarado | operação depende de julgamento do usuário |

# 9. Histórico

Sem tabela de revisões: o histórico é o do git.

```sh
git log --follow -- docs/construcao/CONSTRUCAO.md
```
