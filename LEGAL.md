# Aviso legal — PS-001

Este documento explica **o que este repositório é**, **o que a licença cobre**, **o que
ela não cobre** e **quais são os riscos de segurança**. Ele acompanha o `LICENSE` e
prevalece em caso de dúvida sobre o escopo. Nada aqui é aconselhamento jurídico: se você
pretende fabricar, vender, importar ou publicar derivados, procure um advogado.

Data desta revisão: 2026-11-14.

---

## 1. Natureza do projeto

O PS-001 é um **estudo de modelagem paramétrica** de uma pistola de solda por
transformador (estanhador) de 550 W / 127 V, feita a partir de:

- fotos públicas de anúncios do produto;
- artigos públicos sobre estanhadores caseiros;
- catálogos e tabelas de núcleos de transformador EI;
- normas e boas práticas de segurança elétrica.

O objetivo é **documentar e estudar** a geometria, a montagem e a função de cada peça
(como exercício de engenharia e de CAD), e não reproduzir industrialmente o produto.
O modelo é uma **reconstrução aproximada por observação**, não um projeto original do
fabricante, não um desenho de fabricação e não uma peça de reposição.

Não há vínculo, patrocínio, aprovação ou representação de nenhuma marca.

## 2. Licença do conteúdo próprio

O conteúdo produzido pelo autor — o modelo CAD (`cad/solidcraft/PS-001.sc`), os textos,
as tabelas, os scripts e as imagens geradas pelo próprio autor — é licenciado sob
**Creative Commons Atribuição-NãoComercial-CompartilhaIgual 4.0 Internacional**
(CC BY-NC-SA 4.0). O texto integral está em [`LICENSE`](LICENSE).

Em resumo:

| Você pode | Você deve | Você não pode |
|---|---|---|
| copiar, estudar, modificar e compartilhar o modelo e os textos | dar crédito ao autor e ao projeto, indicar alterações e manter o aviso de licença | usar para vantagem comercial ou compensação monetária |
| publicar derivados | licenciar o derivado sob CC BY-NC-SA 4.0 (ou compatível) | impor restrições adicionais ou medidas tecnológicas que limitem o uso |
| imprimir, montar e usar para estudo próprio | manter o aviso de segurança e a ausência de garantias | sugerir endosso do autor, do fabricante ou de qualquer marca |

Pontos de atenção:

- **"NãoComercial" é uma condição da licença, não uma sugestão.** Publicar o modelo em
  site com anúncios, usá-lo em aula paga, vendê-lo ou incluí-lo em produto/serviço
  cobrado está fora do escopo.
- A licença é **irrevogável** para quem já recebeu o material: não é possível "fechar"
  depois.
- O autor pode oferecer **licença separada** para o próprio conteúdo (por exemplo,
  permissão comercial), mas isso **não** resolve direitos de terceiros (seção 3 e 4).
- A CC BY-NC-SA **não licencia patentes nem marcas** (Seção 2(b)(2) do texto legal).
- O produto físico construído não é coberto pela licença: ele é seu, com os riscos e as
  responsabilidades da seção 7.

## 3. Marca "The Black Tools" e outras marcas

- "The Black Tools" e demais nomes comerciais citados pertencem aos seus titulares.
- O nome aparece apenas em **referência nominativa**, para identificar o produto
  estudado ("reconstrução de estudo do estanhador vendido sob esta marca").
- **Não há** uso de logotipo, identidade visual, embalagem ou alegação de origem.
- Os renders e o modelo **não reproduzem** logotipo ou etiqueta do produto.
- Se você publicar derivados, **não** use a marca no nome do seu projeto, no título de
  vídeos ou em material promocional de forma que sugira origem ou aprovação. Descreva
  como "compatível com" ou "inspirado em", sem destaque visual da marca.
- Registro de marca confere ao titular o direito de **coibir confusão** e uso em
  economia (Lei 9.279/96, arts. 123–132 e 189). Referência informativa a produto
  existente é, em regra, admissível; uso como marca própria, não.

## 4. Referências de terceiros

Os materiais usados como referência (fotos de anúncios, PDFs de artigos, textos
extraídos, exportações de conversas) **não são redistribuídos neste repositório** e
estão listados em [`docs/referencias.md`](docs/referencias.md), com autoria e origem.

- Ficam fora do versionamento (`.gitignore`): `ref/`, `docs/*.pdf`, `docs/extracted/`.
- O uso é de **estudo e citação**, com indicação de autor e origem, na medida
  justificada (Lei 9.610/98, art. 46, II e VIII).
- Textos e fotos continuam sob os direitos dos respectivos autores; a licença deste
  repositório não os alcança e não os torna reutilizáveis por terceiros.
- Se você é titular de algum material aqui citado e quer correção ou remoção, abra uma
  issue ou entre em contato: o ajuste é feito assim que identificado.

## 5. Desenho industrial, patentes e concorrência

Este é o ponto de maior risco jurídico de qualquer reconstrução de produto existente.

- **Desenho industrial** (Lei 9.279/96, arts. 95–113): a forma externa de um produto pode
  estar registrada — no Brasil por 10 anos, prorrogáveis por até mais 15. Um registro
  vigente dá ao titular o direito de impedir a reprodução da forma para fins comerciais.
