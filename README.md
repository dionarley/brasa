# PS-001 — Pistola de solda por transformador (estudo)

**Licença:** [CC BY-NC-SA 4.0](LICENSE) (conteúdo próprio) · **Versão:** 0.15.0 ·
**Estado:** modelo 3D aprovado; prancha 2D em execução.

Reconstrução **de estudo** de um estanhador de 550 W / 127 V com transformador e
secundário de fita de cobre, modelado como peça paramétrica no SolidCraft a partir de
fotos públicas, artigos e teoria de transformadores. Não é projeto de fabricação, não é
peça de reposição e não tem vínculo com o fabricante — leia [LEGAL.md](LEGAL.md) antes
de reutilizar qualquer coisa.

## Estado atual

| Entrega | Situação |
|---|---|
| Modelo 3D paramétrico (`cad/solidcraft/PS-001.sc`) | **aprovado** — 22 corpos, 0 erros, 448,4 cm³ |
| Renders de conferência (`out/plot/ps001_v15_*.png`) | gerados (não versionados) |
| Exportações STEP/3MF | **antigas** (13/11) — reexportar da versão aprovada |
| Prancheta 2D (A2) | **em execução** — vistas, corte, detalhes, BOM |
| Versionamento e licença | concluído |

## Estrutura

```
cad/solidcraft/
  PS-001.sc        fonte da verdade: design paramétrico (zip com document.json)
docs/
  referencias.md   fontes, autoria e o que cada uma contribuiu
out/               renders, DXF e exportações (fora do git)
ref/               fotos e vetores de referência (fora do git, direitos de terceiros)
LEGAL.md           escopo da licença, marcas, desenho industrial, segurança
CHANGELOG.md       histórico por versão
```

## Modelo 3D

Um design no SolidCraft, sem montagem separada: cada peça é um corpo nomeado, com
histórico paramétrico. Medidas do `measure` atual:

| Peça(s) | Qtd. | Volume (cm³) | Observação |
|---|---:|---:|---|
| `Nucleo` | 1 | 148,90 | EI-75, 75 × 75 × 35 mm, janela 12,5 × 50 |
| `Bobina` | 1 | 23,44 | carretel: alma 33 × 43 e flanges 37 × 47 × 3 |
| `Secundario` | 1 | 10,26 | tira 2 × 9 mm, 2,5 voltas, sweep único |
| `Ponta_U` | 1 | 2,39 | tubo Ø4,5 + pastilhas de fixação (X 34…52) |
| `Cabo` | 1 | 215,00 | loft "cabeça de prego", 10 seções |
| `Chave`, `Tecla` | 2 | 9,52 | na face +Y do cabo |
| `Fio_primario` | 1 | 0,66 | enterrado no cabo |
| `Prensa_cabo`, `Cabo_forca` | 2 | 6,39 | saída pela base |
| `Canto_*` | 4 | 22,24 | cantoneiras do transformador |
| `Parafuso_canto_*` | 4 | 7,36 | M5 passante |
| `Parafuso_ponta_*`, `Porca_ponta_*` | 4 | 2,26 | fixação das postas, em X 46 |
| **Total** | **22** | **448,4** | |

Envelope: X −52,2…+96,1 · Y ±26,1 · Z −273,7…+39 mm (≈ 148 × 52 × 313 mm).

> A massa mostrada pelo CAD (~594 g) usa a densidade padrão de 1,29 g/cm³ para todos os
> corpos; não representa a peça real. Atribuir densidade por material é pendência.

### Transformador

Núcleo EI-75 de catálogo: perna 12,5 mm, janela 12,5 × 50 mm, pacote 35 mm
(75 × 75 × 35). Volume do transformador montado: **201,1 cm³** (+14,4 % sobre a versão
EI-57, que tinha 175,7 cm³).

### Secundário

Uma tira única de cobre de 2 × 9 mm que dá 2,5 voltas em hélice (passo 12,8 mm) em volta
do núcleo, entra na face +Y em Z +16, desce e sai na face −Y em Z −16, terminando nos
braços em "S" que alimentam as postas. Modelada como **um sweep e um corpo** — foi a
forma de garantir continuidade elétrica e evitar uniões por faces coincidentes.

