# 1. O que este documento é

Manual de **uso** do estanhador **Brasa** (`PS-001`): o que a máquina é, como funciona, o
que se pode e o que não se pode fazer com ela, e como ler essa informação junto ao modelo
3D.

> **Aviso.** O Brasa é um **estudo de modelagem**. O texto descreve o produto original e
> o comportamento esperado de um estanhador por transformador, mas **não é manual do
> fabricante, não é instrução de fabricação e não substitui a documentação de um produto
> certificado**. O equipamento opera em 127 V e o secundário trabalha em curto, com
> corrente muito alta: choque, queimadura e incêndio são riscos reais. Ver
> [LEGAL.md](../../LEGAL.md) §7.

# 2. Identificação

| Item | Valor |
|---|---|
| Produto | **Brasa** — estanhador (pistola de solda) 550 W, 127 V |
| Código do projeto | `PS-001` |
| Princípio | transformador abaixador com secundário de fita de cobre em curto pela ponta |
| Aplicação | solda por fusão em eletrônica, fiação e lataria fina; corte térmico de plástico |
| Modelo de referência | `cad/solidcraft/PS-001.sc` na tag `v0.15.0`, 22 corpos, 448,4 cm³ |
| Envelope | ≈ 148 × 52 × 313 mm (X × Y × Z) |

![Aspecto geral do modelo, transformador no topo e empunhadura de madeira abaixo](renders/PS-001_iso_rA.png){width=78%}

**Brasa** é o nome próprio deste estudo; não é a marca do produto original. Não há
vínculo com o fabricante nem uso de marca de terceiro como identidade do projeto.

# 3. Uso pretendido

## 3.1 Pretendido

- Aquecer a ponta por efeito Joule para **soldar** componentes, terminais e fios de
  pequeno porte.
- Aquecer e **retrair** terminais, e cortar/moldar plástico fino com a ponta.
- Operação **intermitente**, em bancada, com a peça apoiada e a mão livre.

## 3.2 Não pretendido

- Uso contínuo ou industrial, em linha de produção.
- Solda de estruturas, tubulação, lataria grossa ou qualquer coisa que exija calor
  sustentado.
- Atmosfera com solvente, poeira combustível ou material inflamável próximo.
- Operação por crianças, por pessoas não treinadas ou sem supervisão.
- Uso molhado, ao ar livre sob chuva, ou com cabo/ponta danificados.
- Adaptação de tensão (220 V) sem trocar o primário: o transformador é projetado para
  127 V.

# 4. Especificações

| Grandeza | Valor | Origem |
|---|---|---|
| Tensão de alimentação | 127 V ~ 60 Hz | produto original |
| Potência nominal | 550 W | produto original |
| Corrente no primário | ≈ 4,3 A (550 W / 127 V) | cálculo |
| Primário | ~700 espiras de fio AWG 28 em carretel 37 × 47 × 44 mm | modelo |
| Relação de espiras | ≈ 280 : 1 (700 / 2,5) | modelo |
| Tensão de secundário (vazio) | ≈ 0,45 V | cálculo (127 / 280) |
| Secundário | 2,5 voltas de fita de cobre 2 × 9 mm (18 mm²) | modelo |
| Corrente de secundário em curto | ordem de **100 A** | estimativa de projeto |
| Temperatura da ponta | ~300–400 °C, em 3–5 s | comportamento típico da classe |
| Ponta | tubo de cobre Ø4,5 mm, parede 0,75 mm, em U | modelo |
| Massa | **não informada** | densidade uniforme no CAD não representa a peça |
| Isolação | classe do produto original não declarada | ver §8 |

Os números de corrente e temperatura são **ordens de grandeza coerentes com a classe**,
não medições. Medir exige instrumento e ensaio — que este estudo não fez.

# 5. Como funciona

1. O primário (~700 espiras) é ligado à rede de 127 V e cria fluxo no núcleo EI-75.
2. O secundário tem **2,5 voltas** de fita de cobre: a relação de 280 : 1 derruba a
   tensão para menos de 1 V e multiplica a corrente.
3. A ponta em U **fecha o secundário**: é um curto-controlado. Toda a energia do
   transformador se dissipa no cobre da ponta e na junta a soldar.
4. Por isso a máquina aquece em segundos — e por isso **não pode ficar ligada**: em
   repouso, o curto aquece a ponta, o secundário e o primário sem produzir trabalho.

A topologia é a mesma de um transformador de solda a resistência: poucas espiras, seção
grande, tensão baixíssima. Quem controla a temperatura é o **tempo de gatilho**, não um
termostato.

![Conjunto magnético: núcleo EI-75, carretel do primário e a tira do secundário em 2,5 voltas](renders/PS-001_trafo_rA.png){width=72%}

# 6. Partes e controles

| Parte | Corpo no modelo | Função |
|---|---|---|
| Núcleo EI-75 | `Nucleo` | circuito magnético, 75 × 75 × 35 mm |
| Carretel + primário | `Bobina` | isola e posiciona as ~700 espiras |
| Secundário | `Secundario` | 1 tira contínua de Cu, 2,5 voltas |
| Ponta em U | `Ponta_U` | elemento de aquecimento e eletrodo de solda |
| Grampos e parafusos | `Canto_*`, `Parafuso_ponta_*` | fixação mecânica e elétrica das postas |
| Cabo | `Cabo` | empunhadura de madeira, isola e afasta a mão do calor |
| Chave e tecla | `Chave`, `Tecla` | comando do primário, na face +Y do cabo |
| Prensa-cabo e cabo de força | `Prensa_cabo`, `Cabo_forca` | entrada de rede e alívio de tração |
| Fio do primário | `Fio_primario` | ligação chave → bobina, enterrada no cabo |