- **Patentes** (arts. 40–57): podem cobrir o arranjo funcional (por exemplo, o secundário
  em fita e a ponta em U). Patente vigente impede exploração comercial independentemente
  de o modelo ter sido feito "do zero".
- **Concorrência desleal** (art. 195): inclui usar meio fraudulento para desviar
  clientela e divulgar/explorar informações confidenciais obtidas por meio ilícito.
  Estudo de produto adquirido ou exposto publicamente não é, por si, ilícito, mas a
  **comercialização de cópia** pode ser.
- **Outras jurisdições**: desenho comunitário não registrado na UE (3 anos), design
  patents nos EUA e direitos autorais sobre a aparência podem alcançar publicações na
  internet. Não há análise de liberdade de operação (freedom to operate) feita aqui.
- **Consequência prática**: este repositório é adequado para **estudo, ensino, pesquisa
  e uso privado**. Fabricar em escala, vender, importar ou distribuir como produto
  exige busca de anterioridade e parecer jurídico próprios.

## 6. Direito autoral sobre o modelo

- O modelo é obra intelectual do autor na parte em que resulta de escolhas próprias
  (parametrização, decomposição em peças, simplificações, textos e desenhos).
- Na medida em que reproduza a **forma** de um produto de terceiro, ele pode ser
  considerado, em algumas jurisdições, obra derivada ou reprodução de desenho
  protegido. Essa qualificação **não é resolvida por este aviso** nem pela licença.
- Direitos morais (autoria e integridade) não são licenciados; a atribuição é exigida
  pela licença e deve ser mantida.
- O nome "PS-001" e a organização do projeto são identificadores deste estudo, não uma
  designação oficial do produto.

## 7. Segurança, responsabilidade técnica e certificação

**Este modelo não é uma ferramenta certificada e não é instrução de fabricação.**

- O equipamento original opera em **127 V CA** e consome 550 W. O secundário trabalha em
  baixa tensão e **alta corrente** (ordem de 100 A), com fita de cobre que aquece por
  efeito Joule.
- Riscos reais: choque elétrico, curto-circuito, sobreaquecimento do secundário,
  incêndio do cabo de madeira, queimaduras na ponta, solda de estanho projetada.
- Um aparelho assim **não** é certificado. No Brasil, ferramentas elétricas de uso
  doméstico estão sujeitas a certificação compulsória e ao regulamento do Inmetro
  aplicável, além do Código de Defesa do Consumidor (Lei 8.078/90) quanto a defeito e
  responsabilidade do fornecedor. **Não fabrique para venda, doação em massa ou uso por
  terceiros** sem projeto elétrico assinado por responsável técnico e certificação.
- Se ainda assim construir para uso próprio: use DR de 30 mA, fusível no primário,
  isolação reforçada entre primário e secundário, separação física dos circuitos,
  aterramento quando aplicável, e nunca deixe ligado sem supervisão. Referências: NR-10,
  IEC 60335-2-45 (ferros de soldar) e ABNT NBR 5410.
- As tabelas de fio, espiras e corrente do projeto são **estimativas de estudo**, não
  dimensionamento executivo verificado.
- O autor **não se responsabiliza** por danos pessoais, materiais ou elétricos
  decorrentes do uso das informações, do modelo ou de peças construídas a partir dele.

## 8. Dados pessoais (LGPD)

- O repositório **não contém** dados pessoais de terceiros: não são versionados nomes de
  vendedores, contatos, endereços, fotos de pessoas ou exportações de conversas.
- Contribuições não devem incluir dados pessoais, capturas de tela com informações de
  conta, nem material de terceiros sem autorização.
- Se houver contribuição com dados pessoais por engano, ela será removida do histórico.

## 9. Contribuições

- Ao contribuir, você concorda que sua contribuição seja licenciada sob CC BY-NC-SA 4.0
  (entrada e saída com a mesma licença) e declara ter direito para licenciá-la.
- Contribuições com material de terceiros (fotos, trechos longos, desenhos de catálogo)
  não são aceitas.
- Marque no commit o que é seu e o que é referência (`Signed-off-by` é bem-vindo).

## 10. Garantias

O material é fornecido **"como está"**, sem garantia de exatidão dimensional,
funcionalidade, adequação a um fim ou não violação de direitos de terceiros (Seção 5 do
`LICENSE`). Medidas foram conferidas no CAD, mas não substituem metrologia de peça real.

## 11. Como citar

```
DIONARLEY. PS-001 — Pistola de solda por transformador (estudo), versão 0.14.0.
Modelo CAD paramétrico. 2026. Licenciado sob CC BY-NC-SA 4.0.
```

Ao citar imagens, indique a versão (tag do git) e que se trata de reconstrução de
estudo, sem vínculo com o fabricante.

## 12. Lei aplicável

Este aviso é regido pela legislação brasileira. Nada aqui cria relação advocatícia,
sociedade ou representação. Em caso de conflito entre este texto e o `LICENSE`, o texto
legal da CC BY-NC-SA 4.0 prevalece quanto ao uso do conteúdo licenciado.