As duas pontas (entrada e saída) contornam o grampo do lado da ponteira por fora, em
X = 31,7 (face externa do grampo em 29,67), com 1 mm de folga; o resto da hélice passa
pelas duas janelas do núcleo (X 9,17 e −30,83) sem tocar em núcleo, carretel ou grampos.

## Parâmetros principais

| Item | Valor |
|---|---|
| Núcleo | EI-75: 75 × 75 × 35 mm, janela 12,5 × 50, perna 12,5 |
| Primário | ~700 espiras AWG 28 (127 V) em carretel 37 × 47 × 44 (alma 33 × 43, flanges 3) |
| Secundário | 2,5 voltas de fita Cu 2 × 9 mm, passo 12,8 |
| Ponta | tubo Cu Ø4,5 (parede 0,75), em U, X 34…96,1 |
| Fixação das postas | parafuso M5 em X 46, furo Ø6,2 |
| Cantoneiras | 4 ×, 15,5 × 13 × 75, parafusos M5 passantes |
| Cabo | madeira, loft de 10 seções, ~167 mm, topo largo |
| Chave | bezel 7 × 28 × 37, tecla 5,5 × 18 |

## Abrir e editar

Requer o SolidCraft (app desktop) ou o servidor MCP equivalente. O `.sc` é um zip com
`document.json`:

```sh
unzip -l cad/solidcraft/PS-001.sc        # conteúdo
unzip -p cad/solidcraft/PS-001.sc document.json | head -c 400
```

Ao editar: mantenha os nomes dos corpos, use expressões nos campos que devem seguir
parâmetros, e feche cada sketch com `dof 0`. Depois de qualquer mudança, confira com
`measure` (volume e envelope) e gere os renders de conferência.

## Versionamento

- Repositório git **dentro de `diy_hot_gun/`** (branch `main`); tags `v0.x.y`.
- `PS-001.sc` é gravado pelo SolidCraft como zip: o diff não é legível, então o
  histórico útil é o par **(commit + tag)**; para inspecionar uma versão, faça checkout
  da tag e abra o `.sc`.
- Fora do git (`.gitignore`): `out/` (renders, DXF, STEP/3MF), `ref/` e `docs/*.pdf`
  (direitos de terceiros), backups `.bak`/`*_backup.sc`, `render.png`, `shot*.png`.
- Commits em português, no imperativo ("ajusta o secundário para sweep único").

```sh
git log --oneline --decorate
git show v0.14.0 --stat
git checkout v0.14.0 -- cad/solidcraft/PS-001.sc
```

## Licença e avisos legais

O conteúdo próprio (modelo CAD, textos, tabelas e imagens geradas pelo autor) está sob
**CC BY-NC-SA 4.0**: use, estude e compartilhe com atribuição, sem fins comerciais, e
licencie derivados sob a mesma licença.

Ficam **fora** da licença: a marca "The Black Tools" e demais marcas citadas; fotos,
PDFs e textos de terceiros (não redistribuídos, listados em
[`docs/referencias.md`](docs/referencias.md)); e eventuais direitos de desenho
industrial ou patente sobre o produto original. Detalhes, inclusive sobre fabricação e
venda, em [LEGAL.md](LEGAL.md).

## Segurança

O produto original opera em **127 V** e o secundário trabalha com corrente da ordem de
100 A. O modelo é de estudo: **não é certificado e não é instrução de fabricação**.
Construir, ligar ou modificar um equipamento assim envolve risco de choque elétrico,
incêndio e queimadura, e a responsabilidade é de quem constrói. Ver LEGAL.md, seção 7.

## Próximos passos

1. Aprovar (ou corrigir) o modelo 3D — revisão em andamento.
2. Atribuir densidade/material por corpo para massa realista.
3. Reexportar STEP/3MF a partir da versão aprovada.
4. Refazer a prancha 2D A2 do zero (vistas, corte, detalhes, BOM, cotas) no
   OpenCADStudio, com `ocs_audit` e `save_verified`.
