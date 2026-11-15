# Identidade visual — Brasa

Logos do projeto **Brasa** (estudo do estanhador 550 W / 127 V) e da instância
**Brasa PLM** do TeamCraft. Feitos no VectorCraft (`ai.storyteller.vectorcraft`,
0.22.0), com fonte editável versionada.

| Arquivo | Uso | Tamanho |
|---|---|---|
| `brasa-wide.vectorcraft` / `.svg` / `.png` | cabeçalho e tela de entrada do TeamCraft, barra de título do app desktop | 600 × 120 px (5:1), fundo transparente |
| `brasa-square.vectorcraft` / `.svg` / `.png` | ícone da aba, rodapé da página e trilho de navegação do desktop | 256 × 256 px (1:1) |

O SVG leva o texto em curvas: o logo não depende da fonte DejaVu Sans estar
instalada no navegador. O PNG é a referência raster (72 ppi, 1 px por ponto).

## Desenho

- **Marca:** chama em dois tons dentro de um quadrado arredondado com gradiente.
  A chama externa é creme e a interna é o laranja escuro do fundo; lê igual em
  tema claro e escuro.
- **Wordmark:** `BRASA` em DejaVu Sans Bold, tracking 40/1000 em, alinhado à
  base da marca.
- **Paleta:**

| Cor | Uso |
|---|---|
| `#E4560F` → `#A93007` | gradiente do quadrado (topo → base) |
| `#FFF1E0` | chama externa |
| `#D6450E` | wordmark (contraste 4,5:1 no branco e 4,2:1 no fundo escuro `#101216`) |
| `#A93007` | chama interna |

## Regerar

```sh
branding/build.sh            # regera os .svg e .png a partir dos .vectorcraft
branding/build.sh --check    # confere se os exports correspondem às fontes
```

Precisa do flatpak `ai.storyteller.vectorcraft` (VectorCraft 0.22.0) com acesso
a esta pasta. A exportação é determinística; `--check` falha se um export ficou
para trás.

## Aplicar no TeamCraft

Administração → **Branding** (`/admin/branding`) → enviar `brasa-wide.svg` em
*Wide logo* e `brasa-square.svg` em *Square logo*. Regras do TeamCraft 0.2.7:

- PNG, JPEG, WebP ou SVG, até 512 KiB; bitmap até 4096 px por lado;
- SVG sem scripts, `foreignObject`, entidades ou links externos (só `#id` e
  `data:image/…`);
- um único logo wide para os temas claro e escuro — por isso o fundo
  transparente e as cores de contraste equilibrado.

Os logos ficam no banco (`branding_logos`), então entram no backup
(`tools/plm/teamcraft_backup.sh`) e voltam na restauração. Cada envio é
registrado na auditoria (`branding.set`).

## Direitos

Fazem parte do conteúdo próprio do projeto, sob **CC BY-NC-SA 4.0** (ver
[`../LICENSE`](../LICENSE)). Não usam marca de terceiro.