Controles: **um** — a tecla. Não há termostato, nem ajuste de potência, nem indicador
luminoso no modelo estudado.

# 7. Operação

## 7.1 Antes de cada uso

1. Cabo de força e plugue íntegros, sem emenda, sem fio exposto.
2. Ponta firme nos grampos, sem folga e sem oxidação excessiva.
3. Corpo, cabo de madeira e prensa-cabo sem trinca.
4. Bancada seca, sem solvente, sem papel ou pano sob a ponta.
5. Ventilação: a solda gera fumaça de fluxo; trabalhe com exaustão ou janela aberta.

## 7.2 Ciclo de trabalho

1. Apoie a peça; aproxime a ponta **já posicionada** onde a solda vai ocorrer.
2. Pressione a tecla e conte: **3 a 5 s** para a ponta atingir a temperatura de trabalho.
3. Encoste o estanho na junta (não na ponta): a solda deve fluir em 1–3 s.
4. **Solte a tecla** assim que a junta estiver formada.
5. Espere a ponta esfriar antes de guardar — de 1 a 2 min ao ar, nunca em contato com
   plástico, pano ou papel.

## 7.3 Regime

O produto original **não declara ciclo de trabalho**. Trate como intermitente:

- uso típico: 5 s ligado para 15–30 s desligado;
- nunca deixe a tecla travada;
- se o cabo ou a bobina começarem a aquecer além do morno, pare: há curto ou espira em
  falta.

# 8. Segurança

| Risco | Como se manifesta | Controle |
|---|---|---|
| Choque elétrico | 127 V no primário, cabo/prensa-cabo danificado | inspeção antes do uso; nunca operar com a carcaça aberta; NBR 5410 e NR-10 |
| Queimadura | ponta a 300–400 °C, respingo de estanho | óculos, apoio, não tocar na ponta, deixar esfriar |
| Incêndio | ponta encostada em papel/pano/plástico; curto no secundário | bancada limpa, desligar da tomada ao terminar, não deixar sozinho |
| Fumaça de fluxo | irritação respiratória | exaustão local ou ambiente ventilado |
| Isolação | primário e secundário no mesmo núcleo | isolação do carretel e afastamento; classe do original **não declarada** |
| Falha do secundário | tira de cobre solta ou trincada | inspeção visual; não operar com solda fria ou faísca |

**Nunca** improvise a ligação do primário, não elimine o prensa-cabo, não substitua o
cabo de força por um mais fino e não ligue a máquina em 220 V.

# 9. Manutenção

| Item | Frequência | O que fazer |
|---|---|---|
| Ponta | cada uso | limpar a oxidação com escova/palha fina; estanhar a ponta após o uso |
| Parafusos dos grampos | mensal | reapertar; folga no grampo aquece a conexão e derrete a solda |
| Cabo de força | mensal | conferir dobra, isolação e prensa-cabo |
| Chave/tecla | mensal | conferir curso e retorno; tecla que não volta é risco |
| Interior | nunca pelo usuário | não abrir: 127 V e bobina acessíveis |

Não há peça de reposição neste projeto: o modelo é de estudo e a ponta é conformada, não
comprada.

# 10. Solução de problemas

| Sintoma | Causa provável | O que verificar |
|---|---|---|
| Não aquece | rede, chave, primário aberto | tomada, tecla, continuidade do primário |
| Aquece pouco | ponta mal fixada, oxidação, espira em curto | reapertar grampos, limpar ponta, medir continuidade do secundário |
| Aquece demais / cheiro de verniz | secundário em curto permanente, ciclo longo | desligar, deixar esfriar, revisar isolamento |
| Faísca no grampo | conexão frouxa | reapertar; não usar assim |
| Fusível abre | curto no primário | **não** trocar por valor maior; procurar a falha |
| Fumaça branca | fluxo queimando | reduzir tempo, usar fluxo adequado, ventilar |

# 11. Descarte

Ao fim da vida: cabo de força e fios (cobre/PVC) em reciclagem de eletrônicos; núcleo
(aço silicioso) e cantoneiras em metal; cabo de madeira em resíduo comum ou reuso;
ponta e secundário (cobre) em metal. Não incinere o transformador.

# 12. Como usar este manual com o modelo 3D

1. Abra `cad/solidcraft/PS-001.sc` no SolidCraft (ou inspecione o zip).
2. Procure o corpo pelo nome da tabela do §6 — os nomes são estáveis desde a 0.14.0.
3. Use `measure` para conferir volume e envelope; não confie em render para número.
4. Para a sequência de montagem, veja
   [`docs/construcao/CONSTRUCAO.md`](../construcao/CONSTRUCAO.md); para a lista de
   materiais, a BOM do conjunto `PS-001` no PLM (`docs/construcao/BOM.csv` é a
   exportação dela).

# 13. Histórico

Sem tabela de revisões: o histórico é o do git.

```sh
git log --follow -- docs/uso/USO.md
```
