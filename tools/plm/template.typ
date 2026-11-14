// Template de documento do PS-001 para pandoc (writer typst).
// Variáveis vindas do front matter Markdown: title, subtitle, docid, revision,
// status, date, author, project, body.
#let docid = "$docid$"
#let rev = "$revision$"
#let docstatus = "$status$"
#let docdate = "$date$"
#let docauthor = "$author$"
#let docproject = "$project$"

#set document(title: "$title$", author: docauthor)

#set page(
  paper: "a4",
  margin: (top: 24mm, bottom: 18mm, left: 20mm, right: 18mm),
  footer: context {
    set text(size: 7.5pt, fill: luma(110))
    set par(justify: false)
    grid(
      columns: (1fr, auto),
      gutter: 6mm,
      [#docid · rev. #rev · #docstatus],
      [PS-001 · pág. #counter(page).display() / #counter(page).final().first()],
    )
  },
)

#set text(font: "DejaVu Serif", size: 9.8pt, lang: "pt", region: "BR")
#set par(justify: true, leading: 0.66em, spacing: 1.02em)
#set heading(numbering: none)

#show heading.where(level: 1): it => block(above: 1.45em, below: 0.6em)[
  #set text(font: "DejaVu Sans", weight: "bold", size: 13.5pt, fill: rgb("#1d3b5c"))
  #it.body
  #v(-2pt)
  #line(length: 100%, stroke: 0.6pt + rgb("#1d3b5c").lighten(55%))
]
#show heading.where(level: 2): it => block(above: 1.1em, below: 0.4em)[
  #set text(font: "DejaVu Sans", weight: "bold", size: 11pt, fill: rgb("#2c5d86"))
  #it.body
]
#show heading.where(level: 3): it => block(above: 0.9em, below: 0.3em)[
  #set text(font: "DejaVu Sans", weight: "bold", size: 9.8pt)
  #it.body
]

#show raw: set text(font: "DejaVu Sans Mono", size: 8.4pt)
#show link: set text(fill: rgb("#1d5f9e"))

#show figure: it => block(above: 0.9em, below: 1em, breakable: false, it)

#show table: set text(size: 8.6pt)
#show table.cell.where(y: 0): set text(weight: "bold", size: 8.4pt, fill: rgb("#1d3b5c"))
#show table: set par(justify: false, leading: 0.5em)
#show table.cell: set align(left)

// ------------------------------------------------------------------ capa
#block(above: 0mm, below: 4mm)[
  #set par(justify: false)
  #text(font: "DejaVu Sans", size: 8pt, fill: luma(110), tracking: 0.12em)[
    PS-001 · DOCUMENTO CONTROLADO
  ]
  #v(2mm)
  #block[
    #set par(leading: 1.15em, justify: false)
    #text(font: "DejaVu Sans", weight: "bold", size: 20pt, fill: rgb("#1d3b5c"))[$title$]
  ]
  #v(1.5mm)
  #text(font: "DejaVu Sans", size: 11pt, fill: luma(70))[$subtitle$]
]

#table(
  columns: (auto, 1fr, auto, 1fr),
  inset: (x: 6pt, y: 4pt),
  stroke: 0.4pt + luma(200),
  fill: (x, y) => if y == 0 { luma(245) },
  [*Código*], [#docid], [*Revisão*], [#rev],
  [*Estado*], [#docstatus], [*Data*], [#docdate],
  [*Autor*], [#docauthor], [*Produto*], [#docproject],
)

#v(1mm)
#block(below: 1.2em)[
  #set text(size: 8pt, fill: luma(95))
  #set par(justify: true)
  Documento de *estudo*. O PS-001 é uma reconstrução por observação, sem
  certificação e sem vínculo com o fabricante. Licença do conteúdo próprio:
  CC BY-NC-SA 4.0. Riscos e escopo em `LEGAL.md`.
]
#line(length: 100%, stroke: 0.5pt + luma(180))
#v(2mm)

$body$
