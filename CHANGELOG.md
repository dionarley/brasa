# Changelog — PS-001

Formato inspirado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/);
versionamento [SemVer](https://semver.org/lang/pt-BR/), aplicado ao **modelo e à
documentação** (não a uma API). Enquanto a série for `0.x`, mudanças de forma podem
ocorrer em versões menores. Cada tag do git corresponde a um estado do arquivo
`cad/solidcraft/PS-001.sc`.

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

[0.14.0]: #0140--2026-11-14
[0.12.0]: #0120--2026-11-13
[0.1.0]: #010--2026-11-11
